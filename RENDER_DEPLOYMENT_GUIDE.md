# 🚀 Render Deployment Guide for SentinelAI

## Overview
This guide will help you deploy SentinelAI to Render with a live link.

**Deployment Strategy:**
- Backend: Python Web Service (FastAPI)
- Frontend: Static Site (React/Vite)
- Database: Supabase (already configured)

---

## 📋 Prerequisites

1. ✅ GitHub repository (already done)
2. ✅ Render account (sign up at https://render.com)
3. ✅ Supabase project (already configured)

---

## 🎯 Deployment Steps

### Step 1: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

---

### Step 2: Deploy Backend (FastAPI)

#### Option A: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Select "Sentinel-ai" repository
   - Click "Connect"

3. **Configure Backend Service**
   ```
   Name: sentinelai-backend
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_service_role_key
   SECRET_KEY=your_secret_key_here
   PYTHON_VERSION=3.10.0
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://sentinelai-backend.onrender.com`

---

### Step 3: Deploy Frontend (React/Vite)

1. **Create New Static Site**
   - Click "New +" → "Static Site"

2. **Connect Repository**
   - Select "Sentinel-ai" repository
   - Click "Connect"

3. **Configure Frontend Service**
   ```
   Name: sentinelai-frontend
   Branch: main
   Root Directory: (leave empty)
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

4. **Add Environment Variables**
   ```
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   VITE_API_URL=https://sentinelai-backend.onrender.com
   ```
   ⚠️ **Important:** Replace `sentinelai-backend` with your actual backend service name

5. **Deploy**
   - Click "Create Static Site"
   - Wait for deployment (3-5 minutes)
   - Your live link: `https://sentinelai-frontend.onrender.com`

---

### Step 4: Update CORS Settings

After deployment, update your backend CORS to include your frontend URL:

1. Go to backend service on Render
2. Click "Environment"
3. The CORS is already configured in `main.py` to accept Render domains

---

## 🔧 Configuration Files Created

### 1. `render.yaml` (Blueprint)
Automated deployment configuration for both services.

### 2. `backend/build.sh`
Build script for backend deployment.

### 3. Updated `backend/main.py`
- Added Render CORS origins
- Dynamic PORT configuration
- Production-ready settings

---

## 🌐 Your Live URLs

After deployment, you'll have:

- **Frontend:** `https://sentinelai-frontend.onrender.com`
- **Backend API:** `https://sentinelai-backend.onrender.com`
- **API Docs:** `https://sentinelai-backend.onrender.com/docs`
- **Health Check:** `https://sentinelai-backend.onrender.com/health`

---

## ⚙️ Environment Variables Reference

### Backend Environment Variables
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
SECRET_KEY=generate_a_random_secret_key
PYTHON_VERSION=3.10.0
```

### Frontend Environment Variables
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_API_URL=https://sentinelai-backend.onrender.com
```

---

## 🔍 Troubleshooting

### Backend Issues

**Problem:** Build fails
```bash
Solution: Check requirements.txt is in backend folder
Verify Python version is 3.10+
```

**Problem:** Service won't start
```bash
Solution: Check environment variables are set
Verify PORT is not hardcoded
Check logs in Render dashboard
```

**Problem:** CORS errors
```bash
Solution: Verify frontend URL is in CORS origins
Check VITE_API_URL matches backend URL
```

### Frontend Issues

**Problem:** Build fails
```bash
Solution: Check package.json is in root
Verify node version compatibility
Check build command: npm run build
```

**Problem:** API calls fail
```bash
Solution: Verify VITE_API_URL is correct
Check backend is deployed and running
Test backend health endpoint
```

**Problem:** Blank page
```bash
Solution: Check browser console for errors
Verify environment variables are set
Check dist folder is being published
```

---

## 📊 Free Tier Limits

### Render Free Plan
- ✅ 750 hours/month (enough for 1 service 24/7)
- ✅ Automatic SSL certificates
- ✅ Custom domains
- ⚠️ Services spin down after 15 min of inactivity
- ⚠️ Cold start: 30-60 seconds

### Tips for Free Tier
1. **Keep services active:** Use a service like UptimeRobot to ping your backend every 14 minutes
2. **Optimize cold starts:** Minimize dependencies
3. **Use caching:** Implement caching for frequently accessed data

---

## 🚀 Post-Deployment Steps

### 1. Test Your Deployment
```bash
# Test backend health
curl https://sentinelai-backend.onrender.com/health

# Test frontend
Open https://sentinelai-frontend.onrender.com in browser
```

### 2. Update GitHub README
Add your live links to README.md:
```markdown
## 🌐 Live Demo
- **Application:** https://sentinelai-frontend.onrender.com
- **API:** https://sentinelai-backend.onrender.com
- **API Docs:** https://sentinelai-backend.onrender.com/docs
```

### 3. Set Up Custom Domain (Optional)
1. Go to Render dashboard
2. Click on your service
3. Go to "Settings" → "Custom Domain"
4. Add your domain
5. Update DNS records

### 4. Monitor Your Services
- Check Render dashboard for logs
- Set up email notifications
- Monitor uptime and performance

---

## 🔄 Updating Your Deployment

### Automatic Deployment
Render automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Deployment
1. Go to Render dashboard
2. Click on your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

## 💰 Cost Optimization

### Free Tier Strategy
- Deploy backend on Render Free
- Deploy frontend on Render Free
- Use Supabase Free tier
- **Total Cost: $0/month**

### Upgrade Path (When Needed)
- **Starter Plan ($7/month):**
  - No cold starts
  - Always-on services
  - Better performance

---

## 📞 Support

### Render Support
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### SentinelAI Issues
- GitHub Issues: https://github.com/rambill/Sentinel-ai/issues

---

## ✅ Deployment Checklist

### Pre-Deployment
- [x] GitHub repository created
- [x] render.yaml configured
- [x] Environment variables prepared
- [x] CORS settings updated
- [x] Build scripts created

### Backend Deployment
- [ ] Create web service on Render
- [ ] Configure build and start commands
- [ ] Add environment variables
- [ ] Deploy and verify health endpoint
- [ ] Note backend URL

### Frontend Deployment
- [ ] Create static site on Render
- [ ] Configure build command
- [ ] Add environment variables (with backend URL)
- [ ] Deploy and verify site loads
- [ ] Test API connectivity

### Post-Deployment
- [ ] Test all features
- [ ] Update README with live links
- [ ] Set up monitoring
- [ ] Share your live link!

---

## 🎉 Success!

Once deployed, your SentinelAI will be live at:
**https://sentinelai-frontend.onrender.com**

Share it with the world! 🌍

---

**Need Help?** Open an issue on GitHub or check Render documentation.

**Last Updated:** 2024
