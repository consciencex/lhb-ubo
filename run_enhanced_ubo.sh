#!/bin/bash
# Enhanced UBO Detection System Launcher
# สคริปต์สำหรับเริ่มต้นระบบ Enhanced UBO

echo "🚀 Enhanced UBO Detection System"
echo "=================================="
echo "ระบบตรวจสอบผู้ได้รับผลประโยชน์ที่แท้จริง"
echo "ตามเอกสาร NC958 PRO05-2568"
echo ""

# ตรวจสอบ Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ไม่พบ Python3 กรุณาติดตั้ง Python3 ก่อน"
    exit 1
fi

echo "✅ พบ Python3: $(python3 --version)"

# ตรวจสอบ pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ ไม่พบ pip3 กรุณาติดตั้ง pip3 ก่อน"
    exit 1
fi

echo "✅ พบ pip3"

# ตรวจสอบไฟล์ requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ ไม่พบไฟล์ requirements.txt"
    exit 1
fi

echo "✅ พบไฟล์ requirements.txt"

# ติดตั้ง dependencies
echo ""
echo "📦 กำลังติดตั้ง dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ ติดตั้ง dependencies สำเร็จ"
else
    echo "❌ การติดตั้ง dependencies ล้มเหลว"
    exit 1
fi

# ตรวจสอบไฟล์หลัก
echo ""
echo "🔍 ตรวจสอบไฟล์หลัก..."

required_files=(
    "enhanced_ubo_system.py"
    "enhanced_app.py"
    "templates/enhanced_index.html"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ พบไฟล์: $file"
    else
        echo "❌ ไม่พบไฟล์: $file"
        exit 1
    fi
done

# สร้างโฟลเดอร์สำหรับรายงาน
mkdir -p reports
echo "✅ สร้างโฟลเดอร์ reports"

# แสดงเมนู
echo ""
echo "🎯 เลือกการทำงาน:"
echo "1. รัน Enhanced Web Application"
echo "2. ทดสอบระบบด้วย LAND AND HOUSES BANK"
echo "3. ทดสอบ API Connection"
echo "4. ดูสถานะระบบ"
echo "5. ออกจากระบบ"
echo ""

read -p "กรุณาเลือก (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🌐 กำลังเริ่มต้น Enhanced Web Application..."
        echo "   เข้าถึงระบบได้ที่: http://localhost:4444"
        echo "   กด Ctrl+C เพื่อหยุดระบบ"
        echo ""
        python3 enhanced_app.py
        ;;
    2)
        echo ""
        echo "🧪 กำลังทดสอบระบบด้วย LAND AND HOUSES BANK..."
        echo ""
        python3 enhanced_ubo_system.py
        ;;
    3)
        echo ""
        echo "🔌 กำลังทดสอบ API Connection..."
        echo ""
        python3 test_api_spec.py
        ;;
    4)
        echo ""
        echo "📊 สถานะระบบ:"
        echo "   ✅ Python3: $(python3 --version)"
        echo "   ✅ pip3: พร้อมใช้งาน"
        echo "   ✅ Dependencies: ติดตั้งแล้ว"
        echo "   ✅ ไฟล์หลัก: พร้อมใช้งาน"
        echo "   ✅ โฟลเดอร์ reports: พร้อมใช้งาน"
        echo ""
        echo "🎉 ระบบพร้อมใช้งาน!"
        ;;
    5)
        echo ""
        echo "👋 ออกจากระบบ"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1-5"
        exit 1
        ;;
esac
