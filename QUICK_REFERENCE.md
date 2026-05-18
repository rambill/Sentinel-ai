# 🚀 SentinelAI Quick Reference

## Start Backend (Choose One)

```powershell
# Option 1: PowerShell Script
cd sentinelai/backend
./start.ps1

# Option 2: Direct Python
cd sentinelai/backend
./venv/Scripts/python.exe main.py

# Option 3: Activate venv first
cd sentinelai/backend
./venv/Scripts/Activate.ps1
python main.py
```

## Start Frontend

```bash
cd sentinelai
npm run dev
```

## Test Backend

```bash
# Run comprehensive test suite
cd sentinelai/backend
python test_real_ai.py

# Quick health check
curl http://localhost:8000/health

# Test text analysis
curl -X POST http://localhost:8000/api/analyze-text \
  -H "Content-Type: application/json" \
  -d '{"text": "URGENT! Click here now!"}'
```

## API Endpoints

- **Health**: `GET http://localhost:8000/health`
- **Text Analysis**: `POST http://localhost:8000/api/analyze-text`
- **Image Analysis**: `POST http://localhost:8000/api/analyze-image`
- **Statistics**: `GET http://localhost:8000/api/stats`

## Current Status

- ✅ **Phase 1**: Complete - Premium UI/UX
- ✅ **Phase 2**: Complete - Real AI (75-90% accuracy)
- 🔄 **Phase 3**: Next - Custom models (95%+ accuracy)

## Key Files

- `AI_INTEGRATION_SUCCESS.md` - Full AI integration details
- `PHASE_2_DEPLOYMENT_COMPLETE.md` - Deployment summary
- `backend/REAL_AI_SETUP.md` - Setup instructions
- `README.md` - Project overview

## Troubleshooting

**Backend won't start?**
```bash
cd sentinelai/backend
./venv/Scripts/python.exe -c "from ai_models.text_detector import TextScamDetector; print('OK')"
```

**Missing dependencies?**
```bash
cd sentinelai/backend
pip install -r requirements.txt
python -m textblob.download_corpora
```

**Frontend issues?**
```bash
cd sentinelai
npm install
npm run dev
```

## URLs

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Detection Capabilities

### Text (8 Methods)
- Urgency tactics
- Threat language
- Financial lures
- Suspicious URLs
- Grammar issues
- AI patterns
- Sentiment analysis
- Action requests

### Image (7 Methods)
- EXIF metadata
- Compression artifacts
- Noise patterns
- Edge detection
- Color distribution
- FFT analysis
- Face symmetry
