# 🔧 Vercel Environment Variables - Required

## ❌ ปัญหาปัจจุบัน

**API Error 500:** `/api/analyze` ไม่ทำงาน

**สาเหตุน่าจะเป็น:** Environment Variables ยังไม่ได้ตั้งใน Vercel Dashboard

---

## ✅ Fix: ตั้งค่า Environment Variables

### ใน Vercel Dashboard:

1. ไปที่ https://vercel.com/dashboard
2. เลือก project: `lhb-ubo`
3. ไปที่ **Settings** → **Environment Variables**
4. เพิ่ม variables ต่อไปนี้:

---

### Required Variable (ต้องมี):

```
Key: ENLITE_API_KEY
Value: HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV

Environments:
✅ Production
✅ Preview
✅ Development
```

---

### Optional Variables (แนะนำ):

```
Key: ENLITE_API_URL
Value: https://xignal-uat.bol.co.th

Environments:
✅ Production
✅ Preview
✅ Development
```

```
Key: ENLITE_API_TIMEOUT
Value: 60

Environments:
✅ Production
✅ Preview
✅ Development
```

---

## 🔄 หลังตั้งค่า Environment Variables

### ต้อง Redeploy:

1. ไปที่ **Deployments** tab
2. คลิก **"..."** (three dots) ที่ latest deployment
3. เลือก **"Redeploy"**
4. รอ 2-3 นาที

---

## ✅ ตรวจสอบว่าตั้งค่าถูกต้อง

หลัง Redeploy, ทดสอบ API:

```bash
curl https://lhb-ubo.vercel.app/api/status

# Expected response:
{
  "status": "running",
  "ubo_system_initialized": true,
  "timestamp": "..."
}
```

ถ้าได้ `"ubo_system_initialized": true` แสดงว่า Environment Variables ตั้งถูกต้อง ✅

---

## 🎯 หลังแก้ไข

- ✅ API จะทำงานได้
- ✅ กราฟจะแสดงผล
- ✅ ข้อมูลจะโหลดได้

---

**สำคัญ:** ต้องตั้งค่า Environment Variables ใน Vercel Dashboard ก่อนใช้งาน!

