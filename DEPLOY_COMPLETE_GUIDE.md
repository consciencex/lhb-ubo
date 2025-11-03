# 🚀 คู่มือ Deploy ครบถ้วน - LH Bank UBO Analysis System

## ✅ สิ่งที่แก้ไขแล้ว

1. ✅ แก้ `vercel.json` - ลบ `builds` และใช้แค่ `functions` + `rewrites`
2. ✅ ปรับ `vercel_app.py` - ใช้ auto-detection ของ Vercel
3. ✅ ปรับ `api/index.py` - ใช้ auto-detection ของ Vercel
4. ✅ JavaScript errors - แก้แล้วใน `enhanced_index.html`

---

## 📋 ขั้นตอนที่ 1: Push ไป GitHub

```bash
# 1. ไปที่ directory
cd /Users/waiywaiy/UBO

# 2. ตรวจสอบ status
git status

# 3. Add files ที่แก้ไข
git add .

# 4. Commit
git commit -m "Fix Vercel deployment: remove builds, use functions only"

# 5. Push ไป GitHub
git push origin main
```

---

## 📋 ขั้นตอนที่ 2: Deploy ไป Vercel

### วิธีที่ 1: ผ่าน Vercel Dashboard (แนะนำ)

1. **ไปที่ Vercel Dashboard**
   - URL: https://vercel.com
   - Login ด้วย GitHub account

2. **Import Project**
   - คลิก "Add New Project"
   - เลือก repository: `consciencex/lhb-ubo`

3. **Configure Project**
   
   **Project Name:** `lhb-ubo` (หรือชื่ออื่นที่ไม่ซ้ำ)
   
   **Framework Preset:** 
   - เลือก **"Flask"** หรือ **"Other"**
   
   **Root Directory:** 
   - `./` (root ของ repo)
   
   **Build and Output Settings:**
   - **Build Command:** (ว่างเปล่า - ไม่ต้องใส่)
   - **Output Directory:** (ว่างเปล่า - ไม่ต้องใส่)
   - **Install Command:** `pip install -r requirements.txt`

4. **Environment Variables** (Optional)
   - ถ้ามี API keys หรือ sensitive data
   - คลิก "Add" เพื่อเพิ่ม:
     - `API_KEY` = `your-api-key`
     - `API_TIMEOUT` = `60`

5. **Deploy**
   - คลิกปุ่ม **"Deploy"**
   - รอ deployment เสร็จ (ประมาณ 2-5 นาที)

---

### วิธีที่ 2: ผ่าน Vercel CLI

```bash
# 1. Install Vercel CLI (ถ้ายังไม่มี)
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
cd /Users/waiywaiy/UBO
vercel

# 4. Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (เลือก account)
# - Link to existing project? No (ถ้าใหม่)
# - Project name? lhb-ubo
# - Directory? ./
# - Override settings? No
```

---

## 🔧 Vercel Configuration

ไฟล์ `vercel.json` ที่แก้ไขแล้ว:

```json
{
  "version": 2,
  "functions": {
    "api/index.py": {
      "maxDuration": 60,
      "memory": 3008
    },
    "vercel_app.py": {
      "maxDuration": 60,
      "memory": 3008
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/index.py"
    },
    {
      "source": "/(.*)",
      "destination": "/vercel_app.py"
    }
  ],
  "regions": ["sin1"]
}
```

**อธิบาย:**
- `functions` - กำหนด timeout และ memory สำหรับ functions
- `rewrites` - route requests ไปยัง Python files
- `regions` - ใช้ Singapore region (ใกล้ประเทศไทย)

---

## ✅ หลัง Deploy สำเร็จ

### URLs ที่จะได้:

1. **Production URL:**
   - `https://lhb-ubo.vercel.app` (หรือชื่อตาม project)

2. **Preview URLs:**
   - `https://lhb-ubo-git-main.vercel.app` (สำหรับ main branch)
   - `https://lhb-ubo-git-[branch].vercel.app` (สำหรับ branches อื่น)

### Auto-Deploy:

- ✅ ทุกครั้งที่ push ไป `main` branch = auto-deploy production
- ✅ ทุกครั้งที่ push ไป branch อื่น = auto-deploy preview

---

## 🧪 ทดสอบหลัง Deploy

### 1. เปิด URL Production
```
https://lhb-ubo.vercel.app
```

### 2. ทดสอบการทำงาน
- ใส่ Company ID: `0107548000234`
- คลิก "Analyze UBO"
- ตรวจสอบว่าทำงานได้ปกติ

### 3. ตรวจสอบ API Endpoint
```
https://lhb-ubo.vercel.app/api/status
```

ควรได้ response:
```json
{
  "status": "running",
  "ubo_system_initialized": true,
  "timestamp": "2025-10-30 21:00:00"
}
```

---

## ⚠️ Troubleshooting

### ปัญหา: Build failed

**แก้ไข:**
1. ตรวจสอบ Vercel build logs
2. ตรวจสอบว่า `requirements.txt` ครบถ้วน
3. ตรวจสอบว่า `vercel.json` ไม่มี syntax error

### ปัญหา: Function timeout

**แก้ไข:**
- ตรวจสอบว่า `maxDuration: 60` ถูกตั้งค่าใน `vercel.json`
- Vercel Pro tier รองรับถึง 60 วินาที ✅

### ปัญหา: Module not found

**แก้ไข:**
- ตรวจสอบว่า dependencies ใน `requirements.txt` ครบ
- ตรวจสอบว่า import paths ถูกต้อง

### ปัญหา: 404 Not Found

**แก้ไข:**
- ตรวจสอบ `rewrites` ใน `vercel.json`
- ตรวจสอบว่าไฟล์ `vercel_app.py` และ `api/index.py` มีอยู่

---

## 📝 Checklist

### ก่อน Deploy:
- [x] แก้ `vercel.json` (ลบ `builds`, ใช้ `functions` + `rewrites`)
- [x] ปรับ `vercel_app.py` (ใช้ auto-detection)
- [x] ปรับ `api/index.py` (ใช้ auto-detection)
- [x] แก้ JavaScript errors

### ขั้นตอน Deploy:
- [ ] Push ไป GitHub (`git push origin main`)
- [ ] Import project ใน Vercel Dashboard
- [ ] ตั้งค่า Project (Framework: Flask, Install: `pip install -r requirements.txt`)
- [ ] Deploy
- [ ] ทดสอบ Production URL

---

## 🎉 เสร็จแล้ว!

หลังจาก deploy สำเร็จ:
- ✅ Production URL พร้อมใช้งาน
- ✅ Auto-deploy เมื่อ push ไป GitHub
- ✅ Preview deployments สำหรับ branches อื่น
- ✅ Vercel Pro features: 60s timeout, 3008MB memory, Singapore region

---

**พร้อม Deploy แล้ว! 🚀**

