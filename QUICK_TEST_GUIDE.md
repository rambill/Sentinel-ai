# 🚀 Quick Test Guide - SentinelAI

## ⚡ 30-Second Test

### 1. Copy This Message:
```
URGENT: Your bank account has been suspended due to suspicious activity! Click here immediately to verify your identity: http://bit.ly/verify-now or your account will be permanently closed within 24 hours. Enter your credit card details to confirm.
```

### 2. Test It:
- Open: http://localhost:5173 (frontend)
- Go to: "Analyze Text" page
- Paste the message
- Click "Analyze Message"

### 3. Expected Result:
- ✅ **Confidence:** 99%
- ✅ **Threat Level:** HIGH
- ✅ **Indicators:** Urgency, threats, financial, suspicious URL
- ✅ **Recommendation:** Do NOT click, delete immediately

---

## 📊 Quick Test Results

| Test Type | Message | Expected Confidence | Expected Threat |
|-----------|---------|-------------------|-----------------|
| **Phishing** | Bank suspension + URL | 90-99% | HIGH |
| **Scam** | Lottery winner + wire transfer | 90-99% | HIGH |
| **Impersonation** | PayPal + suspicious link | 90-99% | HIGH |
| **Marketing** | Limited time offer | 60-75% | MEDIUM |
| **Legitimate** | Professional email | 15-25% | LOW |

---

## 🎯 3 Must-Try Tests

### Test 1: HIGH RISK (Phishing)
```
URGENT: Your bank account has been suspended due to suspicious activity! Click here immediately to verify your identity: http://bit.ly/verify-now or your account will be permanently closed within 24 hours.
```
**Expected:** 99% confidence, HIGH risk

### Test 2: MEDIUM RISK (Marketing)
```
Limited time offer! Get 50% off your next purchase. Click here to claim your discount before it expires. Don't miss out!
```
**Expected:** 60-75% confidence, MEDIUM risk

### Test 3: LOW RISK (Legitimate)
```
Hi John, thanks for your email yesterday. I've reviewed the project proposal and it looks great. Let's schedule a meeting next week to discuss the timeline.
```
**Expected:** 15-25% confidence, LOW risk

---

## 🔧 Troubleshooting

### Backend Not Running?
```bash
cd backend
python -m app.main
```

### Frontend Not Running?
```bash
npm run dev
```

### Run Full Test Suite:
```bash
cd backend
./venv/Scripts/python test_detection_system.py
```

---

## 📈 What to Look For

### ✅ Good Results:
- High-risk scams: 70%+ confidence
- Medium-risk: 40-69% confidence
- Low-risk legitimate: <40% confidence
- Relevant indicators shown
- Clear recommendations

### ❌ Issues:
- All messages showing same confidence
- No indicators displayed
- API errors in console
- Backend not responding

---

## 💡 Pro Tips

1. **Test with real scam emails** from your spam folder
2. **Try ChatGPT-generated text** to see AI detection
3. **Test with URLs** to see URL analysis
4. **Mix legitimate + scam elements** to test edge cases
5. **Check the explanation** to understand why it's flagged

---

## 📚 More Test Messages

See `TEST_MESSAGES.txt` for 20+ comprehensive test cases!

---

## ✅ Success Criteria

Your system is working if:
- ✅ Phishing messages show 90%+ confidence
- ✅ Legitimate messages show <30% confidence
- ✅ Indicators are relevant and accurate
- ✅ Explanations make sense
- ✅ Recommendations are appropriate

---

**Status:** ✅ System Verified and Production-Ready!
