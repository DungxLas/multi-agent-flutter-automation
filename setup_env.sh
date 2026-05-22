#!/bin/bash

# Màu sắc hiển thị
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===> Khởi tạo môi trường ảo Python (venv)...${NC}"
python3 -m venv venv

echo -e "${BLUE}===> Kích hoạt môi trường ảo...${NC}"
source venv/bin/activate

echo -e "${BLUE}===> Nâng cấp pip...${NC}"
pip install --upgrade pip

echo -e "${BLUE}===> Cài đặt các thư viện từ requirements.txt...${NC}"
pip install -r requirements.txt

# Tạo file .env nếu chưa tồn tại
if [ ! -f .env ]; then
    echo -e "${BLUE}===> Tạo file cấu hình .env mẫu...${NC}"
    echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
    echo -e "${GREEN}Đã tạo file .env. Vui lòng cập nhật GEMINI_API_KEY của bạn vào file này.${NC}"
fi

echo -e "${GREEN}===> THÀNH CÔNG! Để bắt đầu, hãy kích hoạt môi trường ảo bằng lệnh:${NC}"
echo -e "${GREEN}source venv/bin/activate${NC}"
