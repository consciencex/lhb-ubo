# 🚀 Deployment Guide

## 🔐 Security First!

**⚠️ NEVER commit API keys to git!**

All sensitive data must be stored in:
- `.env` file (local development)
- Environment Variables (production)

---

## 📋 Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `ENLITE_API_KEY` | API key for Enlite service | `your_api_key_here` |
| `ENLITE_API_URL` | API endpoint URL | `https://enlite.lhb.co.th` |
| `ENLITE_API_TIMEOUT` | Request timeout (seconds) | `60` |

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Step 1: Clone repository
```bash
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo
```

### Step 2: Create .env file
```bash
cp env.example .env
# Edit .env and add your API key
nano .env
```

**.env content:**
```
ENLITE_API_KEY=your_actual_api_key_here
ENLITE_API_URL=https://enlite.lhb.co.th
ENLITE_API_TIMEOUT=60
```

### Step 3: Start container
```bash
docker-compose up -d
```

### Step 4: Access
```
http://localhost:4444
```

---

## 🖥️ Option 2: Direct Python (Windows/Linux)

### Step 1: Clone & Install
```bash
git clone https://github.com/consciencex/lhb-ubo.git
cd lhb-ubo
pip install -r requirements.txt
```

### Step 2: Create .env file
```bash
cp env.example .env
# Edit .env and add your API key
```

### Step 3: Run
```bash
python enhanced_app.py
```

---

## ☁️ Option 3: Vercel Deployment

### Step 1: Import project
1. Go to https://vercel.com
2. Import GitHub repository

### Step 2: Set Environment Variables
In Vercel Dashboard → Settings → Environment Variables:

| Key | Value |
|-----|-------|
| `ENLITE_API_KEY` | `your_api_key` |
| `ENLITE_API_URL` | `https://enlite.lhb.co.th` |
| `ENLITE_API_TIMEOUT` | `60` |

⚠️ **Note:** Vercel servers may not have access to internal APIs. See network requirements below.

---

## 🔒 Security Best Practices

### 1. Never commit secrets
- ✅ Use `.env` file (already in `.gitignore`)
- ✅ Use environment variables
- ❌ Never hardcode API keys in source code

### 2. Rotate API keys regularly
- Change API keys periodically
- Revoke compromised keys immediately

### 3. Limit network access
For Docker:
```yaml
ports:
  - "127.0.0.1:4444:4444"  # localhost only
```

### 4. Use HTTPS in production
- Deploy behind reverse proxy (nginx/traefik)
- Use SSL certificates

---

## 🌐 Network Requirements

The server must be able to reach:
- `https://enlite.lhb.co.th` (Production API)

**If deploying outside bank network:**
- API may be blocked by firewall
- Request IP whitelist from infrastructure team
- Or deploy on internal server with VPN access

---

## 📊 Project Structure

```
UBO/
├── app.py                  # Vercel entrypoint
├── enhanced_app.py         # Main Flask application
├── final_ubo_system.py     # Core UBO analysis logic
├── templates/
│   └── enhanced_index.html # Frontend UI
├── static/
│   ├── css/               # Stylesheets
│   └── locales/           # i18n translations
├── env.example            # Environment template
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker orchestration
├── requirements.txt       # Python dependencies
└── vercel.json           # Vercel configuration
```

---

## ❓ Troubleshooting

### "ENLITE_API_KEY not set"
- Create `.env` file from `env.example`
- Add your API key to `.env`

### API Connection Failed
- Check VPN/network connection
- Verify API endpoint is accessible
- Test with: `curl https://enlite.lhb.co.th`

### Docker build failed
```bash
docker-compose down --rmi all
docker-compose up -d --build
```

---

## 📞 Support

For assistance, contact the development team.
