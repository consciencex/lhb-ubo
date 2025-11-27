# 🐳 Docker Deployment Guide - UBO Analysis System

## 📋 ความต้องการ

- Docker Engine 20.10+
- Docker Compose 2.0+
- เครื่องต้องอยู่ใน VPN Network ที่เข้าถึง `enlite.lhb.co.th` ได้

---

## 🚀 Quick Start (2 คำสั่ง)

```bash
# 1. Clone repository
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo

# 2. Start with Docker Compose
docker-compose up -d
```

เปิด Browser: **http://localhost:4444**

---

## 📖 คำสั่งที่ใช้บ่อย

### เริ่มต้น Container
```bash
docker-compose up -d
```

### หยุด Container
```bash
docker-compose down
```

### ดู Logs
```bash
docker-compose logs -f
```

### Restart
```bash
docker-compose restart
```

### Rebuild (หลังอัพเดท code)
```bash
docker-compose up -d --build
```

---

## 🔧 การตั้งค่า

### เปลี่ยน Port

แก้ไข `docker-compose.yml`:
```yaml
ports:
  - "8080:4444"  # เปลี่ยน 8080 เป็น port ที่ต้องการ
```

### เปลี่ยน API Key

แก้ไข `docker-compose.yml`:
```yaml
environment:
  - ENLITE_API_KEY=your_new_api_key_here
```

---

## 🖥️ Deploy บน Windows (Docker Desktop)

### Step 1: ติดตั้ง Docker Desktop
1. ดาวน์โหลดจาก https://www.docker.com/products/docker-desktop
2. ติดตั้งและ restart เครื่อง
3. เปิด Docker Desktop

### Step 2: Clone และ Run
เปิด PowerShell หรือ Command Prompt:
```powershell
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo
docker-compose up -d
```

### Step 3: ตรวจสอบ
```powershell
docker-compose ps
docker-compose logs
```

---

## 🐧 Deploy บน Linux Server

### Step 1: ติดตั้ง Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin
```

### Step 2: Clone และ Run
```bash
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo
docker compose up -d
```

### Step 3: ตั้งค่า Auto-start
```bash
# Enable Docker service
sudo systemctl enable docker

# Container จะ restart อัตโนมัติ (restart: unless-stopped)
```

---

## 🔒 Security

### 1. ใช้ HTTPS (แนะนำสำหรับ Production)

ใช้ Nginx reverse proxy:

```nginx
# /etc/nginx/sites-available/ubo
server {
    listen 443 ssl;
    server_name ubo.yourbank.local;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:4444;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. จำกัด Network Access

```yaml
# docker-compose.yml
services:
  ubo-app:
    ports:
      - "127.0.0.1:4444:4444"  # เฉพาะ localhost
```

---

## 📊 Monitoring

### ตรวจสอบ Container Status
```bash
docker-compose ps
```

### ดู Resource Usage
```bash
docker stats lhb-ubo-system
```

### Health Check
```bash
curl http://localhost:4444/api/status
```

---

## ❓ Troubleshooting

### Container ไม่ start
```bash
# ดู logs
docker-compose logs

# ตรวจสอบ port ว่างหรือไม่
netstat -tulpn | grep 4444
```

### API Connection Failed
```bash
# เข้าไปใน container
docker exec -it lhb-ubo-system bash

# ทดสอบ connection
curl -v https://enlite.lhb.co.th
```

### Rebuild หลังแก้ไข code
```bash
docker-compose down
docker-compose up -d --build --force-recreate
```

### ลบ container และ image ทั้งหมด
```bash
docker-compose down --rmi all -v
```

---

## 📞 Support

หากพบปัญหา:
1. ตรวจสอบ logs: `docker-compose logs -f`
2. ตรวจสอบ VPN connection
3. ติดต่อทีมพัฒนา

