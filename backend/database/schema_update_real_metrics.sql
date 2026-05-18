-- SentinelAI Database Schema Update - Real Metrics
-- Add this to your existing database (run in Supabase SQL Editor)

-- Performance Metrics Table (for tracking response times)
CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    analysis_type VARCHAR(20) NOT NULL CHECK (analysis_type IN ('text', 'image')),
    response_time_ms INTEGER NOT NULL,
    success BOOLEAN NOT NULL DEFAULT true,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Daily Scan Summary Table (for scan frequency chart)
CREATE TABLE IF NOT EXISTS daily_scan_summary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    scan_date DATE NOT NULL,
    total_scans INTEGER DEFAULT 0,
    text_scans INTEGER DEFAULT 0,
    image_scans INTEGER DEFAULT 0,
    threats_detected INTEGER DEFAULT 0,
    high_risk_count INTEGER DEFAULT 0,
    medium_risk_count INTEGER DEFAULT 0,
    low_risk_count INTEGER DEFAULT 0,
    avg_confidence DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, scan_date)
);

-- System Health Table (for uptime tracking)
CREATE TABLE IF NOT EXISTS system_health (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('online', 'offline', 'degraded')),
    uptime_percentage DECIMAL(5,2) DEFAULT 100,
    last_check TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_performance_metrics_user_id ON performance_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_created_at ON performance_metrics(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_type ON performance_metrics(analysis_type);

CREATE INDEX IF NOT EXISTS idx_daily_scan_summary_user_id ON daily_scan_summary(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_scan_summary_date ON daily_scan_summary(scan_date DESC);
CREATE INDEX IF NOT EXISTS idx_daily_scan_summary_user_date ON daily_scan_summary(user_id, scan_date);

CREATE INDEX IF NOT EXISTS idx_system_health_service ON system_health(service_name);
CREATE INDEX IF NOT EXISTS idx_system_health_status ON system_health(status);

-- Row Level Security
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_scan_summary ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_health ENABLE ROW LEVEL SECURITY;

-- Performance Metrics Policies
CREATE POLICY "Users can view their own performance metrics"
    ON performance_metrics FOR SELECT
    USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "System can insert performance metrics"
    ON performance_metrics FOR INSERT
    WITH CHECK (true);

-- Daily Scan Summary Policies
CREATE POLICY "Users can view their own daily summaries"
    ON daily_scan_summary FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "System can insert daily summaries"
    ON daily_scan_summary FOR INSERT
    WITH CHECK (true);

CREATE POLICY "System can update daily summaries"
    ON daily_scan_summary FOR UPDATE
    USING (true);

-- System Health Policies (public read)
CREATE POLICY "Anyone can view system health"
    ON system_health FOR SELECT
    USING (true);

CREATE POLICY "System can manage health records"
    ON system_health FOR ALL
    USING (true);

-- Function to update daily scan summary
CREATE OR REPLACE FUNCTION update_daily_scan_summary()
RETURNS TRIGGER AS $$
DECLARE
    v_scan_date DATE := DATE(NEW.created_at);
    v_is_threat BOOLEAN;
    v_threat_level VARCHAR(20);
BEGIN
    -- Determine if it's a threat and threat level
    IF TG_TABLE_NAME = 'text_analyses' THEN
        v_is_threat := NEW.is_scam;
        v_threat_level := NEW.threat_level;
        
        -- Insert or update daily summary
        INSERT INTO daily_scan_summary (
            user_id, scan_date, total_scans, text_scans, threats_detected,
            high_risk_count, medium_risk_count, low_risk_count
        )
        VALUES (
            NEW.user_id, v_scan_date, 1, 1,
            CASE WHEN v_is_threat THEN 1 ELSE 0 END,
            CASE WHEN v_threat_level = 'high' THEN 1 ELSE 0 END,
            CASE WHEN v_threat_level = 'medium' THEN 1 ELSE 0 END,
            CASE WHEN v_threat_level = 'low' THEN 1 ELSE 0 END
        )
        ON CONFLICT (user_id, scan_date) DO UPDATE SET
            total_scans = daily_scan_summary.total_scans + 1,
            text_scans = daily_scan_summary.text_scans + 1,
            threats_detected = daily_scan_summary.threats_detected + CASE WHEN v_is_threat THEN 1 ELSE 0 END,
            high_risk_count = daily_scan_summary.high_risk_count + CASE WHEN v_threat_level = 'high' THEN 1 ELSE 0 END,
            medium_risk_count = daily_scan_summary.medium_risk_count + CASE WHEN v_threat_level = 'medium' THEN 1 ELSE 0 END,
            low_risk_count = daily_scan_summary.low_risk_count + CASE WHEN v_threat_level = 'low' THEN 1 ELSE 0 END,
            updated_at = NOW();
            
    ELSIF TG_TABLE_NAME = 'image_analyses' THEN
        v_is_threat := NEW.is_fake;
        v_threat_level := NEW.threat_level;
        
        -- Insert or update daily summary
        INSERT INTO daily_scan_summary (
            user_id, scan_date, total_scans, image_scans, threats_detected,
            high_risk_count, medium_risk_count, low_risk_count
        )
        VALUES (
            NEW.user_id, v_scan_date, 1, 1,
            CASE WHEN v_is_threat THEN 1 ELSE 0 END,
            CASE WHEN v_threat_level = 'high' THEN 1 ELSE 0 END,
            CASE WHEN v_threat_level = 'medium' THEN 1 ELSE 0 END,
            CASE WHEN v_threat_level = 'low' THEN 1 ELSE 0 END
        )
        ON CONFLICT (user_id, scan_date) DO UPDATE SET
            total_scans = daily_scan_summary.total_scans + 1,
            image_scans = daily_scan_summary.image_scans + 1,
            threats_detected = daily_scan_summary.threats_detected + CASE WHEN v_is_threat THEN 1 ELSE 0 END,
            high_risk_count = daily_scan_summary.high_risk_count + CASE WHEN v_threat_level = 'high' THEN 1 ELSE 0 END,
            medium_risk_count = daily_scan_summary.medium_risk_count + CASE WHEN v_threat_level = 'medium' THEN 1 ELSE 0 END,
            low_risk_count = daily_scan_summary.low_risk_count + CASE WHEN v_threat_level = 'low' THEN 1 ELSE 0 END,
            updated_at = NOW();
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for daily scan summary
CREATE TRIGGER update_text_daily_summary_trigger
    AFTER INSERT ON text_analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_daily_scan_summary();

CREATE TRIGGER update_image_daily_summary_trigger
    AFTER INSERT ON image_analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_daily_scan_summary();

-- Function to calculate average confidence
CREATE OR REPLACE FUNCTION calculate_avg_confidence(p_user_id UUID)
RETURNS DECIMAL AS $$
DECLARE
    v_avg_confidence DECIMAL(5,2);
BEGIN
    SELECT 
        COALESCE(
            (
                (SELECT COALESCE(AVG(confidence), 0) FROM text_analyses WHERE user_id = p_user_id) +
                (SELECT COALESCE(AVG(confidence), 0) FROM image_analyses WHERE user_id = p_user_id)
            ) / 2,
            0
        )
    INTO v_avg_confidence;
    
    -- Update user statistics
    UPDATE user_statistics 
    SET avg_confidence = v_avg_confidence, updated_at = NOW()
    WHERE user_id = p_user_id;
    
    RETURN v_avg_confidence;
END;
$$ LANGUAGE plpgsql;

-- Function to get scan frequency for last N days
CREATE OR REPLACE FUNCTION get_scan_frequency(p_user_id UUID, p_days INTEGER DEFAULT 7)
RETURNS TABLE(
    scan_date DATE,
    total_scans INTEGER,
    text_scans INTEGER,
    image_scans INTEGER,
    threats_detected INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.scan_date,
        COALESCE(dss.total_scans, 0) as total_scans,
        COALESCE(dss.text_scans, 0) as text_scans,
        COALESCE(dss.image_scans, 0) as image_scans,
        COALESCE(dss.threats_detected, 0) as threats_detected
    FROM (
        SELECT CURRENT_DATE - generate_series(0, p_days - 1) as scan_date
    ) d
    LEFT JOIN daily_scan_summary dss ON d.scan_date = dss.scan_date AND dss.user_id = p_user_id
    ORDER BY d.scan_date ASC;
END;
$$ LANGUAGE plpgsql;

-- Function to get average response time
CREATE OR REPLACE FUNCTION get_avg_response_time(p_user_id UUID DEFAULT NULL, p_hours INTEGER DEFAULT 24)
RETURNS TABLE(
    analysis_type VARCHAR(20),
    avg_response_time_ms DECIMAL,
    success_rate DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pm.analysis_type,
        ROUND(AVG(pm.response_time_ms)::DECIMAL, 2) as avg_response_time_ms,
        ROUND((COUNT(*) FILTER (WHERE pm.success = true)::DECIMAL / COUNT(*)::DECIMAL * 100), 2) as success_rate
    FROM performance_metrics pm
    WHERE 
        (p_user_id IS NULL OR pm.user_id = p_user_id)
        AND pm.created_at >= NOW() - (p_hours || ' hours')::INTERVAL
    GROUP BY pm.analysis_type;
END;
$$ LANGUAGE plpgsql;

-- Initialize system health records
INSERT INTO system_health (service_name, status, uptime_percentage)
VALUES 
    ('text_analysis', 'online', 100.0),
    ('image_analysis', 'online', 100.0),
    ('api', 'online', 100.0)
ON CONFLICT DO NOTHING;

-- View for easy dashboard queries
CREATE OR REPLACE VIEW user_dashboard_stats AS
SELECT 
    us.user_id,
    us.total_scans,
    us.text_scans,
    us.image_scans,
    us.threats_detected,
    us.high_risk_detections,
    us.medium_risk_detections,
    us.low_risk_detections,
    us.avg_confidence,
    us.security_score,
    us.last_scan_at,
    (SELECT COUNT(*) FROM text_analyses WHERE user_id = us.user_id AND created_at >= NOW() - INTERVAL '7 days') as text_scans_7d,
    (SELECT COUNT(*) FROM image_analyses WHERE user_id = us.user_id AND created_at >= NOW() - INTERVAL '7 days') as image_scans_7d,
    (SELECT COUNT(*) FROM text_analyses WHERE user_id = us.user_id AND is_scam = true AND created_at >= NOW() - INTERVAL '7 days') as threats_7d
FROM user_statistics us;

-- Grant permissions
GRANT SELECT ON user_dashboard_stats TO authenticated;

