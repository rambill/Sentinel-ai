# Remove Mock Data - Implementation Guide

## Overview
This guide explains how to remove all mock data and implement real metrics tracking.

---

## Step 1: Update Database Schema ✅

**File:** `backend/database/schema_update_real_metrics.sql`

**Action:** Run this SQL script in your Supabase SQL Editor

This will create:
- `performance_metrics` table - Track response times
- `daily_scan_summary` table - Track daily scan frequency
- `system_health` table - Track system uptime
- Database functions for aggregating data
- Triggers to automatically update summaries

**Status:** ✅ SQL file created and ready to run

---

## Step 2: Update Backend Service ✅

**File:** `backend/app/services/analysis_service.py`

**Changes Made:**
- ✅ Added `track_performance()` method
- ✅ Added `get_scan_frequency()` method
- ✅ Added `get_performance_metrics()` method
- ✅ Added `get_system_health()` method
- ✅ Added `_update_avg_confidence()` helper

**Status:** ✅ Service updated

---

## Step 3: Update Backend Routes ✅

**File:** `backend/app/routes/analysis.py`

**Changes Made:**
- ✅ Added performance tracking to `/api/analyze-text`
- ✅ Added performance tracking to `/api/analyze-image`
- ✅ Added new endpoint: `/api/scan-frequency`
- ✅ Added new endpoint: `/api/performance`
- ✅ Added new endpoint: `/api/system-health`

**Status:** ✅ Routes updated

---

## Step 4: Update Frontend Dashboard ⏳

**File:** `src/pages/Dashboard.tsx`

**Changes Needed:**

### 4.1: Add State Variables

```typescript
// Add these after existing state
const [scanFrequency, setScanFrequency] = useState<any[]>([]);
const [avgResponseTime, setAvgResponseTime] = useState('0.0');
const [successRate, setSuccessRate] = useState('100.0');
const [systemUptime, setSystemUptime] = useState('100.0');
```

**Status:** ✅ Added

### 4.2: Update fetchDashboardData Function

Replace the current `fetchDashboardData` function with:

```typescript
const fetchDashboardData = async () => {
  try {
    // Fetch user statistics
    const statsResponse = await api.get('/api/statistics');
    setStatistics(statsResponse.data);

    // Fetch recent history
    const historyResponse = await api.get('/api/history?limit=5');
    setHistory(historyResponse.data.history || []);
    
    // Fetch scan frequency (last 7 days)
    const frequencyResponse = await api.get('/api/scan-frequency?days=7');
    const frequencyData = frequencyResponse.data.frequency || [];
    
    // Format for chart
    const formattedFrequency = frequencyData.map((day: any) => ({
      date: new Date(day.scan_date).toLocaleDateString('en-US', { weekday: 'short' }),
      scans: day.total_scans || 0,
      threats: day.threats_detected || 0,
    }));
    setScanFrequency(formattedFrequency);
    
    // Fetch performance metrics
    const perfResponse = await api.get('/api/performance?hours=24');
    const perfData = perfResponse.data.metrics || {};
    
    // Calculate average response time
    const textTime = perfData.text?.avg_response_time_ms || 0;
    const imageTime = perfData.image?.avg_response_time_ms || 0;
    const avgTime = textTime && imageTime ? (textTime + imageTime) / 2 : textTime || imageTime || 0;
    setAvgResponseTime((avgTime / 1000).toFixed(1)); // Convert to seconds
    
    // Calculate success rate
    const textSuccess = perfData.text?.success_rate || 100;
    const imageSuccess = perfData.image?.success_rate || 100;
    const avgSuccess = (textSuccess + imageSuccess) / 2;
    setSuccessRate(avgSuccess.toFixed(1));
    
    // Fetch system health
    const healthResponse = await api.get('/api/system-health');
    const healthData = healthResponse.data;
    setSystemUptime(healthData.uptime_percentage?.toFixed(1) || '100.0');
    
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    // Set defaults if API fails
    setStatistics({
      totalScans: 0,
      threatsDetected: 0,
      avgConfidence: 0,
      securityScore: 100,
    });
    setScanFrequency([]);
    setAvgResponseTime('0.0');
    setSuccessRate('100.0');
    setSystemUptime('100.0');
  } finally {
    setLoading(false);
  }
};
```

