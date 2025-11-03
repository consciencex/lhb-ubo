# 🚂 Railway.app Deployment Guide

## ✅ สรุป

ผมได้ **restore ทุก features กลับมา** แล้ว:
- ✅ pandas, openpyxl dependencies
- ✅ Excel export function
- ✅ ทุก features ครบถ้วน

พร้อม deploy บน Railway.app (Production-Grade Platform)

---

## 🎯 ทำไมต้อง Railway?

### Vercel ปัญหา:
- ❌ Serverless limit: 250MB
- ❌ pandas (~200MB) + dependencies = เกินขนาด
- ❌ ต้องลบ features

### Railway.app ข้อดี:
- ✅ **ไม่มีขีดจำกัดขนาด** - รองรับ dependencies ทุกตัว
- ✅ **Deploy ง่าย** - Connect GitHub repository (1-click)
- ✅ **ราคาถูก** - $5/month (Hobby plan)
- ✅ **Production-ready** - Auto-scaling, monitoring, logging
- ✅ **Keep ทุก features** - Excel export, ทุกอย่าง
- ✅ **Auto-deploy** - Push to GitHub = Auto-deploy

---

## 🚀 ขั้นตอนการ Deploy

### 1. Commit และ Push Changes

```bash
cd /Users/waiywaiy/UBO

git add .
git commit -m "Restore full dependencies for Railway deployment"
git push origin main
```

### 2. สร้าง Railway Account

1. ไปที่ https://railway.app
2. คลิก **"Login"**
3. เลือก **"Login with GitHub"**
4. Authorize Railway

### 3. Deploy Project

1. คลิก **"New Project"**
2. เลือก **"Deploy from GitHub repo"**
3. เลือก repository: `consciencex/lhb-ubo`
4. Railway จะ:
   - Auto-detect Flask app
   - Install dependencies จาก `requirements.txt`
   - Deploy automatically

### 4. Set Environment Variables

1. ใน Railway Dashboard → เลือก project
2. ไปที่ **"Variables"** tab
3. เพิ่ม environment variables:

```
ENLITE_API_KEY = HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV
ENLITE_API_URL = https://xignal-uat.bol.co.th
ENLITE_API_TIMEOUT = 60
PORT = 4444
```

### 5. Configure Start Command (Optional)

Railway จะ auto-detect Flask, แต่ถ้าต้องการกำหนดเอง:

1. ไปที่ **"Settings"** → **"Deploy"**
2. Set **Start Command**:
   ```bash
   gunicorn vercel_app:app --bind 0.0.0.0:$PORT
   ```

หรือสร้างไฟล์ `Procfile`:
```
web: gunicorn vercel_app:app --bind 0.0.0.0:$PORT
```

### 6. Deploy!

- Railway จะเริ่ม build และ deploy
- ใช้เวลา 2-5 นาที
- หลัง deploy สำเร็จ จะได้ URL: `https://your-app.railway.app`

---

## 📝 ไฟล์ที่ต้องเพิ่ม (Optional)

### `Procfile`
```
web: gunicorn vercel_app:app --bind 0.0.0.0:$PORT --timeout 120
```

### Update `requirements.txt` (เพิ่ม gunicorn)
```txt
requests>=2.31.0
pandas>=2.0.0
openpyxl>=3.1.0
flask>=2.3.0
flask-cors>=4.0.0
lxml>=4.9.0
python-dateutil>=2.8.0
gunicorn>=21.2.0
```

---

## 🎯 หลัง Deploy

### 1. ตรวจสอบ Deployment

1. ไปที่ Railway Dashboard
2. ดู Deployment Logs
3. ตรวจสอบว่า deploy สำเร็จ

### 2. Test Application

```bash
# Test status endpoint
curl https://your-app.railway.app/api/status

# Expected response:
{
  "status": "running",
  "ubo_system_initialized": true,
  "timestamp": "2025-11-03 15:00:00"
}
```

### 3. Test UBO Analysis

1. เปิด browser ไปที่ `https://your-app.railway.app`
2. ใส่ registration ID: `0107562000386`
3. คลิก "Analyze UBO"
4. ตรวจสอบผลลัพธ์

---

## 💰 ราคา

### Railway.app Pricing

| Plan | Price | Resources | Recommended |
|------|-------|-----------|-------------|
| **Developer** | Free | 500 execution hours/month | Testing |
| **Hobby** | $5/month | Unlimited hours | ✅ **Production** |
| **Pro** | $20/month | Priority support | Enterprise |

**แนะนำ: Hobby ($5/month)** - เพียงพอสำหรับ production use

---

## 🔄 Auto-Deploy

Railway จะ auto-deploy เมื่อ:
- Push code ใหม่ไป GitHub (branch `main`)
- ไม่ต้องทำอะไรเพิ่ม

---

## 📊 Monitoring

Railway มี built-in monitoring:
- CPU usage
- Memory usage
- Request metrics
- Logs (real-time)

Access: Railway Dashboard → Project → Metrics

---

## ⚙️ Configuration

### Custom Domain (Optional)

1. ไปที่ **"Settings"** → **"Domains"**
2. คลิก **"Add Domain"**
3. ใส่ custom domain
4. Update DNS records

### Scaling (Optional)

Railway จะ auto-scale, แต่สามารถกำหนดได้:
1. ไปที่ **"Settings"** → **"Resources"**
2. ปรับ CPU/Memory limits

---

## 🆚 Comparison: Railway vs Vercel

| Feature | Railway | Vercel |
|---------|---------|--------|
| **Serverless Limits** | ❌ None | ✅ 250MB |
| **Full Dependencies** | ✅ Yes | ❌ No (pandas too large) |
| **Excel Export** | ✅ Yes | ❌ Disabled |
| **Price** | $5/month | $20/month |
| **Deploy Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Auto-Deploy** | ✅ Yes | ✅ Yes |
| **Monitoring** | ✅ Built-in | ✅ Built-in |
| **Production-Ready** | ✅ Yes | ✅ Yes (with limits) |

**Winner: Railway** - ถูกกว่า, ไม่มีข้อจำกัด, keep ทุก features

---

## 🐛 Troubleshooting

### Build Failed

1. ตรวจสอบ `requirements.txt` syntax
2. ดู build logs ใน Railway Dashboard
3. ตรวจสอบ Python version (Railway ใช้ 3.11 by default)

### App Not Starting

1. ตรวจสอบ environment variables
2. ดู runtime logs
3. ตรวจสอบ start command

### API Errors

1. ตรวจสอบ `ENLITE_API_KEY` ถูกต้อง
2. ดู application logs
3. Test API endpoint ด้วย curl

---

## ✅ Checklist

- [ ] Push code to GitHub
- [ ] Create Railway account
- [ ] Deploy from GitHub
- [ ] Set environment variables
- [ ] Test deployment
- [ ] Verify all features work
- [ ] Update custom domain (optional)

---

## 🎉 Done!

หลังจาก deploy แล้ว คุณจะได้:
- ✅ Production-grade UBO Analysis System
- ✅ ทุก features ครบถ้วน (Excel export)
- ✅ Auto-scaling
- ✅ Monitoring
- ✅ Auto-deploy from GitHub
- ✅ ราคาถูก ($5/month)

---

## 📚 Resources

- Railway Docs: https://docs.railway.app
- Flask Deployment: https://docs.railway.app/deploy/deployments
- Environment Variables: https://docs.railway.app/develop/variables

---

**พร้อม deploy แล้ว! 🚀**

