# ✅ UBO Logic Clarification

## 🎯 UBO Definition (Final)

**UBO (Ultimate Beneficial Owner) ต้องเป็น PERSON (Individual) เท่านั้น**

- ✅ **Yes UBO**: บุคคลธรรมดา (Personal shareholder) ที่มี effective ownership ≥ 15%
- ❌ **Not UBO**: บริษัท (Corporate shareholder) ไม่ใช่ UBO แม้จะมี effective ownership ≥ 15%

---

## 📊 Algorithm

### 3-Tier Shareholding Analysis

**ระบบจะค้นหาผู้ถือหุ้น 3 ทอด:**

1. **Tier 1 (Level 1)**: ผู้ถือหุ้นโดยตรงของบริษัทหลัก
2. **Tier 2 (Level 2)**: ผู้ถือหุ้นของบริษัททั้งหมดใน Tier 1
3. **Tier 3 (Level 3)**: ผู้ถือหุ้นของบริษัททั้งหมดใน Tier 2

**การระบุ UBO:**
- ✅ เก็บ **Personal shareholders** ไว้ใน UBO candidates
- ✅ คำนวณ **effective ownership %** จาก chain
- ✅ UBO = Personal shareholders ที่มี total effective % ≥ 15%
- ❌ **Corporate shareholders** ไม่ใช่ UBO (ใช้เพื่อ drill down ต่อเท่านั้น)

---

## 🔄 Processing Flow

```
Main Company (100%)
    ├─ Personal A: 30% → ✅ Check if ≥15% → UBO Candidate
    ├─ Company X: 25% → ❌ Not UBO, but drill down to find shareholders
    │   ├─ Personal B: 50% → effective = 25% × 50% = 12.5% → Check if ≥15%
    │   └─ Company Y: 30% → ❌ Not UBO, but drill down
    │       └─ Personal C: 80% → effective = 25% × 30% × 80% = 6% → Check if ≥15%
    └─ Personal D: 20% → ✅ Check if ≥15% → UBO Candidate
```

**ผลลัพธ์:**
- Personal A: 30% ≥ 15% → ✅ **UBO**
- Personal D: 20% ≥ 15% → ✅ **UBO**
- Personal B: 12.5% < 15% → ❌ Not UBO
- Personal C: 6% < 15% → ❌ Not UBO
- Company X: 25% → ❌ **Not UBO** (เพราะเป็นบริษัท)
- Company Y: 7.5% → ❌ **Not UBO** (เพราะเป็นบริษัท)

---

## 🚫 What is NOT a UBO

### 1. Corporate Shareholders (บริษัท)
**ไม่นับเป็น UBO** ไม่ว่าจะมี effective ownership เท่าไร:
- ✅ Company X ถือหุ้น 25% → ไม่ใช่ UBO (เป็นบริษัท)
- ✅ Company Y ถือหุ้น 46% → ไม่ใช่ UBO (เป็นบริษัท)
- ✅ Foreign Company ถือหุ้น 30% → ไม่ใช่ UBO (เป็นบริษัท)

### 2. Companies That Cannot Be Drilled Down
**ไม่นับเป็น UBO** แม้จะไม่สามารถหาผู้ถือหุ้นต่อได้:
- บริษัทต่างประเทศ (Foreign Company) → ❌ Not UBO
- API Error (HTTP 500, timeout) → ❌ Not UBO
- Max Level Reached (Level 3) → ❌ Not UBO

**เหตุผล:** UBO ต้องเป็น **Person** เท่านั้น ตามนิยามของ BOT (Bank of Thailand)

---

## ✅ What IS a UBO

### Personal Shareholders with ≥15% Effective Ownership

**ตัวอย่าง:**

#### Case 1: Direct Shareholding
```
Main Company
    └─ Mr. John Doe: 20%
       → effective = 20%
       → ✅ UBO (Personal + ≥15%)
```

#### Case 2: Indirect Shareholding (Through 1 Company)
```
Main Company
    └─ Company A: 50%
        └─ Ms. Jane Smith: 40%
           → effective = 50% × 40% = 20%
           → ✅ UBO (Personal + ≥15%)
```

#### Case 3: Indirect Shareholding (Through 2 Companies)
```
Main Company
    └─ Company A: 80%
        └─ Company B: 60%
            └─ Mr. Bob Lee: 35%
               → effective = 80% × 60% × 35% = 16.8%
               → ✅ UBO (Personal + ≥15%)
```

#### Case 4: Multiple Paths (Aggregation)
```
Main Company
    ├─ Company A: 50%
    │   └─ Mr. X: 20% → effective = 50% × 20% = 10%
    └─ Company B: 30%
        └─ Mr. X: 30% → effective = 30% × 30% = 9%

Total for Mr. X = 10% + 9% = 19%
→ ✅ UBO (Personal + ≥15% after aggregation)
```

---

## 📋 Code Implementation

### Personal Shareholders Only

```python
if shareholder_type == 'personal':
    # ✅ เก็บใน UBO candidates
    if shareholder_name not in self.ubo_results:
        self.ubo_results[shareholder_name] = UBOCandidate(
            name=shareholder_name,
            total_percentage=0.0,
            paths=[],
            method=1,
            nationality=nationality,
            is_director=is_director
        )
    
    # บวก effective % เข้า candidate
    self.ubo_results[shareholder_name].total_percentage += effective_percentage
    self.ubo_results[shareholder_name].paths.append(path)

elif shareholder_type == 'corporate':
    # ❌ ไม่เก็บเป็น UBO candidate
    # แต่เพิ่มเข้า queue เพื่อหาผู้ถือหุ้นต่อ
    processing_queue.append((regis_id, effective_percentage, level + 1, path))
```

### Final UBO Identification

```python
def _identify_final_ubos(self) -> List[UBOCandidate]:
    """Filter UBO candidates - PERSONAL shareholders only with ≥15%"""
    final_ubos = []
    
    for candidate in self.ubo_results.values():
        if candidate.total_percentage >= 15.0:
            final_ubos.append(candidate)
            logger.info(f"UBO: {candidate.name} ({candidate.total_percentage:.2f}%)")
    
    return final_ubos
```

---

## 🎯 Summary

| Type | Effective % | Is UBO? | Reason |
|------|-------------|---------|---------|
| Personal | ≥ 15% | ✅ Yes | Meets criteria |
| Personal | < 15% | ❌ No | Below threshold |
| Corporate | ≥ 15% | ❌ No | Not a person |
| Corporate | < 15% | ❌ No | Not a person |
| Foreign Company | Any % | ❌ No | Not a person |

---

## 📚 References

**Bank of Thailand (BOT) Guidelines:**
- UBO = **Ultimate Beneficial Owner** (ผู้เป็นเจ้าของผลประโยชน์ที่แท้จริง)
- ต้องเป็น **บุคคลธรรมดา** (Natural Person)
- ไม่ใช่นิติบุคคล (Not a Legal Entity / Corporate Entity)

---

**Last Updated:** 2025-11-03 (Commit: Revert to personal-only UBO logic)

