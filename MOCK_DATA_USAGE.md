# 🎭 Mock Data Usage Guide

## 📋 Overview

สร้าง Mock Data สำหรับทดสอบ NetworkX Spider-Web Visualization โดยไม่กระทบระบบเดิม

---

## 🚀 How to Use

### ✅ ใช้ Mock Data

**Input:** กรอก Registration ID = `XXXXXXXX`

```
1. เปิดเว็บแอป: https://lhb-ubo.vercel.app
2. กรอก Registration ID: XXXXXXXX
3. คลิก "Analyze UBO"
4. ระบบจะใช้ Mock Data แสดงผล
```

### ✅ ใช้ Real Data

**Input:** กรอก Registration ID จริง เช่น `0107548000234`

```
1. เปิดเว็บแอป: https://lhb-ubo.vercel.app
2. กรอก Registration ID: 0107548000234
3. คลิก "Analyze UBO"
4. ระบบจะเรียก API จริง
```

---

## 📊 Mock Data Details

### Main Company
- **Name:** DEMO BANK PUBLIC COMPANY LIMITED
- **ID:** XXXXXXXX
- **Capital:** ฿50,000,000,000
- **Type:** Banking and Financial Services

### Hierarchy Structure

**Level 0 (Main Company):**
- DEMO BANK PUBLIC COMPANY LIMITED (100%)

**Level 1 (6 Shareholders):**
1. GLOBAL INVESTMENT CORPORATION (35.50%) - Company
2. ASIA PACIFIC HOLDINGS LTD (28.75%) - Company
3. EUROPEAN FINANCIAL GROUP (18.20%) - Company
4. MICHAEL BROWN (12.50%) - Individual
5. EMMA WILSON (3.80%) - Individual
6. OLIVIA MARTIN (1.25%) - Individual

**Level 2 (6 Companies):**
1. COMP_A → WILLIAM ANDERSON (45%), SOPHIA CHEN (32%), VENTURE CAPITAL PARTNERS (23%)
2. COMP_B → JAMES TANAKA (52.87%), WILLIAM ANDERSON (35%), STRATEGIC INVESTMENTS INC (12.13%)
3. COMP_C → SOPHIA CHEN (40.66%), INTERNATIONAL EQUITY FUND (46.70%), LUCAS BERGMANN (12.64%)
4. COMP_D → WILLIAM ANDERSON (72%), DAVID KIM (28%)
5. COMP_E → SOPHIA CHEN (85%), ALEXANDER NOVAK (15%)
6. COMP_F → EMILY RODRIGUEZ (100%)

---

## 🎯 UBO Results

### ✅ UBO Candidates (≥15%)

| Name | Total % | Paths | Nationality | Director | Status |
|------|---------|-------|-------------|----------|--------|
| WILLIAM ANDERSON | 28.50% | 2 | American | Yes | ✅ UBO |
| SOPHIA CHEN | 18.75% | 3 | Singaporean | No | ✅ UBO |
| JAMES TANAKA | 15.20% | 1 | Japanese | Yes | ✅ UBO |

### ❌ Non-UBO (<15%)

| Name | Total % | Nationality |
|------|---------|-------------|
| EMILY RODRIGUEZ | 8.50% | Spanish |
| DAVID KIM | 6.30% | Korean |
| MICHAEL BROWN | 12.50% | British |
| EMMA WILSON | 3.80% | Australian |
| OLIVIA MARTIN | 1.25% | Canadian |

---

## 🕸️ Network Visualization Features

Mock Data ถูกออกแบบเพื่อแสดง:

1. **Node Sizes** - ขนาดต่างกันตามทุนจดทะเบียน:
   - Main Company: ฿50B (largest)
   - COMP_B: ฿12B
   - COMP_A: ฿8.5B
   - COMP_C: ฿6.75B
   - COMP_F: ฿4.5B
   - COMP_E: ฿3.2B
   - COMP_D: ฿2.1B (smallest)

2. **Edge Thickness** - ความหนาต่างกันตาม %:
   - Thickest: 52.87% (JAMES TANAKA → COMP_B)
   - Medium: 35.50% (COMP_A → Main)
   - Thin: 1.25% (OLIVIA MARTIN → Main)

