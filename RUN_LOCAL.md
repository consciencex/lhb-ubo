# 🚀 คู่มือการรัน Local - LH Bank UBO Analysis System

## ขั้นตอนการรัน (แบบง่าย)

### 1. ติดตั้ง Dependencies
```bash
cd /Users/waiywaiy/UBO
pip3 install -r requirements.txt
```

### 2. เริ่มต้น Web Application
```bash
python3 enhanced_app.py
```

### 3. เข้าถึงระบบ
เปิดเบราว์เซอร์ไปที่: **http://localhost:4444**

---

## วิธีรันแบบละเอียด

### ตรวจสอบ Python
```bash
python3 --version
# ควรเป็น Python 3.7 หรือสูงกว่า
```

### ติดตั้ง Packages ที่จำเป็น
```bash
pip3 install -r requirements.txt
```

Packages หลัก:
- `flask` - Web framework
- `flask-cors` - CORS support
- `requests` - API calls
- `pandas` - Data processing
- `lxml` - XML parsing

### รัน Server
```bash
python3 enhanced_app.py
```

คุณจะเห็นข้อความ:
```
🚀 Enhanced UBO Web Application
==================================================
✅ UBO system initialized successfully
🌐 Starting web server...
   Access the UI at: http://localhost:4444
   Press Ctrl+C to stop the server
--------------------------------------------------
```

### หยุด Server
กด `Ctrl + C` ใน Terminal

---

## วิธีทดสอบ

### ทดสอบด้วย Company ID
1. เปิดเบราว์เซอร์ไปที่ `http://localhost:4444`
2. ใส่เลขทะเบียนบริษัท เช่น: `0107548000234`
3. คลิก "Analyze Company"
4. ดูผลการวิเคราะห์ UBO

### ทดสอบผ่าน API (Optional)
```bash
# ทดสอบ API connection
python3 test_api_spec.py

# ทดสอบ UBO calculation
python3 verify_calculation.py
```

---

## การแก้ไขปัญหา

### Port 4444 ถูกใช้งานแล้ว
```bash
# ตรวจสอบ port
lsof -i :4444

# เปลี่ยน port ใน enhanced_app.py (บรรทัด 384)
app.run(host='0.0.0.0', port=5555, debug=True)  # เปลี่ยนเป็น port อื่น
```

### Module not found
```bash
# ติดตั้ง dependencies ใหม่อีกครั้ง
pip3 install -r requirements.txt --upgrade
```

### API Connection Error
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ตรวจสอบ VPN (ถ้ามี)
- API อาจตอบช้า (timeout 60 วินาที)

---

## ไฟล์สำคัญ

- **`enhanced_app.py`** - Flask web application (รันไฟล์นี้)
- **`final_ubo_system.py`** - Core UBO calculation logic
- **`templates/enhanced_index.html`** - Frontend UI
- **`requirements.txt`** - Python dependencies

---

## สรุป Quick Start

```bash
# 1. ติดตั้ง dependencies
pip3 install -r requirements.txt

# 2. รัน server
python3 enhanced_app.py

# 3. เปิดเบราว์เซอร์
# http://localhost:4444
```

**เสร็จแล้ว! 🎉**
