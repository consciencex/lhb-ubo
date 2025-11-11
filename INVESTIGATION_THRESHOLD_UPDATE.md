# Investigation Companies - 15% Threshold Update

## Date: November 11, 2025
## Status: ✅ Implemented

---

## 🎯 New Logic: Investigation Only for ≥15% Companies

### Requirement:
```
Companies Requiring Investigation ต้องมีเงื่อนไข 2 ข้อ:
1. ไม่มีข้อมูลผู้ถือหุ้น (API ไม่สามารถหาข้อมูลได้)
2. มี effective shareholding ≥ 15%

ถ้า < 15% ไม่ต้อง investigate (ไม่ถึง UBO threshold อยู่แล้ว)
```

---

## 🔍 Logic Comparison

### ❌ Before (Wrong):

```javascript
// เงื่อนไข: Company ไม่มี shareholders
if (shareholders.length === 0) {
    // Mark as investigation
}
```

**Problem:**
- แม้ shareholding < 15% ก็ยัง investigate
- ไม่มีความจำเป็นต้องหา UBO (ต่ำกว่า threshold)
- Waste effort on irrelevant companies

**Example (Wrong):**
```
Company X: 8% shareholding
- No shareholder data
❌ Marked as "Investigation Required"
✗ ไม่จำเป็น! (8% < 15%)
```

---

### ✅ After (Correct):

```javascript
// เงื่อนไข: Company ไม่มี shareholders AND >= 15%
const effectivePercent = parseFloat(company.parent_percentage || 0);

if (shareholders.length === 0 && effectivePercent >= 15.0) {
    // Mark as investigation
}
```

**Correct:**
- เฉพาะ companies ที่ ≥ 15%
- สำคัญพอที่ต้องหา UBO
- Focus on relevant companies

**Example (Correct):**
```
Company A: 22.5% shareholding
- No shareholder data
✅ Marked as "Investigation Required"
✓ จำเป็น! (22.5% ≥ 15%)

Company B: 8% shareholding
- No shareholder data
✅ NOT marked
✓ ไม่จำเป็น (8% < 15%)
```

---

## 📊 Detection Logic Flow

```
For each company in hierarchy:
    │
    ├─ Is level 1 or 2? ──┐
    │   NO → Skip         │
    │   YES               │
    │   └─ Has shareholders? ──┐
    │       YES → Skip          │
    │       NO                  │
    │       └─ Effective % ≥ 15%? ──┐
    │           NO → Skip              │
    │           YES                    │
    │           └─ ADD to investigation list ✅
```

---

## 🎨 Visual Indicators Updated

### Investigation Company Card:

```
┌──────────────────────────────────────────────────────────┐
│ 🏢 HD00071701                                            │
│    [Level 2] [22.50% Shareholding] ← Shows percentage   │
│                                                          │
│ Company ID: HD00071701                                   │
│ ⚠️ No shareholder data available                        │
│                                                          │
│ ℹ️ Action Required: This company holds ≥15% but API    │
│    could not retrieve shareholder data. This may be a   │
│    foreign company or institution.                       │
│    Manual verification required to identify UBO.         │
└──────────────────────────────────────────────────────────┘
```

**New Element:**
- `[22.50% Shareholding]` - Warning badge showing percentage
- Explains WHY investigation is needed (≥15%)

---

## 🔧 Code Changes

### Frontend Detection (Display):

```javascript
const effectivePercent = parseFloat(company.parent_percentage || 0);

// Check: NO shareholders AND >= 15%
if (shareholders.length === 0 && effectivePercent >= 15.0) {
    investigationCompanies.push({
        name: company.display_name,
        company_id: company.company_id,
        level: level,
        effective_percent: effectivePercent  // ✅ Store percentage
    });
}
```

### Network Graph Detection:

```javascript
// Calculate effective percentage from hierarchy
const nodeEffectivePercent = new Map();
Object.entries(hierarchyData).forEach(([compId, compData]) => {
    const effectivePercent = parseFloat(compData.parent_percentage || 0);
    nodeEffectivePercent.set(compId, effectivePercent);
});

// Check: NO children AND >= 15%
const effectivePercent = nodeEffectivePercent.get(node.id) || 0;

if (!hasAnyChildren && effectivePercent >= 15.0) {
    investigationNodeIds.add(node.id); // ✅ Mark with deep blue
}
```

### Display Update:

```html
<span class="badge bg-warning">${effectivePercent.toFixed(2)}% Shareholding</span>

<p>This company holds ≥15% but API could not retrieve shareholder data.</p>
```

---

## 📋 Examples

