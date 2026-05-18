# SentinelAI - Complete Setup Guide

This guide will walk you through setting up the complete SentinelAI platform from scratch.

## 📋 Prerequisites

Before you begin, ensure you have:
- **Node.js 18+** and npm installed
- **Python 3.9+** installed
- A **Supabase account** (free tier works)
- A code editor (VS Code recommended)
- Terminal/Command Prompt access

## 🎯 Step 1: Supabase Setup

### 1.1 Create Supabase Project

1. Go to https://supabase.com and sign up/login
2. Click "New Project"
3. Fill in:
   - **Name**: SentinelAI
   - **Database Password**: (create a strong password)
   - **Region**: Choose closest to you
4. Click "Create new project" and wait for setup to complete

### 1.2 Get API Credentials

1. In your Supabase dashboard, go to **Settings** > **API**
2. Copy these values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon public** key (under "Project API keys")

### 1.3 Enable Email Authentication

1. Go to **Authentication** > **Providers**
2. Ensure **Email** is enabled
3. Configure email templates if desired (optional)

## 🚀 Step 2: Frontend Setup

### 2.1 Install Dependencies

```bash
cd sentinelai
npm install
```

This will install all required packages including:
- React, React Router, Framer Motion
- Tailwind CSS
- Supabase client
- Zustand, TanStack Query
- And more...

### 2.2 Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Supabase credentials:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
VITE_API_URL=http://localhost:8000
```

### 2.3 Start Development Server

```bash
npm run dev
```

The frontend will start at: **http://localhost:5173**

## 🐍 Step 3: Backend Setup

### 3.1 Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 3.2 Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn
- Pydantic
- Supabase Python client

### 3.4 Configure Backend Environment

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` (optional for Phase 1):
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_key
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 3.5 Start Backend Server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will start at: **http://localhost:8000**

## ✅ Step 4: Verify Installation

### 4.1 Check Backend

1. Open browser to: http://localhost:8000
2. You should see: `{"status": "online", "service": "SentinelAI API", ...}`
3. Visit API docs: http://localhost:8000/docs

### 4.2 Check Frontend

1. Open browser to: http://localhost:5173
2. You should see the SentinelAI landing page
3. Try clicking "Get Started" or "Sign In"

### 4.3 Test Authentication

1. Click "Sign up" on the landing page
2. Fill in:
   - Full Name
   - Email
   - Password (min 8 characters)
3. Click "Create Account"
4. Check your email for verification (Supabase sends this)
5. After verification, login with your credentials

### 4.4 Test Features

1. After login, you'll see the Dashboard
2. Try "Text Analyzer":
   - Paste: "URGENT: Your account has been suspended! Click here immediately to verify."
   - Click "Analyze Text"
   - Should detect as high-risk scam
3. Try "Image Detector":
   - Upload any image
   - Click "Analyze Image"
   - Will show mock analysis results

## 🎨 Step 5: Customization (Optional)

### 5.1 Change Theme Colors

Edit `sentinelai/tailwind.config.js`:
```javascript
colors: {
  cyber: {
    500: '#14b8a6', // Change this to your preferred color
  },
}
```

### 5.2 Update Branding

1. Replace logo in `src/components/layout/Sidebar.tsx`
2. Update app name in various components
3. Modify landing page content in `src/pages/Landing.tsx`

## 🐛 Troubleshooting

### Frontend Issues

**Problem: "Module not found" errors**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problem: Tailwind styles not working**
```bash
npm run dev
# Restart the dev server
```

**Problem: Supabase connection fails**
- Verify your `.env` file has correct credentials
- Check Supabase project is active
- Ensure no typos in URL or keys

### Backend Issues

**Problem: "Module not found" in Python**
```bash
pip install -r requirements.txt --force-reinstall
```

**Problem: Port 8000 already in use**
```bash
# Change port in backend/main.py:
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

**Problem: CORS errors**
- Check `CORS_ORIGINS` in backend `.env`
- Ensure frontend URL is included

## 📱 Step 6: Testing on Mobile

### 6.1 Find Your Local IP

**Windows:**
```bash
ipconfig
# Look for IPv4 Address
```

**macOS/Linux:**
```bash
ifconfig
# Look for inet address
```

### 6.2 Update Configuration

1. Update frontend `.env`:
```env
VITE_API_URL=http://YOUR_IP:8000
```

2. Start backend with:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Access from mobile: `http://YOUR_IP:5173`

## 🚀 Step 7: Production Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Go to https://vercel.com
3. Import your repository
4. Add environment variables in Vercel dashboard
5. Deploy!

### Backend (Railway)

1. Go to https://railway.app
2. Create new project from GitHub
3. Add environment variables
4. Deploy!

### Update Frontend API URL

After backend deployment, update frontend `.env`:
```env
VITE_API_URL=https://your-backend.railway.app
```

## 📚 Next Steps

Now that everything is set up:

1. **Explore the Dashboard** - Check out all the features
2. **Test Analysis Tools** - Try different text and images
3. **Customize Design** - Make it your own
4. **Add Real AI** - Integrate actual ML models (Phase 2)
5. **Deploy** - Share with the world!

## 🆘 Need Help?

- Check the main README.md
- Review API docs at http://localhost:8000/docs
- Check Supabase documentation
- Open an issue on GitHub

## 🎉 Success!

You now have a fully functional AI-powered scam detection platform running locally!

The platform includes:
- ✅ Modern authentication system
- ✅ Interactive dashboard
- ✅ Text scam analyzer
- ✅ Fake image detector
- ✅ Premium UI/UX
- ✅ Responsive design
- ✅ Dark/light mode

Happy coding! 🚀
