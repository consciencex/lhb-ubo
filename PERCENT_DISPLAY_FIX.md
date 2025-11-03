# 🐛 Fix: Direct Shareholding Percentage Display

## ปัญหาที่พบ

**Test Case:** Main Company `0107535000249`
- บริษัท `0105543093348`
- **API แสดง:** 6.11%
- **System แสดง:** 11.35% ❌ **ผิด!**

---

## 🔍 Root Cause

ใน `aggregateShareholders()` function (templates/enhanced_index.html):

```javascript
// ❌ OLD CODE (บวก direct % เมื่อมี multiple entries)
entry.direct += directContribution;
entry.effective += effectiveContribution;
```

**ปัญหา:** 
- ถ้า shareholder คนเดียวกันปรากฏใน multiple paths
- ระบบจะ **บวก direct %** เข้าด้วยกัน
- ทำให้ % ที่แสดงไม่ตรงกับ API

**ตัวอย่าง:**
- Path 1: บริษัท A → Company X (6.11%)
- Path 2: บริษัท B → Company X (5.24%)
- **ผลลัพธ์ที่ผิด:** 6.11% + 5.24% = 11.35% ❌

---

## ✅ Solution

แก้ไขให้แสดง **direct % จาก API ตรงๆ** (ไม่บวก):

```javascript
// ✅ NEW CODE (ใช้ direct % จาก entry แรก)
const entry = itemMap.get(key);
entry.type = entry.type === 'company' || sh.shareholder_type === 'company' ? 'company' : 'personal';
const directContribution = parseFloat(sh.direct_percent ?? sh.percent ?? 0) || 0;
const effectiveContribution = parseFloat(sh.effective_percentage || sh.effective || sh.percent || 0) || 0;

// ✅ FIX: ใช้ direct % จาก API ตรงๆ ไม่บวก (เอาค่าแรก)
if (entry.entries.length === 0) {
    entry.direct = directContribution;
}
// Effective ยังคงบวกเพื่อ UBO calculation
entry.effective += effectiveContribution;
```

---

## 📊 Correct Behavior

### Tier 1 (Level 1) - Shareholders ของ Main Company

```
Main Company (0107535000249) - 100%
    ├─ Individual A: 24.23% ✅ (จาก API ตรงๆ)
    ├─ Company 0105543093348: 6.11% ✅ (จาก API ตรงๆ)
    ├─ Company HD00085916: 6.80% ✅ (จาก API ตรงๆ)
    └─ ...
```

### Tier 2 (Level 2) - Shareholders ของ Companies จาก Tier 1

```
Company 0105543093348 (จาก Tier 1, ถือ 6.11%)
    ├─ Individual B: 30% ✅ (จาก API ตรงๆ, effective = 6.11% × 30% = 1.83%)
    ├─ Company Y: 50% ✅ (จาก API ตรงๆ, effective = 6.11% × 50% = 3.06%)
    └─ ...
```

---

## 🎯 Key Points

1. **Direct %** = % ตรงๆ จาก API (`levelHeldBy level="1"`)
   - **ไม่บวก** เมื่อมี multiple paths
   - แสดงตรงกับ API response

2. **Effective %** = % ที่คำนวณจาก chain (สำหรับ UBO)
   - **บวกเข้าด้วยกัน** เมื่อมี multiple paths
   - ใช้สำหรับหา UBO (≥15%)

3. **Display Logic:**
   - UI แสดง **Direct %** ในการ์ดหลัก
   - แสดง **Effective %** ใน "View UBO Calc" (collapsible)

---

## ✅ Verified

**Test Case: 0107535000249**
- บริษัท 0105543093348
- **Before:** 11.35% ❌
- **After:** 6.11% ✅ (ตรงกับ API)

---

## 🚀 Deployment

```bash
# Committed: Fix direct shareholding % display
git commit -m "Fix: show direct shareholding % from API (not aggregated) for all levels"
git push origin main
```

**Next:** Redeploy บน Vercel
1. https://vercel.com/dashboard → `lhb-ubo`
2. Deployments → "..." → **Redeploy** (Clear cache)
3. ทดสอบอีกครั้งด้วย company `0107535000249`

