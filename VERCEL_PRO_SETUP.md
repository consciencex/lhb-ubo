# 🚀 Vercel Pro Setup Guide - LH Bank UBO Analysis System

## ✅ Configuration สำหรับ Vercel Pro ($20 tier)

### 📋 Features ที่ได้จาก Vercel Pro

1. **Function Timeout**: 60 วินาที (แทน 10 วินาที)
2. **Memory**: สูงสุด 3008 MB (แทน 1024 MB)
3. **Bandwidth**: ไม่จำกัด (แทน 100 GB/month)
4. **Builds**: ไม่จำกัด
5. **Custom Domain**: สนับสนุน
6. **Regions**: เลือก region ได้ (เช่น Singapore `sin1`)

---

## ⚙️ Configuration ที่อัพเดทแล้ว

### 1. `vercel.json`

เพิ่ม configurations:
```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 60,
      "memory": 3008,
      "runtime": "python3.9"
    },
    "vercel_app.py": {
      "maxDuration": 60,
      "memory": 3008,
      "runtime": "python3.9"
    }
  },
  "regions": ["sin1"]
}
```

**คำอธิบาย:**
- `maxDuration: 60` - อนุญาตให้ function รันได้นานถึง 60 วินาที (เหมาะกับ API ที่ตอบช้า)
- `memory: 3008` - ใช้ memory สูงสุด (เหมาะกับการประมวลผลข้อมูลจำนวนมาก)
- `regions: ["sin1"]` - ใช้ Singapore region (ใกล้ประเทศไทย, latency ต่ำ)

---

## 🔧 การตั้งค่าเพิ่มเติม

### 1. Environment Variables (ถ้าจำเป็น)

ไปที่ Vercel Dashboard → Project → Settings → Environment Variables

**ตัวอย่าง:**
- `API_KEY` - API key สำหรับ Enlite API (ถ้าใช้)
- `API_TIMEOUT` - Timeout สำหรับ API calls (default: 60)
- `LOG_LEVEL` - Log level (INFO, DEBUG, etc.)

### 2. Custom Domain (ถ้าต้องการ)

1. ไปที่ Vercel Dashboard → Project → Settings → Domains
2. Add domain
3. ตั้งค่า DNS records ตามที่ Vercel แนะนำ

---

## 📊 Performance Optimization

### 1. API Timeout
- ตอนนี้ใช้ timeout 60 วินาที (ใน `final_ubo_system.py`)
- เหมาะกับ API ที่ตอบช้า

### 2. Memory
- ใช้ 3008 MB (สูงสุด)
- เหมาะกับการประมวลผลข้อมูลจำนวนมาก (3 levels hierarchy)

### 3. Region
- ใช้ Singapore (`sin1`)
- Latency ต่ำสำหรับผู้ใช้ในประเทศไทย

---

## 🎯 Best Practices

### 1. Caching
- Vercel Pro มี bandwidth ไม่จำกัด แต่ควร cache API responses
- ใช้ `cache` dictionary ใน `FinalEnliteAPIClient` (มีอยู่แล้ว)

### 2. Error Handling
- Handle timeout errors อย่างถูกต้อง (มีอยู่แล้ว)
- Log errors สำหรับ debugging

### 3. Monitoring
- ใช้ Vercel Analytics (ถ้าเปิดใช้งาน)
- ตรวจสอบ Function logs ใน Vercel Dashboard

---

## ✅ Checklist

- [x] อัพเดท `vercel.json` สำหรับ Pro tier
- [x] เพิ่ม `maxDuration: 60` สำหรับ API functions
- [x] เพิ่ม `memory: 3008` สำหรับการประมวลผล
- [x] ตั้งค่า region เป็น `sin1` (Singapore)
- [ ] ตั้งค่า Environment Variables (ถ้าจำเป็น)
- [ ] ตั้งค่า Custom Domain (ถ้าต้องการ)

---

## 🌐 หลัง Deploy

### Production URL
- **Default**: `https://your-project.vercel.app`
- **Custom Domain**: `https://your-domain.com` (ถ้าตั้งค่า)

### Function Performance
- **Timeout**: 60 วินาที (แทน 10 วินาที)
- **Memory**: 3008 MB (แทน 1024 MB)
- **Region**: Singapore (`sin1`) - Latency ต่ำ

---

## 📞 Troubleshooting

### ปัญหา: Function timeout
- **แก้ไข**: ตรวจสอบว่า `maxDuration: 60` ถูกตั้งค่าใน `vercel.json`

### ปัญหา: Memory limit
- **แก้ไข**: ตรวจสอบว่า `memory: 3008` ถูกตั้งค่าใน `vercel.json`

### ปัญหา: High latency
- **แก้ไข**: ตรวจสอบว่า `regions: ["sin1"]` ถูกตั้งค่าใน `vercel.json`

---

## 🎉 เสร็จแล้ว!

ตอนนี้ระบบพร้อมใช้งานบน Vercel Pro tier พร้อม configurations ที่เหมาะสมสำหรับการประมวลผล UBO analysis ที่ใช้เวลานานและต้องการ memory สูง