3. **Colors** - แยกสีตาม type:
   - 🔵 Blue: Companies
   - 🟢 Green: Individuals (non-UBO)
   - 🔴 Red: UBOs (≥15%)

4. **3-Tier Structure** - แสดงการถือหุ้น 3 ทอด:
   - Tier 1: 6 shareholders
   - Tier 2: 6 companies
   - Tier 3: 11 individuals

5. **Spider-Web Layout** - แสดงความสัมพันธ์แบบ network:
   - Main company ตรงกลาง
   - Shareholders กระจายรอบๆ
   - Multiple paths สำหรับ WILLIAM ANDERSON & SOPHIA CHEN

---

## 🔍 Testing Scenarios

Mock Data ออกแบบเพื่อทดสอบ:

### ✅ Scenario 1: Multiple Paths
**WILLIAM ANDERSON** ถือหุ้นผ่าน 2 paths:
- Path 1: Main → COMP_A → WILLIAM (45%) = 15.975%
- Path 2: Main → COMP_B → WILLIAM (35%) = 10.0625%
- **Total:** 28.50% ✅ UBO

### ✅ Scenario 2: Multiple Levels
**SOPHIA CHEN** ถือหุ้นผ่าน 3 paths:
- Path 1: Main → COMP_A → SOPHIA (32%) = 11.36%
- Path 2: Main → COMP_C → SOPHIA (40.66%) = 7.40%
- Path 3: Main → COMP_A → COMP_E → SOPHIA (85%) = 6.94%
- **Total:** 18.75% ✅ UBO

### ✅ Scenario 3: Single Path High %
**JAMES TANAKA** ถือหุ้นผ่าน 1 path:
- Path 1: Main → COMP_B → JAMES (52.87%) = 15.20%
- **Total:** 15.20% ✅ UBO

### ❌ Scenario 4: Below Threshold
**EMILY RODRIGUEZ** ถือหุ้นผ่าน 1 path:
- Path 1: Main → COMP_C → COMP_F → EMILY (100%) = 8.50%
- **Total:** 8.50% ❌ Not UBO

---

## 💻 Implementation

### Backend Logic

```python
# enhanced_app.py

if registration_id == "XXXXXXXX":
    # Use mock data
    mock_report = generate_mock_ubo_data()
    
    # Build network graph
    mock_report['network_graph'] = build_network_graph(...)
    
    return jsonify({
        'success': True,
        'data': mock_report,
        'is_mock': True  # Flag to indicate mock data
    })
else:
    # Use real API
    result = analyze_company_ubo(registration_id)
    ...
```

### Mock Data Generator

```python
# mock_data_generator.py

def generate_mock_ubo_data():
    return {
        'company_info': {...},
        'hierarchy_data': {...},
        'ubos': [...],
        'analysis_summary': {...}
    }
```

---

## 🎯 Benefits

1. **No API Dependency** - ทดสอบได้โดยไม่ต้องเรียก API จริง
2. **Consistent Results** - ผลลัพธ์เหมือนเดิมทุกครั้ง
3. **Complex Scenario** - มี multiple paths, multiple levels
4. **Visual Testing** - ทดสอบ NetworkX visualization ได้ชัดเจน
5. **No Side Effects** - ไม่กระทบระบบเดิมเลย

---

## 📚 Files

| File | Purpose |
|------|---------|
| `mock_data_generator.py` | Generate mock data structure |
| `enhanced_app.py` | Check for "XXXXXXXX" and use mock |
| `MOCK_DATA_USAGE.md` | This documentation |

---

## 🚀 Deployment

```bash
# Already deployed (commit: 107a560)
git add -A
git commit -m "Add: Mock data generator for testing"
git push origin main

# Redeploy on Vercel
```

**Test URL:** https://lhb-ubo.vercel.app

**Test ID:** `XXXXXXXX`

---

**Note:** Mock data จะแสดงเมื่อกรอก Registration ID = `XXXXXXXX` เท่านั้น ไม่กระทบการทำงานปกติของระบบ

