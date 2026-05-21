# 🔗 CONNECT FRONTEND TO BACKEND

## 🎉 GREAT NEWS!

Both services are deployed:
- ✅ **Frontend:** LIVE!
- ✅ **Backend:** LIVE!

**But they're not connected yet!**

---

## ⚠️ THE ISSUE

Your frontend is trying to connect to:
```
http://localhost:8000 ❌ (Your local computer)
```

But it should connect to:
```
https://sentinelai-backend-xxxx.onrender.com ✅ (Your deployed backend)
```

---

## ✅ THE SOLUTION

Update the `VITE_API_URL` environment variable in your Render frontend settings.

---

## 📋 STEP-BY-STEP FIX

### Step 1: Get Your Backend URL

1. Go to https://render.com/dashboard
2. Click on your **backend service** (sentinelai-backend)
3. Copy the URL at the top (looks like: `https://sentinelai-backend-xxxx.onrender.com`)

**Example:**
```
https://sentinelai-backend-abc123.onrender.com
```

### Step 2: Update Frontend Environment Variable

1. Go back to Render dashboard
2. Click on your **frontend service** (sentinelai-frontend)
3. Click **"Environment"** tab (left sidebar)
4. Find `VITE_API_URL` variable
5. Click **"Edit"**
6. Change value from:
   ```
   http://localhost:8000 ❌
   ```
   To:
   ```
   https://sentinelai-backend-xxxx.onrender.com ✅
   ```
   (Use YOUR actual backend URL!)
7. Click **"Save Changes"**

### Step 3: Redeploy Frontend

After changing environment variables, you need to redeploy:

1. Click **"Manual Deploy"** (top right)
2. Select **"Deploy latest commit"**
3. Wait 2-3 minutes

---

## 🎯 VISUAL GUIDE

### Where to Find Backend URL:

```
Render Dashboard
  └── sentinelai-backend
      └── URL shown at top: https://sentinelai-backend-xxxx.onrender.com
          └── Copy this! ✅
```

### Where to Update Frontend Environment:

```
Render Dashboard
  └── sentinelai-frontend
      └── Environment (left sidebar)
          └── Environment Variables
              └── VITE_API_URL
                  └── Edit
                      Old: http://localhost:8000
                      New: https://sentinelai-backend-xxxx.onrender.com
                      [Save Changes]
```

### After Saving:

```
Render Dashboard
  └── sentinelai-frontend
      └── [Manual Deploy] (top right)
          └── Deploy latest commit
              └── Wait 2-3 minutes
```

---

## 🧪 VERIFICATION

### Step 1: Test Backend Directly

Open in browser:
```
https://your-backend-url.onrender.com/health
```

**Should return:**
```json
{
  "status": "healthy",
  "ai_models": {
    "text_analyzer": "operational - REAL AI",
    "image_detector": "operational - REAL AI"
  }
}
```

### Step 2: Test Frontend Connection

After redeploying frontend:

1. Open your frontend URL
2. Go to "Analyze Text"
3. Enter: "Congratulations! You won $1000 from MTN"
4. Click "Analyze"
5. Should see results! ✅

---

## 📊 WHAT EACH SERVICE DOES

### Backend (Port 8000):
```
https://sentinelai-backend-xxxx.onrender.com
```
- Runs AI detection models
- Processes text and images
- Returns analysis results
- Handles authentication

### Frontend (Static Site):
```
https://sentinelai-frontend-xxxx.onrender.com
```
- User interface
- Sends requests to backend
- Displays results
- Handles user interactions

### Connection:
```
Frontend → VITE_API_URL → Backend
```

---

## ⏱️ TIMELINE

- **Now:** Update VITE_API_URL
- **+30 sec:** Save changes
- **+1 min:** Trigger manual deploy
- **+2-3 min:** Frontend rebuilds with new URL
- **+4 min:** Everything works! ✅

---

## 🚨 COMMON MISTAKES

### ❌ WRONG:
```
VITE_API_URL=http://localhost:8000
VITE_API_URL=localhost:8000
VITE_API_URL=sentinelai-backend.onrender.com
VITE_API_URL=https://sentinelai-backend.onrender.com/
```

### ✅ CORRECT:
```
VITE_API_URL=https://sentinelai-backend-xxxx.onrender.com
```

**Notes:**
- ✅ Must include `https://`
- ✅ No trailing slash `/`
- ✅ Use YOUR actual backend URL
- ✅ Must be exact URL from Render dashboard

---

## 💡 WHY THIS IS NEEDED

### During Development (Local):
```
Frontend: http://localhost:5173
Backend: http://localhost:8000
VITE_API_URL: http://localhost:8000 ✅
```

### In Production (Render):
```
Frontend: https://sentinelai-frontend-xxxx.onrender.com
Backend: https://sentinelai-backend-xxxx.onrender.com
VITE_API_URL: https://sentinelai-backend-xxxx.onrender.com ✅
```

**Environment variables tell frontend where to find backend!**

---

## 🔍 TROUBLESHOOTING

### "Still says backend not running"

**Check 1: Backend is actually running**
```
Visit: https://your-backend-url.onrender.com/health
Should return: {"status": "healthy"}
```

**Check 2: VITE_API_URL is correct**
```
Go to: Frontend → Environment → VITE_API_URL
Should be: https://your-backend-url.onrender.com
```

**Check 3: Frontend was redeployed**
```
After changing env vars, you MUST redeploy frontend
Environment changes don't apply until rebuild
```

### "CORS errors in browser console"

**Solution:** Already configured in backend!
```python
# backend/main.py already has:
allow_origins=[
    "https://*.onrender.com"  ✅
]
```

### "Backend URL not found"

**Check backend logs:**
```
Render Dashboard → sentinelai-backend → Logs
Look for: "Application startup complete"
```

---

## 📝 QUICK CHECKLIST

- [ ] Copy backend URL from Render dashboard
- [ ] Go to frontend service
- [ ] Click "Environment" tab
- [ ] Find `VITE_API_URL`
- [ ] Click "Edit"
- [ ] Paste backend URL (with https://, no trailing slash)
- [ ] Click "Save Changes"
- [ ] Click "Manual Deploy"
- [ ] Select "Deploy latest commit"
- [ ] Wait 2-3 minutes
- [ ] Test text analysis
- [ ] Test image analysis
- [ ] Celebrate! 🎉

---

## 🎉 AFTER SUCCESSFUL CONNECTION

### Your Live Platform:

**Frontend:**
```
https://sentinelai-frontend-xxxx.onrender.com
```

**Backend:**
```
https://sentinelai-backend-xxxx.onrender.com
```

### Features Working:
- ✅ Text scam detection
- ✅ Image deepfake detection
- ✅ User authentication
- ✅ Dashboard with metrics
- ✅ Dark/Light theme toggle
- ✅ Ugandan scam awareness
- ✅ Trust guidance system

---

## 🚀 ACTION REQUIRED NOW

**DO THIS RIGHT NOW:**

1. ✅ Go to https://render.com/dashboard
2. ✅ Click **sentinelai-backend**
3. ✅ **Copy the URL** at the top
4. ✅ Go back to dashboard
5. ✅ Click **sentinelai-frontend**
6. ✅ Click **"Environment"** tab
7. ✅ Edit **VITE_API_URL**
8. ✅ Paste your backend URL
9. ✅ Save changes
10. ✅ Click **"Manual Deploy"**
11. ✅ Wait 2-3 minutes
12. ✅ Test your app!

---

**You're SO close! Just connect the frontend to the backend and everything will work! 🚀**

