# SentinelAI - Real AI Installation Script
# This script installs all AI/ML dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SentinelAI - Real AI Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-Not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

Write-Host "📦 Installing AI/ML dependencies..." -ForegroundColor Cyan
Write-Host "This may take 5-10 minutes (~2GB download)" -ForegroundColor Yellow
Write-Host ""

# Install dependencies
pip install -r requirements.txt

Write-Host ""
Write-Host "📚 Downloading NLTK data..." -ForegroundColor Cyan
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); print('✅ NLTK data downloaded')"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Real AI models are now installed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start the backend: python main.py" -ForegroundColor White
Write-Host "2. Test the API: python test_api.py" -ForegroundColor White
Write-Host "3. Check docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Features now available:" -ForegroundColor Cyan
Write-Host "✅ Real phishing detection" -ForegroundColor Green
Write-Host "✅ Real deepfake detection" -ForegroundColor Green
Write-Host "✅ AI-generated text detection" -ForegroundColor Green
Write-Host "✅ Advanced image analysis" -ForegroundColor Green
Write-Host ""
