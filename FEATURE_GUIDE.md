# UBO System - New Features Guide

## 🎯 Quick Start

1. Run the application:
   ```bash
   python enhanced_app.py
   ```

2. Open browser: `http://localhost:4444`

3. Enter Company ID: `XXXXXXXX` (for mock data demo)

4. Click "Analyze UBO"

---

## 📊 Feature 1: UBO Calculation Details

### What You'll See:

**UBO Result Card:**
```
┌─────────────────────────────────────────────────────┐
│ 👑 UBO #1                                           │
│                                                     │
│ Name: WILLIAM ANDERSON                              │
│ Total Shareholding: 28.10%  [5 paths]              │
│ Identification Method: Method 1                     │
│ Nationality: American                               │
│ Director: Yes                                       │
│                                                     │
│ [🧮 View Calculation Details] ◄── Click here       │
└─────────────────────────────────────────────────────┘
```

**After Clicking "View Calculation Details":**
```
┌─────────────────────────────────────────────────────┐
│ UBO Calculation Details (All Paths):                │
│                                                     │
│ 1. Path 1: VENTURE CAPITAL PARTNERS →               │
│            GLOBAL INVESTMENT CORPORATION →          │
│            WILLIAM ANDERSON                         │
│    [76.2% × 18.5% × 22.5% = 3.171%]                │
│                                                     │
│ 2. Path 2: GLOBAL INVESTMENT CORPORATION →          │
│            WILLIAM ANDERSON                         │
│    [38.2% × 22.5% = 8.595%]                        │
│                                                     │
│ 3. Path 3: ASIA PACIFIC HOLDINGS LTD →             │
│            WILLIAM ANDERSON                         │
│    [42.1% × 18.8% = 7.914%]                        │
│                                                     │
│ 4. Path 4: PRIVATE EQUITY VENTURES →               │
│            NORTH AMERICAN FUND →                    │
│            WILLIAM ANDERSON                         │
│    [82.5% × 31.2% × 14.6% = 3.758%]               │
│                                                     │
│ 5. Path 5: EUROPEAN FINANCIAL GROUP →              │
│            WILLIAM ANDERSON                         │
│    [28.6% × 16.3% = 4.661%]                        │
│                                                     │
│ ╔══════════════════════════════════════════════╗   │
│ ║ Total UBO Effect:                            ║   │
│ ║ 3.171% + 8.595% + 7.914% + 3.758% + 4.661%  ║   │
│ ║ = 28.099%                                    ║   │
│ ╚══════════════════════════════════════════════╝   │
└─────────────────────────────────────────────────────┘
```

### 💡 Benefits:
- See exactly how UBO percentage is calculated
- Verify each path independently
- Understand the ownership structure depth
- Audit trail for compliance

---

## 🔍 Feature 2: Entity Filtering

### Location:
Look for the dropdown filters above the network visualization:

```
┌─────────────────────────────────────────────────────┐
│ Shareholding Network                                │
│                                                     │
│ 👤 Filter by Individual:  [-- All Individuals --] ▼│
│ 🏢 Filter by Company:     [-- All Companies --]   ▼│
│                                                     │
│ [All Levels] [Level 0-1] [Level 0-2] [Level 0-3]  │
│                                                     │
│ [Network Graph Visualization]                      │
└─────────────────────────────────────────────────────┘
```

### How to Use:

**Filter by Individual:**
1. Click "Filter by Individual" dropdown
2. Select a person (e.g., "WILLIAM ANDERSON")
3. Watch the graph highlight all paths related to this person
4. Select "-- All Individuals --" to clear

**Filter by Company:**
1. Click "Filter by Company" dropdown
2. Select a company (e.g., "GLOBAL INVESTMENT CORPORATION")
3. Watch the graph highlight all shareholders and connections
4. Select "-- All Companies --" to clear

### What Happens When You Filter:

**Before Filtering:**
```
All nodes visible at 100% opacity
All edges visible at default opacity
```

**After Selecting "WILLIAM ANDERSON":**
```
✅ William Anderson node: Orange border, emphasized
✅ Connected companies: Full brightness
✅ Related individuals: Full brightness  
✅ Connected paths: Blue or Red (if UBO), thicker
❌ Other nodes: 15% opacity, faded
❌ Other edges: 10% opacity, barely visible
```

### 💡 Benefits:
- Focus on specific entities
- Trace ownership paths visually
- Understand entity relationships
- Quick analysis without clutter

---

## 🔴 Feature 3: Red UBO Paths

### What You'll See:

The network graph now uses color coding for edges (lines):

| Color | Meaning | Appearance |
|-------|---------|------------|
| 🔴 Red | UBO Path (leads to UBO ≥15%) | Thick, high opacity |
| ⚪ Gray | Regular shareholding | Normal thickness, lower opacity |
| 🔵 Blue | Highlighted path (when filtering) | Thick, high opacity |

### Example Visualization:

```
              Main Company (Black ⚫)
                    |
        ┌──────────┼──────────┐
        │          │          │
     [RED]      [RED]      [GRAY]
        │          │          │
   Company A  Company B  Company C
    (Blue 🔵)  (Blue 🔵) (Blue 🔵)
        │          │          │
     [RED]      [RED]      [GRAY]
        │          │          │
    William    Sophia     John
   Anderson    Chen      Smith
   (Red 🔴)   (Red 🔴)  (Green 🟢)
    28.10%     22.18%     9.20%
    ✅ UBO     ✅ UBO     ❌ Not UBO
```

