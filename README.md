# 🏦 LH Bank UBO Analysis System

ระบบวิเคราะห์ผู้ได้รับผลประโยชน์ที่แท้จริง (Ultimate Beneficial Owner) ตามเอกสาร **NC958 PRO05-2568** ของธนาคารแห่งประเทศไทย

---

## ✨ คุณสมบัติหลัก

- 🔍 **3-Tier Analysis** - ตรวจสอบการถือหุ้น 3 ทอด (Level 1-3)
- 📊 **15% Threshold** - เกณฑ์ UBO ตาม NC958 PRO05-2568
- 🧮 **Effective Ownership Calculation** - คำนวณการถือหุ้นทางอ้อม (indirect)
- 🌐 **Web Interface** - UI สวยงามใช้งานง่าย
- 📈 **Interactive Tree Diagram** - แผนภูมิโครงสร้างการถือหุ้นแบบ interactive (D3.js)
- 🚀 **Vercel Deployment** - Deploy ready สำหรับ Vercel Pro

---

## 📁 โครงสร้างโปรเจค

```
UBO/
├── final_ubo_system.py      # Core UBO analysis logic
├── enhanced_app.py           # Main Flask application
├── vercel_app.py             # Vercel entry point (Flask app)
├── templates/
│   └── enhanced_index.html   # Frontend UI
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel configuration
├── .gitignore                # Git ignore rules
├── README.md                 # Documentation (this file)
└── [Reference Files]
    └── Enlite BOL API.postman_collection.json
```

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. (Optional) Set environment variables for custom API settings
export ENLITE_API_KEY="your-api-key-here"
export ENLITE_API_URL="https://xignal-uat.bol.co.th"
export ENLITE_API_TIMEOUT="60"

# 4. Run application
python3 enhanced_app.py

# 5. Open browser
# http://localhost:4444
```

**หมายเหตุ:** สำหรับ local development, default values จะถูกใช้ถ้าไม่ตั้งค่า environment variables

### Vercel Deployment

1. **Push to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

2. **Deploy to Vercel**
   - ไปที่ [vercel.com](https://vercel.com)
   - Import project จาก GitHub
   - Vercel จะ auto-detect configuration
   - คลิก "Deploy"

3. **Production URL**
   - `https://lhb-ubo.vercel.app` (หรือตามชื่อ project)

---

## 🔧 Configuration

### Vercel Settings

**Project Name:** `lhb-ubo`  
**Framework Preset:** `Flask` หรือ `Other`  
**Root Directory:** `./`  
**Install Command:** `pip install -r requirements.txt`  
**Build Command:** (empty)  
**Output Directory:** (empty)

### Environment Variables (Required)

ตั้งค่า Environment Variables ใน Vercel Dashboard:

#### ขั้นตอนการตั้งค่า:

