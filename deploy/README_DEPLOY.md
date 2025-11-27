# 🚀 คู่มือ Deploy UBO Analysis System บน Server ภายใน

## 📋 ความต้องการระบบ

- **OS:** Windows 10/11 หรือ Windows Server 2016+
- **Python:** 3.8 หรือสูงกว่า
- **RAM:** อย่างน้อย 2GB
- **Network:** อยู่ใน VPN network ที่สามารถเข้าถึง `enlite.lhb.co.th` ได้

---

## 🔐 Security: ตั้งค่า API Key

**⚠️ สำคัญ: ห้าม hardcode API key ใน source code!**

ต้องสร้างไฟล์ `.env` เพื่อเก็บ API key:

```cmd
copy env.example .env
notepad .env
```

**แก้ไขไฟล์ .env:**
```
ENLITE_API_KEY=your_actual_api_key_here
ENLITE_API_URL=https://enlite.lhb.co.th
ENLITE_API_TIMEOUT=60
```

---

## 📦 ขั้นตอนการติดตั้ง

### Step 1: ติดตั้ง Python (ถ้ายังไม่มี)

1. ดาวน์โหลด Python จาก https://www.python.org/downloads/
2. ระหว่างติดตั้ง ✅ เลือก **"Add Python to PATH"**
3. ติดตั้งให้เสร็จ

### Step 2: ดาวน์โหลด Source Code

**วิธีที่ 1: Clone จาก GitHub**
```cmd
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo
```

**วิธีที่ 2: ดาวน์โหลด ZIP**
1. ไปที่ https://github.com/consciencex/lhb-ubo
2. คลิก "Code" → "Download ZIP"
3. แตกไฟล์ไปยัง folder ที่ต้องการ เช่น `C:\UBO`

### Step 3: ตั้งค่า API Key

```cmd
cd C:\UBO
copy env.example .env
notepad .env
```

แก้ไข `ENLITE_API_KEY=your_actual_api_key_here` ให้เป็น key จริง

### Step 4: ติดตั้ง Dependencies

เปิด Command Prompt (cmd) แล้วรัน:

```cmd
cd C:\UBO
pip install -r requirements.txt
```

### Step 5: รันระบบ

**วิธีที่ 1: รันด้วย Command**
```cmd
cd C:\UBO
python enhanced_app.py
```

**วิธีที่ 2: Double-click ไฟล์ (Windows)**
- Double-click ที่ไฟล์ `start_server.bat`

### Step 5: เปิดใช้งาน

เปิด Browser แล้วไปที่:
```
http://localhost:4444
```

หรือถ้าต้องการให้เครื่องอื่นในเครือข่ายเข้าถึง:
```
http://[IP-ของเครื่อง]:4444
```

---

## 🔧 การตั้งค่าเพิ่มเติม

### เปลี่ยน Port (ถ้าต้องการ)

แก้ไขไฟล์ `enhanced_app.py` บรรทัดสุดท้าย:
```python
app.run(host='0.0.0.0', port=4444, debug=False)
#                            ^^^^
#                     เปลี่ยนเป็น port ที่ต้องการ
```

### ตั้งค่า Environment Variables (Optional)

สร้างไฟล์ `.env`:
```
ENLITE_API_KEY=fVldOOnGL48NHuUYclP5kLKtZXoCZOr49DFtDqR5vLleuQJ1wQdMyLpY8P7g2ZtQ
ENLITE_API_URL=https://enlite.lhb.co.th
```

---

## 🖥️ รัน Server ตลอดเวลา (Windows Service)

### วิธีที่ 1: ใช้ NSSM (แนะนำ)

1. ดาวน์โหลด NSSM จาก https://nssm.cc/download
2. แตกไฟล์แล้วรัน:
```cmd
nssm install UBOService
```
3. ตั้งค่า:
   - **Path:** `C:\Python311\python.exe`
   - **Startup directory:** `C:\UBO`
   - **Arguments:** `enhanced_app.py`
4. คลิก "Install service"

### วิธีที่ 2: ใช้ Task Scheduler

1. เปิด Task Scheduler
2. สร้าง Task ใหม่
3. ตั้งค่า Trigger: "At startup"
4. ตั้งค่า Action: Run `C:\UBO\start_server.bat`

---

## 🔒 การรักษาความปลอดภัย

### 1. เปิด Firewall สำหรับ Port 4444
```cmd
netsh advfirewall firewall add rule name="UBO System" dir=in action=allow protocol=TCP localport=4444
```

### 2. จำกัดการเข้าถึงเฉพาะ IP ภายใน
แก้ไข `enhanced_app.py`:
```python
from flask import Flask, request, abort

@app.before_request
def limit_remote_addr():
    allowed_ips = ['172.20.', '10.0.', '192.168.']  # ปรับตาม network
    client_ip = request.remote_addr
    if not any(client_ip.startswith(prefix) for prefix in allowed_ips):
        abort(403)
```

---

## ❓ แก้ไขปัญหา

### ปัญหา: "python is not recognized"
- ติดตั้ง Python ใหม่และเลือก "Add to PATH"
- หรือใช้ full path: `C:\Python311\python.exe enhanced_app.py`

### ปัญหา: "Module not found"
```cmd
pip install flask flask-cors requests networkx openpyxl
```

### ปัญหา: "Port already in use"
```cmd
netstat -ano | findstr :4444
taskkill /PID [PID_NUMBER] /F
```

### ปัญหา: API ไม่ตอบ
- ตรวจสอบว่าเครื่องอยู่ใน VPN network
- ทดสอบด้วย: `ping enlite.lhb.co.th`

---

## 📞 ติดต่อ Support

หากพบปัญหา สามารถติดต่อทีมพัฒนาได้

