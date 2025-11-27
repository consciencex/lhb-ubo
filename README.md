# 🏦 LH Bank UBO Analysis System

ระบบวิเคราะห์ Ultimate Beneficial Owner (UBO) สำหรับธนาคารแลนด์ แอนด์ เฮ้าส์

---

## 🚀 Quick Start (Docker - แนะนำ)

### ความต้องการ
- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop))
- เครื่องต้องอยู่ใน **VPN Network** ที่เข้าถึง API ได้

### 4 ขั้นตอน

```bash
# 1. Clone repository
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo

# 2. สร้างไฟล์ .env (ใส่ API Key)
cp env.example .env

# 3. แก้ไข .env ใส่ API Key จริง
notepad .env   # Windows
nano .env      # Mac/Linux

# 4. Start container
docker-compose up -d
```

### เปิดใช้งาน
```
http://localhost:4444
```

---

## 📝 ตั้งค่า API Key

แก้ไขไฟล์ `.env`:

```env
ENLITE_API_KEY=your_api_key_here
ENLITE_API_URL=https://enlite.lhb.co.th
ENLITE_API_TIMEOUT=60
```

> ⚠️ **สำคัญ:** ไฟล์ `.env` จะไม่ถูก commit เข้า git (เพื่อความปลอดภัย)

---

## 🖥️ วิธี Deploy อื่นๆ

### Option 2: Python โดยตรง (ไม่ใช้ Docker)

```bash
# 1. Clone
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo

# 2. ติดตั้ง dependencies
pip install -r requirements.txt

# 3. สร้าง .env
cp env.example .env
notepad .env  # ใส่ API Key

# 4. Run
python enhanced_app.py
```

### Option 3: Windows (Double-click)

1. ดาวน์โหลด ZIP จาก GitHub
2. แตกไฟล์
3. สร้างไฟล์ `.env` จาก `env.example`
4. Double-click `install_windows.bat` (ติดตั้ง)
5. Double-click `start_server.bat` (รัน)

---

## 📁 โครงสร้าง Project

```
lhb-ubo/
├── app.py                  # Vercel entrypoint
├── enhanced_app.py         # Main Flask application
├── final_ubo_system.py     # Core UBO analysis logic
├── mock_data_generator.py  # Mock data for testing
├── templates/
│   └── enhanced_index.html # Frontend UI
├── static/
│   ├── css/               # Stylesheets
│   ├── icon/              # Logo
│   └── locales/           # i18n (TH/EN)
├── docs/                  # Documentation
├── env.example            # Environment template
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker compose
├── requirements.txt       # Python dependencies
└── vercel.json           # Vercel config
```

---

## 🔧 คำสั่งที่ใช้บ่อย

### Docker
```bash
docker-compose up -d      # Start
docker-compose down       # Stop
docker-compose logs -f    # View logs
docker-compose restart    # Restart
docker-compose up -d --build  # Rebuild
```

### ตรวจสอบ
```bash
# Health check
curl http://localhost:4444/api/status

# ดู container
docker ps
```

---

## 🌐 Network Requirements

ระบบต้องสามารถเข้าถึง:
- `https://enlite.lhb.co.th` (Production API)

> หากไม่สามารถเข้าถึง API ได้ ตรวจสอบว่าเครื่องอยู่ใน VPN Network

---

## 📖 เอกสารเพิ่มเติม

| เอกสาร | คำอธิบาย |
|--------|---------|
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | คู่มือ Deploy ละเอียด |
| [docs/DOCKER_DEPLOY.md](docs/DOCKER_DEPLOY.md) | Docker deployment guide |
| [docs/README_DEPLOY.md](docs/README_DEPLOY.md) | Windows deployment guide |
| [docs/ALGORITHM_CONFIRMATION.md](docs/ALGORITHM_CONFIRMATION.md) | UBO calculation algorithm |

---

## ❓ Troubleshooting

### "ENLITE_API_KEY not set"
```bash
# ตรวจสอบว่ามีไฟล์ .env
cat .env

# ถ้าไม่มี ให้สร้างใหม่
cp env.example .env
# แล้วแก้ไขใส่ API Key
```

### "Connection refused" หรือ API ไม่ตอบ
- ตรวจสอบว่าเชื่อมต่อ VPN แล้ว
- ทดสอบ: `ping enlite.lhb.co.th`

### Docker ไม่ start
```bash
docker-compose logs  # ดู error
docker-compose down --rmi all  # ลบแล้วสร้างใหม่
docker-compose up -d --build
```

---

## 📞 Support

หากพบปัญหา ติดต่อทีมพัฒนา

---

**Version:** 2.0.0  
**Last Updated:** November 2025
