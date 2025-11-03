# 🔐 คู่มือตั้งค่า Environment Variables บน Vercel

## 📋 ภาพรวม

หลังจาก import project ใหม่ใน Vercel คุณต้องตั้งค่า Environment Variables เพื่อให้ระบบทำงานได้อย่างถูกต้อง

---

## 🚀 ขั้นตอนที่ 1: ไปที่ Environment Variables Settings

1. **Login เข้า Vercel Dashboard**
   - ไปที่ [https://vercel.com](https://vercel.com)
   - Login ด้วย GitHub account

2. **เลือก Project**
   - คลิกที่ project: `lhb-ubo`
   - หรือ project name ที่คุณตั้งไว้

3. **ไปที่ Settings**
   - คลิกแท็บ **"Settings"** ที่ด้านบน
   - เลื่อนลงไปหา **"Environment Variables"** ในเมนูด้านซ้าย
   - หรือคลิก **"Environment Variables"** จากเมนู

---

## 🔧 ขั้นตอนที่ 2: เพิ่ม Environment Variables

### 1. คลิก "Add New" หรือ "Add"

- จะเห็นปุ่ม **"Add New"** หรือ **"Add"**
- คลิกเพื่อเพิ่ม variable ใหม่

### 2. เพิ่ม Variables ตามตารางนี้

| Variable Name | Value | Environment | คำอธิบาย |
|--------------|-------|-------------|----------|
| `ENLITE_API_KEY` | `HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV` | ✅ Production<br>✅ Preview<br>✅ Development | Enlite API Key (Required) |
| `ENLITE_API_URL` | `https://xignal-uat.bol.co.th` | ✅ Production<br>✅ Preview<br>✅ Development | Enlite API Base URL (Optional) |
| `ENLITE_API_TIMEOUT` | `60` | ✅ Production<br>✅ Preview<br>✅ Development | API Timeout in seconds (Optional) |

---

## 📝 ขั้นตอนที่ 3: ตั้งค่าแต่ละ Variable

### Variable 1: `ENLITE_API_KEY`

1. **Key:**
   ```
   ENLITE_API_KEY
   ```

2. **Value:**
   ```
   HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV
   ```

3. **Environment:**
   - ✅ **Production** (ต้องเลือก)
   - ✅ **Preview** (แนะนำให้เลือก)
   - ✅ **Development** (optional)

4. **คลิก "Save"**

---

### Variable 2: `ENLITE_API_URL` (Optional)

1. **Key:**
   ```
   ENLITE_API_URL
   ```

2. **Value:**
   ```
   https://xignal-uat.bol.co.th
   ```

3. **Environment:**
   - ✅ **Production**
   - ✅ **Preview**
   - ✅ **Development**

4. **คลิก "Save"**

---

### Variable 3: `ENLITE_API_TIMEOUT` (Optional)

1. **Key:**
   ```
   ENLITE_API_TIMEOUT
   ```

2. **Value:**
   ```
   60
   ```

3. **Environment:**
   - ✅ **Production**
   - ✅ **Preview**
   - ✅ **Development**

4. **คลิก "Save"**

---

## 🎯 ตัวอย่างหน้าจอ Vercel Dashboard

### หน้า Environment Variables

```
┌─────────────────────────────────────────────────────┐
│ Environment Variables                                │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ ENLITE_API_KEY                              │   │
│  │ •••••••••••••••••••••••••••••••••••••••••   │   │
│  │ Production ✅  Preview ✅  Development ✅     │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ ENLITE_API_URL                              │   │
│  │ https://xignal-uat.bol.co.th                │   │
│  │ Production ✅  Preview ✅  Development ✅     │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ ENLITE_API_TIMEOUT                          │   │
│  │ 60                                          │   │
│  │ Production ✅  Preview ✅  Development ✅     │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  [+ Add New]                                        │
└─────────────────────────────────────────────────────┘
```

---

## ⚠️ หมายเหตุสำคัญ

### 1. Production vs Preview vs Development

- **Production**: ใช้สำหรับ production deployment
- **Preview**: ใช้สำหรับ preview deployments (branch deployments)
- **Development**: ใช้สำหรับ local development (`vercel dev`)

**แนะนำ:** เลือกทั้ง 3 ตัวเพื่อให้ทำงานได้ทุก environment

### 2. Sensitive Data

- `ENLITE_API_KEY` เป็น sensitive data
- Vercel จะ **encrypt** และเก็บไว้อย่างปลอดภัย
- Values จะถูก **mask** ใน dashboard (แสดงเป็น `••••`)

### 3. Redeploy หลังตั้งค่า

- หลังจากเพิ่ม/แก้ไข Environment Variables
- **ต้อง Redeploy** deployment ปัจจุบัน
- หรือรอ deployment ใหม่ (auto-deploy)

---

## ✅ หลังตั้งค่าเสร็จ

### 1. ตรวจสอบ Variables

- ตรวจสอบว่าเพิ่มครบ 3 variables
- ตรวจสอบว่าเลือก Environment ถูกต้อง

### 2. Redeploy

1. ไปที่ **"Deployments"** tab
2. คลิก **"..."** (three dots) ที่ latest deployment
3. เลือก **"Redeploy"**
4. หรือรอ auto-deploy จาก commit ใหม่

### 3. ตรวจสอบ Deployment

- ตรวจสอบ build logs ว่าสำเร็จ
- ตรวจสอบ function logs ว่าอ่าน environment variables ได้

---

## 🧪 ทดสอบ Environment Variables

### ใน Vercel Function Logs

1. ไปที่ **"Deployments"** → เลือก deployment
2. ไปที่ **"Functions"** tab
3. ดู logs - ควรเห็น API calls ทำงานได้

### ทดสอบ API Endpoint

```bash
curl https://your-project.vercel.app/api/status
```

ควรได้ response:
```json
{
  "status": "running",
  "ubo_system_initialized": true,
  "timestamp": "2025-11-03 14:40:00"
}
```

---

## 📋 Checklist

- [ ] Login เข้า Vercel Dashboard
- [ ] ไปที่ Project → Settings → Environment Variables
- [ ] เพิ่ม `ENLITE_API_KEY` (Production ✅)
- [ ] เพิ่ม `ENLITE_API_URL` (Production ✅, Optional)
- [ ] เพิ่ม `ENLITE_API_TIMEOUT` (Production ✅, Optional)
- [ ] Redeploy latest deployment
- [ ] ตรวจสอบ deployment สำเร็จ
- [ ] ทดสอบ API endpoint

---

## 🚨 Troubleshooting

### ปัญหา: Environment Variable not found

**อาการ:** Function error: `ENLITE_API_KEY not found`

**แก้ไข:**
1. ตรวจสอบว่าเพิ่ม variable แล้ว
2. ตรวจสอบว่าเลือก **Production** environment
3. **Redeploy** deployment

### ปัญหา: API calls fail

**อาการ:** API requests timeout หรือ connection error

**แก้ไข:**
1. ตรวจสอบว่า `ENLITE_API_KEY` ถูกต้อง
2. ตรวจสอบว่า `ENLITE_API_URL` ถูกต้อง
3. ตรวจสอบ network/VPN connectivity

---

## 📚 References

- [Vercel Environment Variables Documentation](https://vercel.com/docs/projects/environment-variables)
- [Vercel Environment Variables Best Practices](https://vercel.com/docs/projects/environment-variables#environment-variables)

---

**เสร็จแล้ว! 🎉**

