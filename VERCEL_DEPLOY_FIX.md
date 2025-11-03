# 🔧 แก้ปัญหา Vercel Deployment

## ❌ ปัญหา: Project name already exists

**Error:** `Project "lhb-dx-ubo" already exists, please use a new name.`

---

## ✅ วิธีแก้ไข

### วิธีที่ 1: เปลี่ยนชื่อ Project (แนะนำ)

1. ในหน้า Vercel "New Project"
2. **Project Name** - เปลี่ยนจาก `lhb-dx-ubo` เป็นชื่ออื่น เช่น:
   - `lhb-ubo` ✅ (แนะนำ - ตรงกับ repo name)
   - `lhb-ubo-analysis`
   - `lhb-ubo-system`
   - `lhb-ubo-app`
   - `ubo-analysis-lhb`
3. คลิก **"Deploy"** อีกครั้ง

---

### วิธีที่ 2: ลบ Project เก่า (ถ้าต้องการใช้ชื่อเดิม)

1. ไปที่ Vercel Dashboard
2. หา project `lhb-dx-ubo` (ที่สร้างไว้แล้ว)
3. ไปที่ Settings → Delete Project
4. ลบ project เก่า
5. สร้างใหม่ด้วยชื่อเดิม

---

## ✅ ตรวจสอบ Settings ที่ถูกต้อง

### 1. **Project Name**
- ใช้ชื่อที่ไม่ซ้ำ เช่น: `lhb-ubo`

### 2. **Framework Preset**
- ✅ **Flask** (ถูกต้อง)

### 3. **Root Directory**
- ✅ `./` (ถูกต้อง - root ของ repo)

### 4. **Build and Output Settings** (คลิกเพื่อขยาย)

**Build Command:** (ว่างเปล่า - ไม่ต้องใส่)
```
(ไม่ต้องใส่)
```

**Output Directory:** (ว่างเปล่า - ไม่ต้องใส่)
```
(ไม่ต้องใส่)
```

**Install Command:**
```
pip install -r requirements.txt
```

### 5. **Environment Variables** (คลิกเพื่อขยาย)

**ถ้ามี API keys หรือ sensitive data:**
- `API_KEY` = `your-api-key-here`
- `API_TIMEOUT` = `60`

**ถ้าไม่มี:** (ไม่ต้องใส่)

---

## 🎯 Recommended Settings Summary

```
Project Name: lhb-ubo
Framework Preset: Flask
Root Directory: ./
Install Command: pip install -r requirements.txt
Build Command: (empty)
Output Directory: (empty)
```

---

## ✅ หลังแก้ไขแล้ว

1. เปลี่ยนชื่อ project
2. ตรวจสอบ settings
3. คลิก **"Deploy"**
4. รอ deployment เสร็จ (ประมาณ 2-5 นาที)
5. คุณจะได้ URL เช่น: `https://lhb-ubo.vercel.app`

---

## 🚀 Next Steps

หลังจาก deploy สำเร็จ:
- ✅ Production URL: `https://lhb-ubo.vercel.app`
- ✅ Auto-deploy เมื่อ push ไป GitHub
- ✅ Preview deployments สำหรับ branches อื่นๆ

---

**เสร็จแล้ว! เปลี่ยนชื่อ project แล้วลอง deploy อีกครั้ง** 🎉

