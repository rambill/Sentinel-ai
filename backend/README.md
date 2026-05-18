# SentinelAI Backend

FastAPI backend for the SentinelAI scam detection platform.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

4. Run the development server:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check with AI model status

### Analysis
- `POST /api/analyze-text` - Analyze text for scams
- `POST /api/analyze-image` - Analyze image for manipulation

### Statistics
- `GET /api/stats` - Get platform statistics

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment

For production, you would:
1. Integrate real AI models (BERT, Vision Transformers, etc.)
2. Add proper authentication middleware
3. Implement rate limiting
4. Add caching layer (Redis)
5. Set up proper logging and monitoring
6. Use production ASGI server (Gunicorn + Uvicorn)
7. Configure SSL/TLS
8. Set up database for storing analysis history

## Future AI Integration

Replace mock responses with:
- Text Analysis: BERT, RoBERTa, or GPT-based classifiers
- Image Analysis: Vision Transformers, CNN-based deepfake detectors
- Metadata Analysis: EXIF data validation
- Pattern Recognition: Custom trained models on scam datasets
