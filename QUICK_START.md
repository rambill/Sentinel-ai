# SentinelAI - Quick Start Guide

Get up and running in 5 minutes!

## ⚡ Prerequisites

- Node.js 18+ installed
- Python 3.9+ installed
- Supabase account (free)

## 🚀 Quick Setup

### 1. Supabase (2 minutes)

1. Go to https://supabase.com → Create project
2. Copy **Project URL** and **anon key** from Settings → API
3. Enable Email auth in Authentication → Providers

### 2. Frontend (1 minute)

```bash
cd sentinelai
npm install
cp .env.example .env
# Edit .env with your Supabase credentials
npm run dev
```

Open: http://localhost:5173

### 3. Backend (2 minutes)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Open: http://localhost:8000

## ✅ Test It

1. Go to http://localhost:5173
2. Click "Sign up"
3. Create account
4. Login
5. Try "Text Analyzer" with: "URGENT: Click here now!"
6. Try "Image Detector" with any image

## 🎨 What You Get

- ✅ Modern authentication
- ✅ Interactive dashboard
- ✅ Text scam analyzer
- ✅ Fake image detector
- ✅ Premium UI/UX
- ✅ Responsive design
- ✅ Dark/light mode

## 📚 Need More Help?

- Full guide: `SETUP_GUIDE.md`
- Project details: `PROJECT_OVERVIEW.md`
- API docs: http://localhost:8000/docs

## 🐛 Common Issues

**"Module not found"**
```bash
npm install
```

**"Port already in use"**
```bash
# Kill process on port 5173 or 8000
```

**"Supabase error"**
- Check .env file
- Verify credentials
- Ensure project is active

## 🚀 Deploy

**Frontend**: Push to GitHub → Deploy on Vercel
**Backend**: Deploy on Railway or Render

That's it! You're ready to go! 🎉