**Status:** ⏳ Needs manual update

### 4.3: Update Stats Display

Find this section (around line 70):

```typescript
const stats = [
  {
    label: 'Total Scans',
    value: statistics?.totalScans?.toString() || '0',
    change: '+12%',
    icon: <Activity className="w-5 h-5" />,
    color: 'cyber',
  },
  {
    label: 'Threats Blocked',
    value: statistics?.threatsDetected?.toString() || '0',
    change: '+5%',
    icon: <Shield className="w-5 h-5" />,
    color: 'danger',
  },
  {
    label: 'Avg Confidence',
    value: `${statistics?.avgConfidence?.toFixed(1) || '0'}%`,
    change: '+2.1%',
    icon: <TrendingUp className="w-5 h-5" />,
    color: 'success',
  },
  {
    label: 'Response Time',
    value: '1.2s',  // ← MOCK DATA
    change: '-0.3s',
    icon: <Zap className="w-5 h-5" />,
    color: 'primary',
  },
];
```

Replace with:

```typescript
const stats = [
  {
    label: 'Total Scans',
    value: statistics?.totalScans?.toString() || '0',
    change: statistics?.totalScans > 0 ? `+${statistics.totalScans}` : '0',
    icon: <Activity className="w-5 h-5" />,
    color: 'cyber',
  },
  {
    label: 'Threats Blocked',
    value: statistics?.threatsDetected?.toString() || '0',
    change: statistics?.threatsDetected > 0 ? `+${statistics.threatsDetected}` : '0',
    icon: <Shield className="w-5 h-5" />,
    color: 'danger',
  },
  {
    label: 'Avg Confidence',
    value: `${statistics?.avgConfidence?.toFixed(1) || '0'}%`,
    change: statistics?.avgConfidence > 0 ? `${statistics.avgConfidence.toFixed(1)}%` : '0%',
    icon: <TrendingUp className="w-5 h-5" />,
    color: 'success',
  },
  {
    label: 'Response Time',
    value: `${avgResponseTime}s`,  // ← REAL DATA
    change: avgResponseTime !== '0.0' ? `${avgResponseTime}s` : '0s',
    icon: <Zap className="w-5 h-5" />,
    color: 'primary',
  },
];
```

**Status:** ⏳ Needs manual update

### 4.4: Update Scan Frequency Chart

Find this section (around line 100):

```typescript
// Mock chart data - replace with real data from API
const threatDistribution = {
  high: statistics?.highRiskDetections || 0,
  medium: statistics?.mediumRiskDetections || 0,
  low: statistics?.lowRiskDetections || 0,
};

const scanFrequency = [  // ← MOCK DATA
  { date: 'Mon', scans: 35, threats: 5 },
  { date: 'Tue', scans: 42, threats: 8 },
  { date: 'Wed', scans: 38, threats: 6 },
  { date: 'Thu', scans: 51, threats: 12 },
  { date: 'Fri', scans: 45, threats: 9 },
  { date: 'Sat', scans: 28, threats: 4 },
  { date: 'Sun', scans: 22, threats: 2 },
];
```

Replace with:

```typescript
const threatDistribution = {
  high: statistics?.highRiskDetections || 0,
  medium: statistics?.mediumRiskDetections || 0,
  low: statistics?.lowRiskDetections || 0,
};

// scanFrequency is now loaded from API in fetchDashboardData
// Remove the mock data array
```

**Status:** ⏳ Needs manual update

### 4.5: Update Success Rate Display

Find this section (around line 250):

