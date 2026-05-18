-- SentinelAI Database Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Text Analyses Table
CREATE TABLE IF NOT EXISTS text_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    text_content TEXT NOT NULL,
    is_scam BOOLEAN NOT NULL,
    confidence DECIMAL(5,2) NOT NULL,
    threat_level VARCHAR(20) NOT NULL CHECK (threat_level IN ('low', 'medium', 'high')),
    explanation TEXT NOT NULL,
    indicators JSONB NOT NULL DEFAULT '[]',
    recommendation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Image Analyses Table
CREATE TABLE IF NOT EXISTS image_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    image_filename VARCHAR(255) NOT NULL,
    is_fake BOOLEAN NOT NULL,
    confidence DECIMAL(5,2) NOT NULL,
    threat_level VARCHAR(20) NOT NULL CHECK (threat_level IN ('low', 'medium', 'high')),
    explanation TEXT NOT NULL,
    manipulation_types JSONB NOT NULL DEFAULT '[]',
    recommendation TEXT NOT NULL,
    technical_details JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Statistics Table
CREATE TABLE IF NOT EXISTS user_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    total_scans INTEGER DEFAULT 0,
    text_scans INTEGER DEFAULT 0,
    image_scans INTEGER DEFAULT 0,
    threats_detected INTEGER DEFAULT 0,
    high_risk_detections INTEGER DEFAULT 0,
    medium_risk_detections INTEGER DEFAULT 0,
    low_risk_detections INTEGER DEFAULT 0,
    avg_confidence DECIMAL(5,2) DEFAULT 0,
    security_score INTEGER DEFAULT 100,
    last_scan_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_text_analyses_user_id ON text_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_text_analyses_created_at ON text_analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_text_analyses_threat_level ON text_analyses(threat_level);

CREATE INDEX IF NOT EXISTS idx_image_analyses_user_id ON image_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_image_analyses_created_at ON image_analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_image_analyses_threat_level ON image_analyses(threat_level);

CREATE INDEX IF NOT EXISTS idx_user_statistics_user_id ON user_statistics(user_id);

-- Row Level Security (RLS) Policies

-- Enable RLS
ALTER TABLE text_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE image_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_statistics ENABLE ROW LEVEL SECURITY;

-- Text Analyses Policies
CREATE POLICY "Users can view their own text analyses"
    ON text_analyses FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own text analyses"
    ON text_analyses FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own text analyses"
    ON text_analyses FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own text analyses"
    ON text_analyses FOR DELETE
    USING (auth.uid() = user_id);

-- Image Analyses Policies
CREATE POLICY "Users can view their own image analyses"
    ON image_analyses FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own image analyses"
    ON image_analyses FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own image analyses"
    ON image_analyses FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own image analyses"
    ON image_analyses FOR DELETE
    USING (auth.uid() = user_id);

-- User Statistics Policies
CREATE POLICY "Users can view their own statistics"
    ON user_statistics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own statistics"
    ON user_statistics FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own statistics"
    ON user_statistics FOR UPDATE
    USING (auth.uid() = user_id);

-- Function to update user statistics
CREATE OR REPLACE FUNCTION update_user_statistics()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert or update user statistics
    INSERT INTO user_statistics (user_id, total_scans, text_scans, threats_detected, last_scan_at)
    VALUES (
        NEW.user_id,
        1,
        1,
        CASE WHEN NEW.is_scam THEN 1 ELSE 0 END,
        NEW.created_at
    )
    ON CONFLICT (user_id) DO UPDATE SET
        total_scans = user_statistics.total_scans + 1,
        text_scans = user_statistics.text_scans + 1,
        threats_detected = user_statistics.threats_detected + CASE WHEN NEW.is_scam THEN 1 ELSE 0 END,
        high_risk_detections = user_statistics.high_risk_detections + CASE WHEN NEW.threat_level = 'high' THEN 1 ELSE 0 END,
        medium_risk_detections = user_statistics.medium_risk_detections + CASE WHEN NEW.threat_level = 'medium' THEN 1 ELSE 0 END,
        low_risk_detections = user_statistics.low_risk_detections + CASE WHEN NEW.threat_level = 'low' THEN 1 ELSE 0 END,
        last_scan_at = NEW.created_at,
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to update image statistics
CREATE OR REPLACE FUNCTION update_image_statistics()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert or update user statistics
    INSERT INTO user_statistics (user_id, total_scans, image_scans, threats_detected, last_scan_at)
    VALUES (
        NEW.user_id,
        1,
        1,
        CASE WHEN NEW.is_fake THEN 1 ELSE 0 END,
        NEW.created_at
    )
    ON CONFLICT (user_id) DO UPDATE SET
        total_scans = user_statistics.total_scans + 1,
        image_scans = user_statistics.image_scans + 1,
        threats_detected = user_statistics.threats_detected + CASE WHEN NEW.is_fake THEN 1 ELSE 0 END,
        high_risk_detections = user_statistics.high_risk_detections + CASE WHEN NEW.threat_level = 'high' THEN 1 ELSE 0 END,
        medium_risk_detections = user_statistics.medium_risk_detections + CASE WHEN NEW.threat_level = 'medium' THEN 1 ELSE 0 END,
        low_risk_detections = user_statistics.low_risk_detections + CASE WHEN NEW.threat_level = 'low' THEN 1 ELSE 0 END,
        last_scan_at = NEW.created_at,
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER update_text_statistics_trigger
    AFTER INSERT ON text_analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_user_statistics();

CREATE TRIGGER update_image_statistics_trigger
    AFTER INSERT ON image_analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_image_statistics();

-- Function to calculate security score
CREATE OR REPLACE FUNCTION calculate_security_score(p_user_id UUID)
RETURNS INTEGER AS $$
DECLARE
    v_score INTEGER := 100;
    v_stats RECORD;
BEGIN
    SELECT * INTO v_stats FROM user_statistics WHERE user_id = p_user_id;
    
    IF v_stats IS NULL THEN
        RETURN 100;
    END IF;
    
    -- Deduct points for high-risk detections
    v_score := v_score - (v_stats.high_risk_detections * 5);
    
    -- Deduct points for medium-risk detections
    v_score := v_score - (v_stats.medium_risk_detections * 2);
    
    -- Add points for regular scanning (up to 20 points)
    IF v_stats.total_scans > 0 THEN
        v_score := v_score + LEAST(v_stats.total_scans, 20);
    END IF;
    
    -- Ensure score is between 0 and 100
    v_score := GREATEST(0, LEAST(100, v_score));
    
    -- Update the security score
    UPDATE user_statistics SET security_score = v_score WHERE user_id = p_user_id;
    
    RETURN v_score;
END;
$$ LANGUAGE plpgsql;

-- Storage bucket for images (run this in Supabase Storage UI or via API)
-- CREATE BUCKET sentinel_images WITH (public = false);

-- Storage policies (run after creating bucket)
-- CREATE POLICY "Users can upload their own images"
--     ON storage.objects FOR INSERT
--     WITH CHECK (bucket_id = 'sentinel_images' AND auth.uid()::text = (storage.foldername(name))[1]);

-- CREATE POLICY "Users can view their own images"
--     ON storage.objects FOR SELECT
--     USING (bucket_id = 'sentinel_images' AND auth.uid()::text = (storage.foldername(name))[1]);

-- CREATE POLICY "Users can delete their own images"
--     ON storage.objects FOR DELETE
--     USING (bucket_id = 'sentinel_images' AND auth.uid()::text = (storage.foldername(name))[1]);
