# 🎮 SentinelAI - Quick Commands

## 🚀 Start/Stop Commands

### Backend
```bash
# Start backend (if not running)
cd backend
python -m app.main

# Or with virtual environment
cd backend
./venv/Scripts/python -m app.main

# Stop backend
# Press CTRL+C in the terminal
```

### Frontend
```bash
# Start frontend
cd sentinelai
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🧪 Testing Commands

### Backend Tests
```bash
cd backend

# Test text detection system
./venv/Scripts/python test_detection_system.py

# Test image detection system
./venv/Scripts/python test_image_detection.py

# Test API endpoints
./venv/Scripts/python test_api.py
```

### Quick API Tests
```bash
# Health check
curl http://localhost:8000/health

# Test text analysis
curl -X POST http://localhost:8000/api/analyze-text \
  -H "Content-Type: application/json" \
  -d '{"text": "URGENT: Your account has been suspended!"}'

# Test root endpoint
curl http://localhost:8000/
```

---

## 📦 Installation Commands

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
./venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Frontend Setup
```bash
cd sentinelai

# Install dependencies
npm install

# Or with yarn
yarn install
```

---

## 🔧 Maintenance Commands

### Update Dependencies
```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd sentinelai
npm update
```

### Check Versions
```bash
# Python version
python --version

# Node version
node --version

# npm version
npm --version

# Check installed packages
pip list  # Backend
npm list  # Frontend
```

### Clean Up
```bash
# Clean Python cache
cd backend
find . -type d -name "__pycache__" -exec rm -r {} +

# Clean node modules and reinstall
cd sentinelai
rm -rf node_modules
npm install

# Clean build files
rm -rf dist
```

---

## 🗄️ Database Commands

### Supabase Setup
```bash
# The database is already configured
# Connection details in backend/.env

# To reset database (if needed):
# 1. Go to Supabase dashboard
# 2. SQL Editor
# 3. Run schema from backend/database/schema.sql
```

---

## 📊 Monitoring Commands

### Check Backend Status
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check process
# Windows PowerShell:
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Check port 8000
Test-NetConnection -ComputerName localhost -Port 8000
```

### View Logs
```bash
# Backend logs are in the terminal where you started it
# Or check the process output

# Frontend logs
# Check browser console (F12)
```

---

## 🎯 Quick Start (Full Stack)

### Terminal 1 - Backend
```bash
cd backend
python -m app.main
```

### Terminal 2 - Frontend
```bash
cd sentinelai
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🧹 Troubleshooting Commands

### Port Already in Use
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Reset Everything
```bash
# Stop all processes
# CTRL+C in all terminals

# Backend - Reinstall
cd backend
rm -rf venv
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt

# Frontend - Reinstall
cd sentinelai
rm -rf node_modules
npm install
```

### Check Configuration
```bash
# View backend config
cd backend
cat .env

# View frontend config
cd sentinelai
cat .env
```

---

## 📝 Git Commands (If Using Version Control)

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "SentinelAI Phase 2 Complete"

# Create .gitignore
echo "node_modules/
venv/
__pycache__/
.env
*.pyc
dist/
.DS_Store" > .gitignore
```

---

## 🔍 Useful Checks

### Verify Installation
```bash
# Check Python packages
cd backend
./venv/Scripts/python -c "import fastapi, uvicorn, transformers, cv2, nltk; print('✅ All packages installed')"

# Check Node packages
cd sentinelai
npm list react vite tailwindcss
```

### Test AI Models
```bash
cd backend

# Test text detector
./venv/Scripts/python -c "from ai_models.text_detector import TextScamDetector; d = TextScamDetector(); print('✅ Text detector loaded')"

# Test image detector
./venv/Scripts/python -c "from ai_models.image_detector import ImageDeepfakeDetector; d = ImageDeepfakeDetector(); print('✅ Image detector loaded')"
```

---

## 📚 Documentation Commands

### View Documentation
```bash
# Open in browser
start PROJECT_STATUS.md  # Windows
open PROJECT_STATUS.md   # Mac
xdg-open PROJECT_STATUS.md  # Linux

# Or use your text editor
code PROJECT_STATUS.md  # VS Code
```

### Generate API Docs
```bash
# Backend API docs are auto-generated
# Access at: http://localhost:8000/docs
```

---

## 🎨 Development Commands

### Format Code
```bash
# Backend (if using black)
cd backend
black .

# Frontend (if using prettier)
cd sentinelai
npx prettier --write .
```

### Lint Code
```bash
# Backend (if using flake8)
cd backend
flake8 .

# Frontend (if using eslint)
cd sentinelai
npm run lint
```

---

## 🚀 Deployment Commands (Future)

### Build for Production
```bash
# Frontend
cd sentinelai
npm run build
# Output in dist/

# Backend
cd backend
# Already production-ready
# Just set DEBUG=False in .env
```

---

## 💡 Quick Tips

### Run Backend in Background (Windows)
```powershell
cd backend
Start-Process -NoNewWindow -FilePath "./venv/Scripts/python" -ArgumentList "-m", "app.main"
```

### Run Multiple Commands
```bash
# Run backend and frontend together (requires concurrently)
npm install -g concurrently
concurrently "cd backend && python -m app.main" "cd sentinelai && npm run dev"
```

### Create Shortcuts
```bash
# Add to package.json scripts:
"scripts": {
  "dev": "vite",
  "backend": "cd backend && python -m app.main",
  "test": "cd backend && python test_detection_system.py",
  "full": "concurrently \"npm run backend\" \"npm run dev\""
}
```

---

**Current Status:**
- ✅ Backend: RUNNING on port 8000
- ⏸️ Frontend: Ready to start with `npm run dev`

**Next Command:**
```bash
cd sentinelai
npm run dev
```
