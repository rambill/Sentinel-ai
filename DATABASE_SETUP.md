# 🗄️ Database Setup Guide

## Step 1: Get Your Supabase JWT Secret

1. Go to your Supabase project: https://supabase.com/dashboard/project/jsvmvkhomshqkzpbpozu
2. Click on **Settings** (gear icon) in the left sidebar
3. Click on **API**
4. Scroll down to **JWT Settings**
5. Copy the **JWT Secret** value
6. Update `sentinelai/backend/.env`:
   ```
   SUPABASE_JWT_SECRET=your-actual-jwt-secret-here
   ```

## Step 2: Run Database Schema

1. Go to your Supabase project
2. Click on **SQL Editor** in the left sidebar
3. Click **New Query**
4. Copy the entire contents of `sentinelai/backend/database/schema.sql`
5. Paste into the SQL editor
6. Click **Run** (or press Ctrl+Enter)
7. Wait for "Success. No rows returned" message

This will create:
- ✅ `text_analyses` table
- ✅ `image_analyses` table
- ✅ `user_statistics` table
- ✅ Indexes for performance
- ✅ Row Level Security (RLS) policies
- ✅ Triggers for auto-updating statistics
- ✅ Functions for security score calculation

## Step 3: Create Storage Bucket

1. In Supabase, click on **Storage** in the left sidebar
2. Click **New bucket**
3. Name: `sentinel_images`
4. **Public bucket**: ❌ NO (keep it private)
5. Click **Create bucket**

## Step 4: Set Storage Policies

1. Click on the `sentinel_images` bucket
2. Click on **Policies** tab
3. Click **New Policy**

### Policy 1: Upload Images
- **Policy name**: Users can upload their own images
- **Allowed operation**: INSERT
- **Target roles**: authenticated
- **USING expression**:
  ```sql
  bucket_id = 'sentinel_images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
  ```
- Click **Review** → **Save policy**

### Policy 2: View Images
- **Policy name**: Users can view their own images
- **Allowed operation**: SELECT
- **Target roles**: authenticated
- **USING expression**:
  ```sql
  bucket_id = 'sentinel_images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
  ```
- Click **Review** → **Save policy**

### Policy 3: Delete Images
- **Policy name**: Users can delete their own images
- **Allowed operation**: DELETE
- **Target roles**: authenticated
- **USING expression**:
  ```sql
  bucket_id = 'sentinel_images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
  ```
- Click **Review** → **Save policy**

## Step 5: Verify Setup

Run this SQL query to verify tables were created:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('text_analyses', 'image_analyses', 'user_statistics');
```

You should see 3 rows returned.

## Step 6: Test Database Connection

1. Make sure your `.env` file has the correct values:
   ```
   SUPABASE_URL=https://jsvmvkhomshqkzpbpozu.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_JWT_SECRET=your-actual-jwt-secret
   ```

2. Start the backend:
   ```bash
   cd sentinelai/backend
   python app/main.py
   ```

3. Check the logs for:
   ```
   Successfully connected to Supabase
   ```

## Step 7: Test with Frontend

1. Start frontend:
   ```bash
   cd sentinelai
   npm run dev
   ```

2. Login to the app
3. Analyze some text or image
4. Check Supabase dashboard:
   - Go to **Table Editor**
   - Click on `text_analyses` or `image_analyses`
   - You should see your analysis saved!

## Troubleshooting

### Error: "JWT Secret is invalid"
- Make sure you copied the JWT Secret from **Settings → API → JWT Settings**
- NOT the anon key or service key

### Error: "relation does not exist"
- Run the schema.sql again
- Make sure you're in the correct project

### Error: "permission denied for table"
- Check RLS policies are enabled
- Make sure you're logged in when testing

### Error: "bucket not found"
- Create the `sentinel_images` bucket
- Make sure it's set to private

## What's Next?

Once database is set up:
- ✅ All analyses will be saved automatically
- ✅ History will be available in dashboard
- ✅ Statistics will update in real-time
- ✅ Images will be stored securely
- ✅ Users can only see their own data

---

*Need help? Check the logs or contact support.*