### Legend (shown in graph):
```
┌──────────────────────────┐
│ ⚫ Main Company          │
│ 🔵 Company               │
│ 🟢 Individual            │
│ 🔴 UBO ≥ 15%             │
│ ━━ UBO Path (Red line)   │
└──────────────────────────┘
```

### 💡 Benefits:
- Instantly identify critical ownership paths
- Focus compliance efforts on red paths
- Visual risk assessment
- Clear distinction between UBO and non-UBO relationships

---

## 🎨 Feature 4: Enhanced Path Highlighting

### Interactive Features:

**1. Hover Over Nodes:**
- Tooltip appears showing:
  - Full name
  - Type (Individual/Company)
  - Registration ID (if company)
  - Capital amount
  - UBO status
  - Level

**2. Drag Nodes:**
- Click and hold any node
- Drag to reposition
- Physics simulation adjusts other nodes
- Release to let it settle

**3. Level Filtering:**
- Click level buttons: [All Levels] [Level 0-1] [Level 0-2] [Level 0-3]
- Graph shows only selected levels
- Useful for step-by-step analysis

**4. Zoom and Pan:**
- Scroll to zoom in/out
- Click and drag background to pan
- Double-click to reset view (not implemented yet, but space for future)

---

## 📋 Complete Workflow Example

### Scenario: Analyzing William Anderson's Ownership

**Step 1: Initial Analysis**
1. Enter company ID and click Analyze
2. Scroll to UBO section
3. See William Anderson at 28.10% (UBO #1)

**Step 2: Verify Calculation**
1. Click "View Calculation Details" on William's card
2. Review all 5 paths
3. Verify: 3.171% + 8.595% + 7.914% + 3.758% + 4.661% = 28.099% ✅

**Step 3: Visual Analysis**
1. Scroll to Network Visualization
2. Notice red paths leading to William (he's marked with red 🔴)
3. Red paths indicate this is a UBO requiring attention

**Step 4: Filter View**
1. Select "WILLIAM ANDERSON" from "Filter by Individual"
2. Graph highlights only William's connections
3. See all 5 companies he has paths through
4. Notice some are Level 1, others Level 2

**Step 5: Investigate Specific Company**
1. Clear individual filter
2. Select "VENTURE CAPITAL PARTNERS" from company filter
3. See William owns 76.2% of this company
4. This company owns 18.5% of another company
5. That path contributes 3.171% to William's total

**Step 6: Documentation**
1. Screenshot the graph with highlights
2. Export the calculation details
3. Document findings for compliance

---

## 🎯 Use Cases

### 1. Compliance Officer
**Task:** Verify UBO calculations for regulatory filing

**Workflow:**
- Open UBO calculation details
- Take screenshots of each path
- Export to compliance report
- Use as audit trail

### 2. Risk Analyst
**Task:** Assess ownership complexity

**Workflow:**
- Count number of paths per UBO
- Check depth of ownership chains
- Identify circular ownership (if any)
- Use red paths to focus risk assessment

### 3. Due Diligence Team
**Task:** Understand beneficial ownership structure

**Workflow:**
- Filter by key individuals
- Trace their ownership paths
- Check for hidden relationships
- Verify against declarations

### 4. Legal Team
**Task:** Prepare ownership disclosure documents

**Workflow:**
- Use calculation details for precise figures
- Reference path details in legal docs
- Screenshot network for visual exhibits
- Verify threshold compliance

---

## 🐛 Troubleshooting

### Issue: Dropdown filters not showing entities
**Solution:** Wait for graph to fully load, then check Network Visualization section

### Issue: Graph looks cluttered
**Solution:** 
1. Use level filters to show fewer levels
2. Use entity filters to focus on specific entities
3. Zoom in on specific areas

### Issue: Can't see calculation details
**Solution:** Scroll to UBO section and click "View Calculation Details" button

### Issue: Red paths not visible
**Solution:** 
1. Ensure there are UBOs ≥15%
2. Zoom in to see line colors clearly
3. Check legend in graph corner

---

## 💡 Tips and Tricks

1. **Quick Entity Check:** Use dropdown filters to quickly see if an entity exists in the structure

2. **Path Counting:** Number of paths badge on UBO card shows ownership complexity

3. **Visual Scanning:** Red color instantly draws attention to UBO-related paths

4. **Audit Trail:** Screenshots of calculation details serve as verification documents

5. **Layer-by-Layer:** Use level filters (0-1, 0-2, 0-3) to understand structure progressively

6. **Comparison:** Compare path counts between UBOs to understand relative complexity

7. **Focus Mode:** Use filters + level selection together for precise analysis

---

## 📞 Support

For questions or issues:
- Check `UBO_ENHANCEMENT_SUMMARY.md` for technical details
- Review `UBO_LOGIC_CLARIFICATION.md` for algorithm explanation
- See `MOCK_DATA_USAGE.md` for testing instructions

---

## 🎉 What's New Summary

✅ **Calculation Transparency:** See exactly how percentages are computed
✅ **Entity Filtering:** Focus on specific individuals or companies  
✅ **Visual Indicators:** Red paths highlight UBO relationships
✅ **Interactive Analysis:** Click, filter, and explore dynamically

All features work together to provide a comprehensive UBO analysis experience!

