# 🛡️ SentinelAI - AI-Powered Scam Detection Platform

<div align="center">

![SentinelAI Logo](https://img.shields.io/badge/SentinelAI-Cybersecurity-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-2.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

**Protect yourself from AI-powered scams with cutting-edge detection technology**

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Tech Stack](#tech-stack)

</div>

---

## 📋 Overview

SentinelAI is a premium, enterprise-grade cybersecurity platform that uses advanced AI and machine learning to detect:
- 🎭 **Deepfakes** - AI-generated and manipulated images
- 📧 **Phishing** - Fraudulent messages and scam attempts
- 🤖 **AI-Generated Content** - Synthetic media detection
- 🇺🇬 **Local Scams** - Ugandan-specific fraud patterns (MTN, Airtel, etc.)

---

## ✨ Features

### 🔍 Text Analysis
- Real-time phishing detection
- Scam pattern recognition
- Urgency and manipulation detection
- Ugandan context awareness (MTN Money, Airtel Money, etc.)
- Confidence scoring with trust guidance

### 🖼️ Image Analysis
- Deepfake detection
- AI-generated image identification
- Photo manipulation detection
- EXIF data analysis
- Technical forensics

### 📊 Dashboard
- Real-time statistics
- Scan frequency charts
- Threat distribution analytics
- Performance metrics
- System health monitoring

### 🎨 Premium UI/UX
- **Dark Mode:** Futuristic cybersecurity aesthetic with minimal glow effects
- **Light Mode:** Clean, professional interface
- Smooth theme switching
- Glassmorphism effects
- Responsive design

---

## 🚀 Demo

### Dark Mode
![Dark Mode](https://via.placeholder.com/800x400/0B1120/3B82F6?text=Dark+Mode+Screenshot)

### Light Mode
![Light Mode](https://via.placeholder.com/800x400/F9FAFC/2563EB?text=Light+Mode+Screenshot)

---

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router** - Navigation
- **Zustand** - State management
- **React Hot Toast** - Notifications

### Backend
- **FastAPI** - High-performance Python framework
- **Uvicorn** - ASGI server
- **Supabase** - Authentication & Database
- **Python 3.10+** - Core language
- **Real AI Models** - Production-ready detection

### AI/ML
- Image analysis algorithms
- Text pattern recognition
- Deepfake detection
- Manipulation identification

---

## 📦 Installation

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.10+
- **Git**
- **Supabase Account** (for authentication)

### 1. Clone Repository
```bash
git clone https://github.com/rambill/Sentinel-ai.git
cd Sentinel-ai
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Add your Supabase credentials to .env
# VITE_SUPABASE_URL=your_supabase_url
# VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
# VITE_API_URL=http://localhost:8000
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your Supabase credentials to backend/.env
```

### 4. Database Setup
```bash
# Run the SQL migration in your Supabase dashboard
# File: backend/database/schema_update_real_metrics.sql
```

---

## 🚀 Usage

### Start Backend Server
```bash
cd backend
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

### Start Frontend
```bash
# In a new terminal
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### Access the Application
1. Open browser: http://localhost:5173
2. Sign up for a new account
3. Start analyzing text and images!

---

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints
- `POST /api/analyze-text` - Analyze text for scams
- `POST /api/analyze-image` - Analyze images for deepfakes
- `GET /api/statistics` - Get user statistics
- `GET /api/history` - Get analysis history
- `GET /api/health` - Health check

---

## 🎨 Color Palette

### Dark Mode - "Midnight Intelligence"
- Primary Background: `#0B1120`
- Secondary Background: `#111827`
- Accent Blue: `#3B82F6`
- Accent Purple: `#8B5CF6`
- Success: `#10B981`
- Danger: `#EF4444`

### Light Mode - "Clean Intelligence"
- Primary Background: `#F9FAFC`
- Secondary Background: `#FFFFFF`
- Accent Blue: `#2563EB`
- Accent Purple: `#7C3AED`
- Success: `#10B981`
- Danger: `#EF4444`

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Secure password hashing
- ✅ Environment variable protection
- ✅ CORS configuration
- ✅ Input validation
- ✅ Rate limiting ready
- ✅ SQL injection prevention

---

## 📊 Project Structure

```
sentinelai/
├── src/                      # Frontend source
│   ├── components/          # React components
│   ├── pages/              # Page components
│   ├── store/              # State management
│   ├── lib/                # Utilities
│   └── config/             # Configuration
├── backend/                 # Backend source
│   ├── app/                # FastAPI application
│   │   ├── ai/            # AI models
│   │   ├── routes/        # API routes
│   │   ├── middleware/    # Middleware
│   │   └── services/      # Business logic
│   ├── database/          # Database schemas
│   └── main.py            # Entry point
├── public/                 # Static assets
└── docs/                   # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@rambill](https://github.com/rambill)

---

## 🙏 Acknowledgments

- OpenAI for AI inspiration
- Stripe for design inspiration
- Linear for UI/UX patterns
- The open-source community

---

## 📞 Support

For support, email your-email@example.com or open an issue on GitHub.

---

## 🗺️ Roadmap

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Admin dashboard
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Mobile app
- [ ] Browser extension
- [ ] API for third-party integration

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by the SentinelAI Team

</div>