```typescript
<div className="text-center">
  <div className="text-2xl font-bold text-primary-400">99.2%</div>  {/* ← MOCK */}
  <div className="text-xs text-slate-400">Success Rate</div>
</div>
```

Replace with:

```typescript
<div className="text-center">
  <div className="text-2xl font-bold text-primary-400">{successRate}%</div>  {/* ← REAL */}
  <div className="text-xs text-slate-400">Success Rate</div>
</div>
```

**Status:** ⏳ Needs manual update

### 4.6: Update Uptime Display

Find this section (around line 300):

```typescript
<div className="text-right">
  <div className="text-2xl font-bold gradient-text">99.9%</div>  {/* ← MOCK */}
  <div className="text-xs text-slate-400">Uptime</div>
</div>
```

Replace with:

```typescript
<div className="text-right">
  <div className="text-2xl font-bold gradient-text">{systemUptime}%</div>  {/* ← REAL */}
  <div className="text-xs text-slate-400">Uptime</div>
</div>
```

**Status:** ⏳ Needs manual update

---

## Step 5: Testing

### 5.1: Run Database Migration

```bash
# Go to Supabase Dashboard → SQL Editor
# Copy and paste content from: backend/database/schema_update_real_metrics.sql
# Click "Run"
```

### 5.2: Restart Backend

```bash
cd sentinelai/backend
.\venv\Scripts\activate
python main.py
```

### 5.3: Test Endpoints

```bash
# Test scan frequency
curl http://localhost:8000/api/scan-frequency?days=7

# Test performance metrics
curl http://localhost:8000/api/performance?hours=24

# Test system health
curl http://localhost:8000/api/system-health
```

### 5.4: Test Frontend

1. Login to your account
2. Perform some analyses (text and images)
3. Go to Dashboard
4. Verify all data is real:
   - Total Scans should match your analyses
   - Response Time should show actual time
   - Scan Frequency chart should show your activity
   - Success Rate should be calculated
   - Uptime should be from database

---

## What Will Change

### Before (Mock Data)
```
Dashboard:
├─ Total Scans: 247 (mock)
├─ Threats: 18 (mock)
├─ Response Time: 1.2s (mock)
├─ Success Rate: 99.2% (mock)
├─ Uptime: 99.9% (mock)
└─ Scan Frequency: Mock 7-day data
```

### After (Real Data)
```
Dashboard:
├─ Total Scans: YOUR actual count
├─ Threats: YOUR actual threats
├─ Response Time: YOUR actual avg time
├─ Success Rate: YOUR actual success rate
├─ Uptime: SYSTEM actual uptime
└─ Scan Frequency: YOUR actual 7-day activity
```

---

## Summary of Changes

### Database ✅
- [x] Created `performance_metrics` table
- [x] Created `daily_scan_summary` table
- [x] Created `system_health` table
- [x] Added database functions
- [x] Added triggers

### Backend ✅
- [x] Updated `analysis_service.py`
- [x] Updated `analysis.py` routes
- [x] Added performance tracking
- [x] Added new endpoints

### Frontend ⏳
- [x] Added state variables
- [ ] Update `fetchDashboardData` function
- [ ] Update stats display
- [ ] Update scan frequency chart
- [ ] Update success rate display
- [ ] Update uptime display

---

## Quick Implementation Steps

1. **Run SQL Migration:**
   ```
   Supabase Dashboard → SQL Editor → Paste schema_update_real_metrics.sql → Run
   ```

2. **Restart Backend:**
   ```bash
   cd sentinelai/backend
   .\venv\Scripts\activate
   python main.py
   ```

3. **Update Dashboard.tsx:**
   - Copy the code snippets from sections 4.2-4.6 above
   - Replace the corresponding sections in your Dashboard.tsx file

4. **Test:**
   - Login
   - Perform analyses
   - Check dashboard shows real data

---

**Status:** Backend ✅ Complete | Frontend ⏳ Needs Manual Updates  
**Estimated Time:** 10-15 minutes to complete frontend updates  
**Last Updated:** May 13, 2026