1. **ไปที่ Vercel Dashboard**
   - Login: [https://vercel.com](https://vercel.com)
   - เลือก Project: `lhb-ubo`

2. **ไปที่ Settings → Environment Variables**
   - คลิกแท็บ **"Settings"**
   - คลิก **"Environment Variables"** ในเมนูด้านซ้าย

3. **เพิ่ม Variables:**
   - คลิก **"Add New"**
   - เพิ่ม variables ตามตารางด้านล่าง
   - เลือก Environment: **Production** ✅ (และ Preview, Development ถ้าต้องการ)
   - คลิก **"Save"**

#### Variables ที่ต้องตั้งค่า:

| Variable | Value | Environment | Required |
|----------|-------|-------------|----------|
| `ENLITE_API_KEY` | `HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV` | ✅ Production<br>✅ Preview | ✅ **Yes** |
| `ENLITE_API_URL` | `https://xignal-uat.bol.co.th` | ✅ Production<br>✅ Preview | Optional |
| `ENLITE_API_TIMEOUT` | `60` | ✅ Production<br>✅ Preview | Optional |

#### หลังตั้งค่า:

- ✅ **Redeploy** deployment ปัจจุบัน
- หรือรอ auto-deploy จาก commit ใหม่

**ดูคู่มือละเอียด:** `VERCEL_ENV_SETUP.md`

---

## 📊 การใช้งาน

### 1. วิเคราะห์บริษัท

1. เปิด Web Interface
2. ใส่ **Company Registration ID** (เช่น: `0107548000234`)
3. คลิก **"Analyze UBO"**
4. ดูผลการวิเคราะห์:
   - Company Information
   - Summary Statistics
   - UBO Analysis Results
   - Shareholding Structure (Tree Diagram)
   - Shareholder Details by Level

### 2. UBO Calculation

ระบบจะคำนวณ:
- **Direct Shareholding** - การถือหุ้นโดยตรง
- **Effective Ownership** - การถือหุ้นทางอ้อม (ผ่านหลายทอด)
- **UBO Threshold** - ≥15% ตาม NC958 PRO05-2568

**ตัวอย่าง:** `70.00% × 50.00% × 20.00% ⇒ 7.0000%`

---

## 🔍 UBO Analysis Logic

### Algorithm

1. **Level 1** - ตรวจสอบผู้ถือหุ้นโดยตรงของบริษัทหลัก
2. **Level 2** - ตรวจสอบผู้ถือหุ้นของบริษัทที่พบใน Level 1
3. **Level 3** - ตรวจสอบผู้ถือหุ้นของบริษัทที่พบใน Level 2

### UBO Identification

- ✅ **Yes UBO** - Effective ownership ≥15%
- ❌ **No UBO** - Effective ownership <15%

### Calculation Path

ระบบจะแสดง calculation path สำหรับแต่ละ shareholder:
```
Path 1: Company A (70%) → Company B (50%) → Person C (20%) = 70% × 50% × 20% ⇒ 7.00%
```

---

## 📈 Features

### Frontend

- **Responsive Design** - ใช้งานได้ทุกอุปกรณ์
- **Interactive Tree** - D3.js hierarchical tree visualization
- **Collapsible Sections** - Level 1, 2, 3 shareholder lists
- **UBO Calculation Details** - แสดงรายละเอียดการคำนวณ
- **English Output** - ทุก output เป็นภาษาอังกฤษ (ไม่มี encoding issues)

### Backend

- **Queue-based Processing** - ประมวลผลแบบ queue สำหรับ 3 levels
- **Circular Reference Detection** - ป้องกัน infinite loops
- **Error Handling** - จัดการ connection errors, timeouts
- **Data Sanitization** - ทำความสะอาดข้อมูล non-ASCII
- **API Caching** - Cache API responses เพื่อลด latency

---

## 🛠️ Technical Stack

- **Backend:** Python 3.9+, Flask
- **Frontend:** HTML5, Bootstrap 5, D3.js v7
- **API:** Enlite SOAP API (BOL)
- **Deployment:** Vercel (Pro tier)
- **Language:** Python, JavaScript

---

## ⚙️ Vercel Pro Configuration

```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 60,
      "memory": 3008
    },
    "vercel_app.py": {
      "maxDuration": 60,
      "memory": 3008
    }
  },
  "regions": ["sin1"]
}
```

**Features:**
- ⏱️ 60 seconds timeout (แทน 10 วินาที)
- 💾 3008 MB memory (แทน 1024 MB)
- 🌏 Singapore region (`sin1`) - Latency ต่ำสำหรับไทย

---

## 📝 API Endpoints

### `POST /api/analyze`

วิเคราะห์บริษัท UBO

**Request:**
```json
{
  "registration_id": "0107548000234"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "company_info": {...},
    "hierarchy_data": {...},
    "ubos": [...],
    "tree_structure": {...}
  }
}
```

### `GET /api/status`

ตรวจสอบสถานะระบบ

**Response:**
```json
{
  "status": "running",
  "ubo_system_initialized": true,
  "timestamp": "2025-10-30 21:00:00"
}
```

---

## 🔧 Development

### Project Structure

```
final_ubo_system.py    # Core analysis logic
├── FinalEnliteAPIClient     # API client
├── analyze_company_ubo()   # Main analysis function
└── UBOAnalysisResult        # Result dataclass

enhanced_app.py        # Flask application
├── /api/analyze       # Analysis endpoint
├── /api/status        # Status endpoint
└── /                  # Home page (serves template)

vercel_app.py         # Vercel entry point
api/index.py          # API serverless function
```

### Key Functions

#### `analyze_company_ubo(registration_id: str) -> UBOAnalysisResult`
- วิเคราะห์ UBO สำหรับบริษัทที่ระบุ
- Returns: UBOAnalysisResult with hierarchy, UBOs, risk level

#### `build_tree_structure(root_id, hierarchy, ubo_names) -> Dict`
- สร้าง tree structure สำหรับ D3.js visualization
- Returns: Nested dictionary สำหรับ rendering

---

## ⚠️ Troubleshooting

### Connection Error

**ปัญหา:** API connection failed  
**แก้ไข:**
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ตรวจสอบ VPN (ถ้ามี)
- API อาจตอบช้า (timeout 60 วินาที)

### Deployment Error

**ปัญหา:** Vercel deployment failed  
**แก้ไข:**
- ตรวจสอบ `vercel.json` ไม่มี syntax error
- ตรวจสอบ `requirements.txt` ครบถ้วน
- ตรวจสอบ build logs ใน Vercel Dashboard

### Function Timeout

**ปัญหา:** Function timeout on Vercel  
**แก้ไข:**
- ตรวจสอบว่า `maxDuration: 60` ใน `vercel.json`
- Vercel Pro tier รองรับถึง 60 วินาที ✅

---

## 📚 Reference Documents

- **NC958 PRO05-2568** - กระบวนการปฏิบัติงาน การระบุผู้ได้รับผลประโยชน์ที่แท้จริง UBO
- **Enlite BOL API** - API documentation (Postman collection)

---

## 📞 Support

สำหรับคำถามหรือการสนับสนุน:
- GitHub Issues: https://github.com/consciencex/lhb-ubo/issues
- Repository: https://github.com/consciencex/lhb-ubo

---

## 📄 License

Internal use - LH Bank

---

## 🎉 Status

✅ **Production Ready**  
✅ **Vercel Deployed**  
✅ **Documentation Complete**  
✅ **Code Optimized**

---

**ระบบพร้อมใช้งาน! 🚀**
