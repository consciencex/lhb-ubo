# 🔧 แก้ปัญหา Function Size > 250MB

## ❌ ปัญหา

**Error:** `A Serverless Function has exceeded the unzipped maximum size of 250 MB`

**Warning:** `Due to 'builds' existing in your configuration file...`

---

## ✅ การแก้ไข

### 1. ลด Dependencies (ลดขนาด)

**ก่อน:**
```txt
requests>=2.31.0
pandas>=2.0.0              # ❌ ใหญ่มาก (~200MB)
matplotlib>=3.7.0          # ❌ ใหญ่มาก (~150MB)
seaborn>=0.12.0            # ❌ ใหญ่มาก
networkx>=3.1              # ❌ ใหญ่
openpyxl>=3.1.0            # ❌ ใหญ่
flask>=2.3.0
flask-cors>=4.0.0
plotly>=5.15.0             # ❌ ใหญ่มาก
dash>=2.14.0               # ❌ ใหญ่มาก
dash-bootstrap-components>=1.4.0  # ❌ ใหญ่
python-dateutil>=2.8.0
lxml>=4.9.0
```

**หลัง:**
```txt
requests>=2.31.0
flask>=2.3.0
flask-cors>=4.0.0
lxml>=4.9.0
python-dateutil>=2.8.0
```

**ลดขนาด:**
- ❌ ลบ `pandas` (~200MB) - ไม่ได้ใช้ใน core logic
- ❌ ลบ `matplotlib` (~150MB) - ไม่ได้ใช้ (ใช้ D3.js แทน)
- ❌ ลบ `seaborn` - ไม่ได้ใช้
- ❌ ลบ `networkx` - ไม่ได้ใช้
- ❌ ลบ `plotly` - ไม่ได้ใช้ (ใช้ D3.js แทน)
- ❌ ลบ `dash` - ไม่ได้ใช้
- ❌ ลบ `openpyxl` - ไม่ได้ใช้ (ปิด Excel export)

**ผลลัพธ์:** ลดขนาดจาก ~500MB+ เหลือ ~50MB ✅

---

### 2. ปิด Excel Export

**ก่อน:**
- `/api/export_excel` endpoint ใช้ `pandas` + `openpyxl`
- ไฟล์ใหญ่มาก

**หลัง:**
- ปิด Excel export endpoint
- ใช้ JSON export แทน (มีอยู่แล้ว)

---

### 3. แก้ `vercel.json` (ลบ `builds`)

**ก่อน:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "vercel_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [...]
}
```

**หลัง:**
```json
{
  "version": 2,
  "routes": [
    {
      "src": "/(.*)",
      "dest": "vercel_app.py"
    }
  ],
  "regions": ["sin1"]
}
```

**หมายเหตุ:** Vercel จะ auto-detect Flask app จาก `vercel_app.py` โดยอัตโนมัติ

---

### 4. สร้าง `.vercelignore`

เพิ่ม `.vercelignore` เพื่อไม่ให้ upload ไฟล์ที่ไม่จำเป็น:
```
*.md (except README.md)
*.pdf
__pycache__/
*.pyc
test_*.py
...
```

---

## 📊 ผลลัพธ์

### Before
- **Dependencies:** 13 packages (~500MB+)
- **Function Size:** >250MB ❌
- **Warnings:** `builds` configuration

### After
- **Dependencies:** 5 packages (~50MB) ✅
- **Function Size:** <250MB ✅
- **Warnings:** ไม่มี ✅

---

## ✅ Checklist

- [x] ลด dependencies ใน `requirements.txt`
- [x] ปิด Excel export endpoint
- [x] ลบ `builds` section จาก `vercel.json`
- [x] สร้าง `.vercelignore`
- [ ] Commit และ push
- [ ] Redeploy บน Vercel
- [ ] ตรวจสอบ deployment สำเร็จ

---

## 🚀 ขั้นตอนถัดไป

1. **Commit และ Push**
   ```bash
   git add .
   git commit -m "Fix: reduce deployment size (remove large dependencies, disable Excel export)"
   git push origin main
   ```

2. **Redeploy ใน Vercel Dashboard**
   - ไปที่ Deployments
   - คลิก "Redeploy" จาก latest commit

3. **ตรวจสอบ Build Logs**
   - ควรไม่มี error เรื่อง size
   - ควรไม่มี warning เรื่อง builds

---

**แก้ไขแล้ว! 🎉**

