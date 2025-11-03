# 🔐 Environment Variables Setup Guide

## 📋 Required Environment Variables

### For Vercel Deployment

1. **ไปที่ Vercel Dashboard**
   - URL: https://vercel.com
   - เลือก Project: `lhb-ubo`
   - ไปที่ **Settings** → **Environment Variables**

2. **เพิ่ม Environment Variables:**

| Variable | Value | Description |
|----------|-------|-------------|
| `ENLITE_API_KEY` | `HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV` | Enlite API Key (Required) |
| `ENLITE_API_URL` | `https://xignal-uat.bol.co.th` | Enlite API Base URL (Optional) |
| `ENLITE_API_TIMEOUT` | `60` | API Timeout in seconds (Optional) |

3. **ตั้งค่า Environment:**

   - **Production:** ✅ Enable
   - **Preview:** ✅ Enable (ถ้าต้องการใช้ใน preview deployments)
   - **Development:** ❌ Optional

4. **Save** และ **Redeploy** project

---

## 🖥️ Local Development

### Option 1: Environment Variables

```bash
export ENLITE_API_KEY="your-api-key-here"
export ENLITE_API_URL="https://xignal-uat.bol.co.th"
export ENLITE_API_TIMEOUT="60"

python3 enhanced_app.py
```

### Option 2: .env file (Recommended)

สร้างไฟล์ `.env` ใน root directory:

```bash
ENLITE_API_KEY=your-api-key-here
ENLITE_API_URL=https://xignal-uat.bol.co.th
ENLITE_API_TIMEOUT=60
```

**หมายเหตุ:** `.env` ถูก ignore ใน `.gitignore` แล้ว

### Option 3: Use Default Values

ถ้าไม่ตั้งค่า environment variables, ระบบจะใช้ default values:
- `ENLITE_API_KEY`: Default API key (hardcoded)
- `ENLITE_API_URL`: `https://xignal-uat.bol.co.th`
- `ENLITE_API_TIMEOUT`: `60`

---

## ✅ ตรวจสอบการตั้งค่า

### ใน Vercel

1. ไปที่ **Vercel Dashboard** → **Project** → **Settings** → **Environment Variables**
2. ตรวจสอบว่า variables ถูกตั้งค่าแล้ว
3. ตรวจสอบว่า **Production** environment ถูก enable

### ใน Code

```python
# final_ubo_system.py
ENLITE_API_KEY = os.getenv('ENLITE_API_KEY', 'default-key')
ENLITE_API_URL = os.getenv('ENLITE_API_URL', 'https://xignal-uat.bol.co.th')
ENLITE_API_TIMEOUT = int(os.getenv('ENLITE_API_TIMEOUT', '60'))
```

---

## 🔒 Security Best Practices

1. **ไม่ commit API keys** ไป Git
   - `.env` ถูก ignore ใน `.gitignore` แล้ว
   - ใช้ environment variables สำหรับ sensitive data

2. **ใช้ Production API Key** สำหรับ Production
   - ตั้งค่าใน Vercel Environment Variables
   - ไม่ hardcode ใน code

3. **Separate Keys** สำหรับ Production และ UAT
   - Production: Production API key
   - Preview: UAT API key (optional)

---

## 📝 ตัวอย่างการใช้งาน

### Vercel Dashboard

```
Environment Variables

┌─────────────────────┬──────────────────────────────────────────┬─────────────┐
│ Variable            │ Value                                    │ Environment │
├─────────────────────┼──────────────────────────────────────────┼─────────────┤
│ ENLITE_API_KEY      │ HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSk...    │ Production  │
│ ENLITE_API_URL      │ https://xignal-uat.bol.co.th            │ Production  │
│ ENLITE_API_TIMEOUT  │ 60                                       │ Production  │
└─────────────────────┴──────────────────────────────────────────┴─────────────┘
```

### Local Development

```bash
# Set environment variables
export ENLITE_API_KEY="your-production-key"
export ENLITE_API_URL="https://xignal-uat.bol.co.th"
export ENLITE_API_TIMEOUT="60"

# Run application
python3 enhanced_app.py
```

---

## 🚨 Troubleshooting

### ปัญหา: API Key not found

**อาการ:** `ValueError: API key not found`

**แก้ไข:**
1. ตรวจสอบว่า `ENLITE_API_KEY` ถูกตั้งค่าใน Vercel
2. ตรวจสอบว่า Production environment ถูก enable
3. Redeploy project หลังเพิ่ม environment variables

### ปัญหา: API Timeout

**อาการ:** API requests timeout

**แก้ไข:**
1. เพิ่ม `ENLITE_API_TIMEOUT` ใน Vercel (เช่น: `90`)
2. ตรวจสอบ API server status
3. ตรวจสอบ network connectivity

---

## ✅ Checklist

- [x] ตั้งค่า `ENLITE_API_KEY` ใน Vercel
- [x] ตั้งค่า `ENLITE_API_URL` (optional)
- [x] ตั้งค่า `ENLITE_API_TIMEOUT` (optional)
- [ ] Enable Production environment
- [ ] Redeploy project
- [ ] ทดสอบ API endpoint

---

**เสร็จแล้ว! 🎉**