### Example 1: Investigation Required ✅

```
Company: GLOBAL INVESTMENT CORPORATION
Level: 1
Effective Shareholding: 22.50%
Shareholders: 0 (API failed)

Decision: ✅ INVESTIGATE
Reason: 22.50% ≥ 15% → Could be UBO path
Action: Manual verification required
```

### Example 2: Investigation NOT Required ❌

```
Company: SMALL HOLDINGS LLC
Level: 2
Effective Shareholding: 8.30%
Shareholders: 0 (API failed)

Decision: ❌ DON'T INVESTIGATE
Reason: 8.30% < 15% → Not UBO material
Action: No action needed
```

### Example 3: Has Data ❌

```
Company: ASIA PACIFIC HOLDINGS
Level: 1
Effective Shareholding: 18.75%
Shareholders: 6 (API success)

Decision: ❌ DON'T INVESTIGATE
Reason: Has shareholder data
Action: Normal processing
```

---

## 🎯 Decision Matrix

| Shareholding | Has Data | Investigation? | Reason |
|--------------|----------|----------------|--------|
| ≥ 15% | ❌ No | ✅ YES | Could be UBO path |
| ≥ 15% | ✅ Yes | ❌ NO | Has data |
| < 15% | ❌ No | ❌ NO | Below UBO threshold |
| < 15% | ✅ Yes | ❌ NO | Below threshold + has data |

---

## 💡 Benefits

### Before Fix:
- ❌ Investigated companies with < 15%
- ❌ Wasted compliance effort
- ❌ False positives
- ❌ Unclear why investigation needed

### After Fix:
- ✅ Only investigate ≥ 15% companies
- ✅ Focus on UBO-relevant companies
- ✅ No false positives
- ✅ Clear percentage shown
- ✅ Efficient compliance workflow

---

## 🔴 Network Graph Visual

### Investigation Node (≥15%, No Data):
```
Node:
  Color: 🔷 Deep Blue (#1e40af)
  Border: 🟠 Orange (#f59e0b), 3px
  No outgoing lines

Tooltip:
  ⚠️ Requires Investigation
  Shareholding: 22.50%
```

### Regular Node (< 15%, No Data):
```
Node:
  Color: 🔵 Regular Blue (#3b82f6)
  Border: ⚪ White, 2px
  No special marking

Tooltip:
  Normal display
```

---

## 🧪 Testing

### Test Case 1: Company ≥ 15%, No Data

```bash
Expected:
- ✅ Listed in "Companies Requiring Investigation"
- ✅ Shows percentage badge (e.g., "22.50% Shareholding")
- ✅ Deep blue color in graph
- ✅ Orange border
- ✅ Message: "holds ≥15% but API could not retrieve data"
```

### Test Case 2: Company < 15%, No Data

```bash
Expected:
- ✅ NOT listed in investigation section
- ✅ Regular blue color in graph
- ✅ No special marking
- ✅ No investigation needed
```

### Test Case 3: Company ≥ 15%, Has Data

```bash
Expected:
- ✅ NOT listed in investigation section
- ✅ Regular processing
- ✅ Shareholders shown in table
```

---

## 📝 Real Data Example

### For Company ID: 0107548000234

```
Potential Investigation Companies:

HD00071701:
- Level: 2
- Effective %: Check from API
- Has shareholders?: Check from API
- If ≥ 15% AND no data → Investigation ✅
- If < 15% → Skip ❌
```

---

## 🎯 Compliance Impact

### Investigation Workflow:

**Step 1: Check Investigation Section**
```
Companies listed here:
- All have ≥ 15% shareholding
- All are missing shareholder data
- All require manual verification
```

**Step 2: Prioritize by Percentage**
```
Sort by effective percentage (highest first):
1. Company A: 45.2% → High priority
2. Company B: 28.6% → Medium priority
3. Company C: 16.3% → Low priority (but still >15%)
```

**Step 3: Manual Verification**
```
For each company:
1. Verify company registration
2. Contact company for shareholder list
3. Check alternative databases
4. Document findings
```

---

## ✅ Summary

**Change:** Added ≥15% threshold for investigation companies

**Impact:** 
- Reduced false positives
- Focus on UBO-relevant companies
- Clear percentage display
- Better compliance efficiency

**Files Modified:**
- `templates/enhanced_index.html` (~30 lines)

**Testing:**
- ✅ No linter errors
- ✅ Logic verified
- ✅ Display updated

---

**Status:** ✅ Investigation logic now only flags companies with ≥15% shareholding that lack data!

**Benefit:** Compliance teams can focus on truly important companies that could affect UBO determination. 🎯

