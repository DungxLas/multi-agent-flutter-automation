import time
import os
import json
import hashlib
from google import genai
from google.genai import types

# Xác định đường dẫn file cache tại thư mục gốc của workspace
CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.gemini_api_cache.json')

def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"  [Cảnh báo]: Không thể đọc file cache: {e}")
    return {}

def save_cache(cache: dict):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  [Cảnh báo]: Không thể ghi file cache: {e}")

def get_cache_key(model: str, contents, config) -> str:
    # Chuẩn hóa contents thành chuỗi để hash
    if hasattr(contents, 'model_dump'):
        contents_str = json.dumps(contents.model_dump(), sort_keys=True)
    elif isinstance(contents, (dict, list)):
        contents_str = json.dumps(contents, sort_keys=True)
    else:
        contents_str = str(contents)

    # Trích xuất thông tin cấu hình
    system_instruction = ""
    temperature = None
    response_schema_name = ""
    
    if config:
        if hasattr(config, 'system_instruction') and config.system_instruction:
            system_instruction = str(config.system_instruction)
        if hasattr(config, 'temperature') and config.temperature is not None:
            temperature = config.temperature
        if hasattr(config, 'response_schema') and config.response_schema:
            if hasattr(config.response_schema, '__name__'):
                response_schema_name = config.response_schema.__name__
            else:
                response_schema_name = str(config.response_schema)
                
    key_dict = {
        'model': model,
        'contents': contents_str,
        'system_instruction': system_instruction,
        'temperature': temperature,
        'response_schema_name': response_schema_name
    }
    
    key_str = json.dumps(key_dict, sort_keys=True)
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()

def generate_content_with_retry(
    client,
    contents,
    config,
    primary_model='gemini-3.5-flash',
    fallback_model='gemini-2.5-flash',
    max_retries=3,
    initial_delay=2.0
):
    """
    Gọi Gemini API với cơ chế tự động thử lại (Retry), chuyển đổi sang model dự phòng (Fallback)
    và lưu/đọc kết quả từ Cache cục bộ (Local Cache) để tối ưu hóa hạn mức RPD/RPM.
    """
    # Đọc model từ biến môi trường nếu có
    primary_model = os.getenv("GEMINI_PRIMARY_MODEL", primary_model)
    fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", fallback_model)
    
    models_to_try = [primary_model, fallback_model]
    last_exception = None

    # Tính cache key dựa trên model chính (primary_model)
    # Điều này giúp nếu primary model lỗi và chạy fallback thành công, ta vẫn cache lại dưới key của primary model
    # để các lần chạy sau lấy kết quả ngay lập tức mà không cần gọi API thật.
    hash_key = get_cache_key(primary_model, contents, config)
    
    # 1. Kiểm tra cache trước
    cache = load_cache()
    if hash_key in cache:
        cached_text = cache[hash_key]
        print(f"  [Cache Hit]: Sử dụng kết quả cache cho model {primary_model}.")
        
        parsed_obj = None
        if config and getattr(config, 'response_schema', None):
            schema = config.response_schema
            try:
                from pydantic import BaseModel
                if hasattr(schema, 'model_validate_json'):
                    parsed_obj = schema.model_validate_json(cached_text)
                elif hasattr(schema, 'parse_raw'):
                    parsed_obj = schema.parse_raw(cached_text)
                else:
                    data = json.loads(cached_text)
                    parsed_obj = schema(**data)
            except Exception as parse_err:
                print(f"  [Cảnh báo]: Lỗi parse cache, chuyển sang gọi API thật: {parse_err}")
                parsed_obj = None
                
        if parsed_obj is not None or not (config and getattr(config, 'response_schema', None)):
            class CachedResponse:
                def __init__(self, text, parsed=None):
                    self.text = text
                    self.parsed = parsed
            return CachedResponse(text=cached_text, parsed=parsed_obj)

    # 2. Gọi API thật nếu không trúng cache
    for model in models_to_try:
        delay = initial_delay
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                
                # Lưu phản hồi vào cache
                if response and hasattr(response, 'text') and response.text:
                    cache = load_cache()
                    cache[hash_key] = response.text
                    save_cache(cache)
                    
                return response
            except Exception as e:
                last_exception = e
                err_msg = str(e)
                # Kiểm tra lỗi tạm thời 503 (UNAVAILABLE) hoặc 429 (RESOURCE_EXHAUSTED)
                is_transient = any(code in err_msg for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"])
                
                if is_transient:
                    if attempt < max_retries:
                        print(f"  [Lỗi gọi API {model} (Lần thử {attempt}/{max_retries})]: {e}. Đang thử lại sau {delay}s...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        print(f"  [Cảnh báo]: Thử lại model {model} thất bại. Chuyển sang thử model tiếp theo...")
                else:
                    # Lỗi cấu hình hoặc API Key không hợp lệ, không cần thử lại
                    raise e
    raise last_exception
