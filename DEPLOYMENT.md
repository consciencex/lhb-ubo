# 🚀 Deployment Guide - Vercel

## ✅ Quick Start

### Deploy บน Vercel:
1. Push code to GitHub
2. Import project ที่ https://vercel.com
3. Set Environment Variables (ดูด้านล่าง)
4. Deploy!

---

## 🔐 Environment Variables

ตั้งค่าใน Vercel Dashboard → Settings → Environment Variables:

```
ENLITE_API_KEY = HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV
ENLITE_API_URL = https://xignal-uat.bol.co.th
ENLITE_API_TIMEOUT = 60
```

เลือก Environments: ✅ Production ✅ Preview ✅ Development

---

## 📋 Features

- ✅ Core UBO Analysis (3-tier hierarchy)
- ✅ D3.js Interactive Tree Visualization
- ✅ JSON Export
- ✅ CSV Export (Excel-compatible)
- ✅ Real-time API Integration
- ✅ English Output (no garbled text)

---

## 🛠️ Tech Stack

**Backend:**
- Flask 2.3+
- Python 3.10+
- Requests, lxml

**Frontend:**
- D3.js (tree visualization)
- Bootstrap 5
- Vanilla JavaScript

**Deployment:**
- Vercel (Serverless)
- Singapore region (sin1)

---

## 📊 Project Structure

```
UBO/
├── app.py                  # Flask entrypoint (Vercel auto-detect)
├── enhanced_app.py         # Main Flask application
├── final_ubo_system.py     # Core UBO analysis logic
├── templates/
│   └── enhanced_index.html # Frontend UI
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel configuration
└── README.md               # Documentation
```

---

## 🔄 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ENLITE_API_KEY=your_key_here
export ENLITE_API_URL=https://xignal-uat.bol.co.th
export ENLITE_API_TIMEOUT=60

# Run locally
python enhanced_app.py

# Access: http://localhost:4444
```

---

## 🚨 Troubleshooting

### Build Failed
- ตรวจสอบ environment variables
- ดู build logs ใน Vercel Dashboard

### API Errors
- ตรวจสอบ ENLITE_API_KEY ถูกต้อง
- ตรวจสอบ API endpoint accessible

### Size Limit
- Vercel limit: 250MB (serverless)
- Current size: ~50MB ✅

---

**Production URL:** https://lhb-ubo.vercel.app

