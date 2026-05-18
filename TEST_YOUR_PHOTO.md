# 📸 Test Your Phone Photo

## Quick Test (30 seconds)

### 1. Make Sure Backend is Running
```bash
cd backend
python -m app.main
```
You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`

### 2. Open Frontend
- Go to: http://localhost:5173
- Click "Analyze Image" in the sidebar

### 3. Upload Your Photo
- Click "Choose File" or drag & drop
- Select a photo from your phone
- Click "Analyze Image"

### 4. Check Results

#### ✅ GOOD (Expected for Real Photos):
- **Confidence:** 20-50%
- **Threat Level:** LOW or MEDIUM
- **Is Fake:** No
- **Indicators:** Minimal or "No manipulation artifacts detected"

#### ❌ BAD (Should NOT happen for real photos):
- **Confidence:** 70%+
- **Threat Level:** HIGH
- **Is Fake:** Yes

---

## What Different Photos Should Show

| Photo Type | Expected Confidence | Expected Threat | Is Fake |
|------------|-------------------|-----------------|---------|
| **Phone selfie** | 20-35% | LOW | No |
| **Landscape photo** | 20-30% | LOW | No |
| **Indoor photo** | 25-40% | LOW-MEDIUM | No |
| **Screenshot** | 40-55% | MEDIUM | No |
| **Instagram filtered** | 45-60% | MEDIUM | Maybe |
| **Heavily edited** | 55-75% | MEDIUM-HIGH | Maybe |
| **AI-generated** | 70-95% | HIGH | Yes |
| **Deepfake** | 75-95% | HIGH | Yes |

---

## If You Still See HIGH Risk on Real Photos

### Check These Details:
1. **What's the exact confidence?** (e.g., 72%, 85%)
2. **What indicators are shown?** (e.g., "metadata inconsistencies")
3. **What type of photo?** (selfie, landscape, screenshot)
4. **Was it edited?** (cropped, filtered, adjusted)
5. **What app took it?** (Camera, Instagram, Snapchat)

### Common Reasons for Higher Scores:
- **Screenshot:** May show MEDIUM (40-55%) - normal
- **Instagram/Snapchat:** Filters add artifacts - may show MEDIUM
- **Heavily cropped:** May show MEDIUM
- **Very old photo:** Compression artifacts - may show MEDIUM
- **Downloaded from web:** May have been re-saved - may show MEDIUM

### What Should Definitely Be LOW:
- Fresh photo from phone camera app
- No filters or edits
- Taken in last few days
- Good lighting

---

## Example Test Results

### ✅ Real Phone Photo (Good)
```
Confidence: 28%
Threat Level: LOW
Is Fake: No
Explanation: This image appears authentic with 72% confidence. 
Analysis shows natural patterns consistent with genuine photography.
Indicators:
  ✅ Natural compression patterns
  ✅ Consistent metadata
  ✅ Authentic noise distribution
  ✅ No manipulation artifacts detected
```

### ⚠️ Edited Photo (Expected)
```
Confidence: 58%
Threat Level: MEDIUM
Is Fake: No
Explanation: This image appears authentic with 42% confidence.
Some minor inconsistencies detected but likely from normal editing.
Indicators:
  ⚠️ Metadata inconsistencies or editing software traces
  ✅ Natural compression patterns
```

### ❌ AI-Generated (Good Detection)
```
Confidence: 87%
Threat Level: HIGH
Is Fake: Yes
Explanation: Our AI has detected signs of digital manipulation 
with 87% confidence. Analysis revealed unnatural noise patterns, 
frequency domain anomalies.
Indicators:
  ⚠️ Unnatural noise patterns (AI generation indicator)
  ⚠️ Frequency domain anomalies (AI generation marker)
  ⚠️ Edge artifacts and sharp transitions detected
```

---

## Troubleshooting

### Backend Not Running?
```bash
cd backend
python -m app.main
```

### Frontend Not Loading?
```bash
npm run dev
```

### Image Upload Fails?
- Check file size (max 10MB)
- Check file type (JPG, PNG, WebP)
- Check browser console for errors

### Still Shows HIGH Risk?
1. Read `IMAGE_DETECTION_FIX.md` for details
2. Share the exact confidence score
3. Share the indicators shown
4. Describe the photo type

---

## Quick Comparison Test

### Test 1: Your Phone Photo
- Upload a recent photo from your phone
- **Expected:** LOW risk (20-35%)

### Test 2: AI-Generated Image
- Go to: https://thispersondoesnotexist.com
- Download the AI face
- Upload to SentinelAI
- **Expected:** HIGH risk (75-95%)

### Test 3: Screenshot
- Take a screenshot of your desktop
- Upload to SentinelAI
- **Expected:** MEDIUM risk (40-55%)

---

## Summary

✅ **Real photos should show LOW to MEDIUM risk**  
✅ **Confidence should be 20-50% for authentic photos**  
✅ **Only AI-generated or heavily manipulated should show HIGH**  

**If your phone photo shows LOW or MEDIUM risk, the system is working correctly!** 🎉

---

**Need help?** Check `IMAGE_DETECTION_FIX.md` for technical details.
