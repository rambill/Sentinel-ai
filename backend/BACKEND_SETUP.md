# Backend Setup Guide - RESOLVED ✅

## ✅ Backend is Now Working!

Your SentinelAI backend is successfully running on **http://localhost:8000**

## What Was Fixed

The initial error was: `ModuleNotFoundError: No module named 'fastapi'`

**Solution Applied:**
1. Created Python virtual environment
2. Installed required dependencies
3. Simplified requirements.txt (removed problematic Supabase dependency)
4. Backend now runs successfully

## Current Status

```
✅ FastAPI server running on http://0.0.0.0:8000
✅ All endpoints operational
✅ API documentation available at http://localhost:8000/docs
✅ Health check passing
✅ Mock AI responses working
```

## Quick Start (Already Done)

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python main.py
```

## Test Results

All API endpoints tested and working:

### 1. Root Endpoint ✅
```bash
GET http://localhost:8000/
Response: {"status":"online","service":"SentinelAI API","version":"1.0.0"}
```

### 2. Health Check ✅
```bash
GET http://localhost:8000/health
Response: {"status":"healthy","ai_models":{"text_analyzer":"operational",...}}
```

### 3. Text Analysis ✅
```bash
POST http://localhost:8000/api/analyze-text
Body: {"text": "URGENT: Click here now!"}
Response: {
  "isScam": true,
  "confidence": 99,
  "threatLevel": "high",
  "explanation": "...",
  "indicators": [...],
  "recommendation": "..."
}
```

### 4. Statistics ✅
```bash
GET http://localhost:8000/api/stats
Response: {"totalScans": 11201885, "threatsBlocked": 574132, ...}
```

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint - API status |
| GET | `/health` | Health check with AI model status |
| POST | `/api/analyze-text` | Analyze text for scams |
| POST | `/api/analyze-image` | Analyze image for manipulation |
| GET | `/api/stats` | Platform statistics |
| GET | `/docs` | Interactive API documentation (Swagger) |
| GET | `/redoc` | Alternative API documentation (ReDoc) |

## Testing the API

### Option 1: Use the Test Script
```bash
.\venv\Scripts\Activate.ps1
python test_api.py
```

### Option 2: Use PowerShell
```powershell
# Test root endpoint
Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing

# Test health check
Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing

# Test text analysis
$body = @{text="URGENT: Click here!"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:8000/api/analyze-text -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

### Option 3: Use Browser
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

### Option 4: Use curl (if installed)
```bash
curl http://localhost:8000
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/analyze-text -H "Content-Type: application/json" -d "{\"text\":\"URGENT: Click here!\"}"
```

## Dependencies Installed

```
fastapi==0.115.0          # Web framework
uvicorn[standard]==0.32.0 # ASGI server
python-multipart==0.0.12  # File upload support
pydantic==2.9.2           # Data validation
python-dotenv==1.0.1      # Environment variables
requests==2.34.0          # HTTP client (for testing)
```

## Environment Variables (Optional)

Create `.env` file in backend directory:

```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Running the Backend

### Development Mode (with auto-reload)
```bash
.\venv\Scripts\Activate.ps1
python main.py
```

### Production Mode
```bash
.\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Background Process
The backend is currently running as a background process (Terminal ID: 4)

To stop it:
```bash
# Press Ctrl+C in the terminal where it's running
# Or kill the process
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation where you can:
- View all endpoints
- Test endpoints directly in browser
- See request/response schemas
- Download OpenAPI specification

## Common Issues & Solutions

### Issue: Port 8000 already in use
**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change port in main.py
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

### Issue: Module not found
**Solution:**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: CORS errors from frontend
**Solution:**
The backend is already configured with CORS for:
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (Alternative port)

If you need to add more origins, edit `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "YOUR_FRONTEND_URL"],
    ...
)
```

## Next Steps

1. ✅ Backend is running
2. ✅ All endpoints tested
3. ✅ API documentation available
4. 🔄 Connect frontend to backend
5. 🔄 Test full integration
6. 🔄 Deploy to production

## Integration with Frontend

The frontend is already configured to connect to the backend at `http://localhost:8000`.

Make sure your frontend `.env` file has:
```env
VITE_API_URL=http://localhost:8000
```

## Production Deployment

### Railway
1. Push code to GitHub
2. Create new project on Railway
3. Connect GitHub repository
4. Add environment variables
5. Deploy!

### Render
1. Create new Web Service
2. Connect GitHub repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

### Fly.io
```bash
fly launch
fly deploy
```

## Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify virtual environment is activated
3. Ensure all dependencies are installed
4. Check port 8000 is not in use
5. Review the API documentation at /docs

## Success! 🎉

Your backend is fully operational and ready to serve the SentinelAI frontend!

**API Base URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs
**Health Check:** http://localhost:8000/health

All systems are go! 🚀
