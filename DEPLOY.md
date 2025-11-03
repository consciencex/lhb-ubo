# 🚀 คู่มือ Deploy - LH Bank UBO Analysis System

## 📋 ขั้นตอนการ Deploy ไปที่ Vercel

### 1. เตรียม GitHub Repository

#### สร้าง Repository ใหม่บน GitHub
```bash
# 1. สร้าง repository ใหม่บน GitHub.com (ตั้งชื่อว่า ubo-analysis หรือชื่ออื่น)

# 2. Initialize git repository (ถ้ายังไม่มี)
cd /Users/waiywaiy/UBO
git init

# 3. Add files
git add .

# 4. Commit
git commit -m "Initial commit: UBO Analysis System"

# 5. Add remote (แทน YOUR_USERNAME และ REPO_NAME ด้วยค่าจริง)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

---

### 2. Deploy ไปที่ Vercel

#### วิธีที่ 1: ผ่าน Vercel Dashboard (แนะนำ)
1. ไปที่ [https://vercel.com](https://vercel.com)
2. สมัคร/Login ด้วย GitHub account
3. คลิก "Add New Project"
4. Import repository จาก GitHub
5. Vercel จะ auto-detect ว่าเป็น Python project
6. Settings:
   - **Framework Preset**: Other
   - **Build Command**: (ไม่ต้องใส่)
   - **Output Directory**: (ไม่ต้องใส่)
   - **Install Command**: `pip install -r requirements.txt`
7. คลิก "Deploy"

#### วิธีที่ 2: ผ่าน Vercel CLI
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
cd /Users/waiywaiy/UBO
vercel

# 4. Follow prompts
# - Set up and deploy? Yes
# - Which scope? (เลือก account)
# - Link to existing project? No
# - Project name? ubo-analysis
# - Directory? ./
```

---

### 3. ตั้งค่า Environment Variables (ถ้าจำเป็น)

ถ้ามี API keys หรือ sensitive data:

1. ไปที่ Vercel Dashboard → Project → Settings → Environment Variables
2. Add variables เช่น:
   - `API_KEY` (ถ้าใช้)
   - `API_URL` (ถ้าใช้)

---

### 4. ตรวจสอบ Deployment

หลังจาก Deploy สำเร็จ:
- Vercel จะให้ URL เช่น: `https://ubo-analysis.vercel.app`
- เปิด URL เพื่อทดสอบ

---

## 🔧 การแก้ไขปัญหา

### ปัญหา: Module not found
**แก้ไข:**
- ตรวจสอบว่า `requirements.txt` มี dependencies ครบ
- ตรวจสอบ Vercel build logs

### ปัญหา: Flask app not found
**แก้ไข:**
- ตรวจสอบ `vercel.json` configuration
- ตรวจสอบว่าไฟล์ `enhanced_app.py` อยู่ใน root directory

### ปัญหา: API timeout
**แก้ไข:**
- Vercel Serverless Functions มี timeout 10 วินาที (free tier)
- อาจต้องเพิ่ม timeout หรือใช้ Vercel Pro

---

## 📝 ไฟล์ที่สำคัญสำหรับ Deployment

### 1. `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "enhanced_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "enhanced_app.py"
    }
  ]
}
```

### 2. `requirements.txt`
- ต้องมี dependencies ครบถ้วน

### 3. `.gitignore`
- ไม่ commit sensitive files

---

## 🌐 Production URL

หลังจาก deploy สำเร็จ คุณจะได้ URL:
- **Production**: `https://your-project.vercel.app`
- **Preview**: `https://your-project-git-branch.vercel.app`

---

## ✅ Checklist

- [ ] สร้าง GitHub repository
- [ ] Push code ไป GitHub
- [ ] Connect Vercel กับ GitHub repository
- [ ] Deploy project
- [ ] ทดสอบ URL
- [ ] ตั้งค่า Environment Variables (ถ้าจำเป็น)
- [ ] ทดสอบ API endpoint

---

## 📞 สนับสนุน

ถ้ามีปัญหา:
1. ตรวจสอบ Vercel build logs
2. ตรวจสอบ browser console
3. ตรวจสอบ Network tab ใน DevTools

---

**เสร็จแล้ว! 🎉**

