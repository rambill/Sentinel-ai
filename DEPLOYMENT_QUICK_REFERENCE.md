# 🎯 DEPLOYMENT QUICK REFERENCE CARD

Keep this handy while deploying! Copy-paste values as needed.

---

## 🔗 IMPORTANT LINKS

| Service | URL |
|---------|-----|
| Render Dashboard | https://render.com |
| GitHub Repo | https://github.com/rambill/Sentinel-ai |
| Supabase Dashboard | https://supabase.com/dashboard |

---

## ⚙️ BACKEND CONFIGURATION

### Service Settings
```
Name: sentinelai-backend
Region: Oregon (US West)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

### Environment Variables (Copy-Paste Ready)

**Variable 1:**
```
Name: SUPABASE_URL
Value: https://jsvmvkhomshqkzpbpozu.supabase.co
```

**Variable 2:**
```
Name: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impzdm12a2hvbXNocWt6cGJwb3p1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2MTM4OTMsImV4cCI6MjA5NDE4OTg5M30.aRQNKMoxPLfuvJgcKjMzHEEBYRwGn51ubiPfSazIQ84
```

**Variable 3:**
```
Name: SECRET_KEY
Value: sentinelai-production-secret-key-2024-secure-random-string
```

---

## 🌐 FRONTEND CONFIGURATION

### Service Settings
```
Name: sentinelai-frontend
Branch: main
Root Directory: (leave empty)
Build Command: npm install && npm run build
Publish Directory: dist
```

### Environment Variables (Copy-Paste Ready)

**Variable 1:**
```
Name: VITE_SUPABASE_URL
Value: https://jsvmvkhomshqkzpbpozu.supabase.co
```

**Variable 2:**
```
Name: VITE_SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impzdm12a2hvbXNocWt6cGJwb3p1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2MTM4OTMsImV4cCI6MjA5NDE4OTg5M30.aRQNKMoxPLfuvJgcKjMzHEEBYRwGn51ubiPfSazIQ84
```

**Variable 3:**
```
Name: VITE_API_URL
Value: [YOUR BACKEND URL FROM STEP 2]
```

⚠️ **IMPORTANT:** Replace `VITE_API_URL` with your actual backend URL!

Example: `https://sentinelai-backend-abc123.onrender.com`

---

## 📝 DEPLOYMENT ORDER

1. **Backend First** → Get backend URL
2. **Frontend Second** → Use backend URL in VITE_API_URL

---

## ✅ HEALTH CHECK ENDPOINTS

After deployment, test these:

| Endpoint | Expected Response |
|----------|-------------------|
| `[BACKEND_URL]/` | `{"status": "online"}` |
| `[BACKEND_URL]/health` | `{"status": "healthy"}` |
| `[BACKEND_URL]/docs` | Swagger UI page |
| `[FRONTEND_URL]` | Landing page |

---

## 🔍 COMMON ERRORS & FIXES

### Backend Build Fails
```
Error: "requirements.txt not found"
Fix: Set Root Directory to "backend"
```

### Backend Won't Start
```
Error: "Port already in use"
Fix: Use $PORT in start command (already configured)
```

### Frontend Build Fails
```
Error: "Cannot find module"
Fix: Check Build Command includes "npm install"
```

### Frontend Shows Blank Page
```
Error: "Failed to fetch"
Fix: Check VITE_API_URL is correct
Fix: Verify backend is running
```

### CORS Errors
```
Error: "CORS policy blocked"
Fix: Already configured - just wait for backend to fully start
```

---

## ⏱️ EXPECTED DEPLOYMENT TIMES

| Service | Build Time | Deploy Time | Total |
|---------|------------|-------------|-------|
| Backend | 3-5 min | 2-3 min | 5-10 min |
| Frontend | 2-3 min | 1-2 min | 3-5 min |
| **Total** | | | **10-15 min** |

---

## 🎯 TEST CASES

### Quick Smoke Test

**Text Analysis:**
```
Input: "Congratulations! You won $1000. Click here to claim your prize now!"
Expected: HIGH risk (70-90% confidence)
```

**Image Analysis:**
```
Input: Any photo from your phone
Expected: LOW-MEDIUM risk (20-50% confidence)
```

---

## 📊 YOUR DEPLOYMENT INFO

Fill this out as you deploy:

**Backend URL:**
```
https://_____________________________________.onrender.com
```

**Frontend URL:**
```
https://_____________________________________.onrender.com
```

**Deployment Date:**
```
_____________________
```

**Test Account:**
```
Email: _____________________
Password: _____________________
```

---

## 🚨 EMERGENCY CONTACTS

If something goes wrong:

1. **Check Render Logs:**
   - Click on service → "Logs" tab
   - Look for red error messages

2. **Check Browser Console:**
   - Press F12 → "Console" tab
   - Look for red errors

3. **Render Support:**
   - https://render.com/docs
   - https://community.render.com

4. **GitHub Issues:**
   - https://github.com/rambill/Sentinel-ai/issues

---

## 💡 PRO TIPS

1. **Copy-paste carefully** - One wrong character breaks everything
2. **Wait for builds** - Don't refresh or close browser
3. **Check logs first** - Most issues are visible in logs
4. **Test backend first** - Frontend depends on backend
5. **Use incognito mode** - Avoids cache issues when testing

---

## 🎉 SUCCESS INDICATORS

You'll know it's working when:

- ✅ Backend `/health` returns `{"status": "healthy"}`
- ✅ Frontend landing page loads with animations
- ✅ You can sign up and login
- ✅ Text analysis returns results
- ✅ Image analysis returns results
- ✅ Dashboard displays (may be empty initially)
- ✅ Theme toggle works (dark/light mode)

---

## 📱 SHARE YOUR SUCCESS

When deployed, share:

```
🎉 Just deployed SentinelAI - an AI-powered scam detection platform!

🔗 Try it: [YOUR_FRONTEND_URL]

Features:
✅ Deepfake detection
✅ Phishing detection
✅ AI-generated content detection
✅ Real-time analysis

Built with React, FastAPI, and real AI models!

#AI #Cybersecurity #WebDev
```

---

## 🔄 REDEPLOY INSTRUCTIONS

If you need to redeploy:

1. Make changes locally
2. Commit: `git add . && git commit -m "Update"`
3. Push: `git push origin main`
4. Render auto-deploys (2-5 min)

Or manually:
1. Go to Render dashboard
2. Click on service
3. Click "Manual Deploy" → "Deploy latest commit"

---

**Print this page or keep it open in a tab while deploying! 📄**

**Good luck! 🚀**

