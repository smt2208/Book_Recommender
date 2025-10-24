# Deploying Book Recommender on Render

This guide will walk you through deploying your Book Recommender application on Render.

## Prerequisites

✅ GitHub repository with your code (already done: `smt2208/Book_Recommender`)  
✅ Trained model artifacts (model.pkl, book_name.pkl, final_ratings.pkl, book_matrix.pkl)  
✅ Render account (free tier available at https://render.com)

---

## Step 1: Update Requirements

Your `requirements.txt` already has the necessary dependencies. We just need to add Gunicorn (production WSGI server):

```txt
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2
scipy==1.11.4
flask==3.0.0
PyYAML
pydantic==2.5.0
gunicorn==21.2.0
```

---

## Step 2: Prepare Your Repository

### 2.1 Ensure Artifacts are Committed

⚠️ **IMPORTANT**: Your model files in `artifacts/` folder must be committed to GitHub:

```powershell
git add artifacts/model.pkl artifacts/book_name.pkl artifacts/final_ratings.pkl artifacts/book_matrix.pkl
git commit -m "Add trained model artifacts for deployment"
git push origin main
```

**Note**: If files are too large (>100MB), you'll need to use Git LFS or store them elsewhere (see Alternative below).

### 2.2 Check File Sizes

```powershell
Get-ChildItem -Path artifacts -Recurse | Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB, 2)}}
```

**If any file exceeds 100MB**, GitHub will reject it. Solutions:
- **Git LFS** (Large File Storage): https://git-lfs.github.com/
- **External Storage**: Use AWS S3, Google Cloud Storage, or Render Disks

---

## Step 3: Create Render Account

1. Go to https://render.com
2. Sign up using your GitHub account (recommended)
3. Authorize Render to access your repositories

---

## Step 4: Deploy on Render

### Method A: Using render.yaml (Recommended - Infrastructure as Code)

1. **Push render.yaml to GitHub**:
   ```powershell
   git add render.yaml
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Create Web Service on Render**:
   - Go to Render Dashboard: https://dashboard.render.com/
   - Click **"New +"** → **"Blueprint"**
   - Connect your `Book_Recommender` repository
   - Render will auto-detect `render.yaml`
   - Click **"Apply"**

### Method B: Manual Setup (Alternative)

1. **Create New Web Service**:
   - Go to Render Dashboard
   - Click **"New +"** → **"Web Service"**
   - Connect your `Book_Recommender` repository

2. **Configure Service**:
   - **Name**: `book-recommender` (or any name you prefer)
   - **Region**: Select closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or paid for better performance)

3. **Environment Variables** (Optional):
   - Add if you need custom configurations

4. **Click "Create Web Service"**

---

## Step 5: Monitor Deployment

1. Render will start building your application
2. You'll see logs in real-time:
   ```
   ==> Cloning from https://github.com/smt2208/Book_Recommender...
   ==> Downloading artifacts...
   ==> Running build command 'pip install -r requirements.txt'...
   ==> Build completed successfully
   ==> Starting service with 'gunicorn app:app'...
   ==> Service is live 🎉
   ```

3. Build typically takes **3-5 minutes** (longer if artifacts are large)

---

## Step 6: Access Your Application

Once deployed, Render provides a URL:
```
https://book-recommender-<random-id>.onrender.com
```

Test your application:
1. Visit the URL
2. Select a book from the dropdown
3. Click "Recommend Books"
4. Verify recommendations are working

---

## Troubleshooting

### Problem 1: Build Fails - "No module named 'gunicorn'"

**Solution**: Ensure `gunicorn` is in `requirements.txt`

### Problem 2: Application Crashes - "FileNotFoundError: artifacts/model.pkl"

**Solution**: Artifacts not committed to repository
```powershell
git add artifacts/
git commit -m "Add model artifacts"
git push origin main
```

### Problem 3: Files Too Large for GitHub

**Solution A - Git LFS**:
```powershell
# Install Git LFS
git lfs install

# Track large files
git lfs track "artifacts/*.pkl"
git add .gitattributes
git add artifacts/
git commit -m "Add large files with Git LFS"
git push origin main
```

**Solution B - Render Disks** (Paid):
- Use Render Persistent Disks to store model files
- Mount disk to your service
- Upload artifacts via SFTP

**Solution C - External Storage**:
- Upload artifacts to AWS S3/Google Cloud Storage
- Download in your app on startup:
  ```python
  import os
  import urllib.request
  
  if not os.path.exists('artifacts/model.pkl'):
      os.makedirs('artifacts', exist_ok=True)
      urllib.request.urlretrieve(
          'https://your-storage-url.com/model.pkl',
          'artifacts/model.pkl'
      )
  ```

### Problem 4: Slow First Load (Free Tier)

**Expected Behavior**: Render free tier spins down after 15 minutes of inactivity
- First request after inactivity takes **30-60 seconds** to spin up
- Subsequent requests are fast

**Solution**: Upgrade to paid tier ($7/month) for always-on service

### Problem 5: Memory Errors

**Solution**: Your model artifacts are loaded into memory
- Free tier has 512MB RAM
- If your artifacts exceed this, upgrade to paid tier (1GB+ RAM)

---

## Performance Optimization

### 1. Reduce Artifact Size

Consider compressing your pickle files:
```python
import pickle
import gzip

# Save compressed
with gzip.open('artifacts/model.pkl.gz', 'wb') as f:
    pickle.dump(model, f)

# Load compressed
with gzip.open('artifacts/model.pkl.gz', 'rb') as f:
    model = pickle.load(f)
```

### 2. Enable Gunicorn Workers

Update `render.yaml`:
```yaml
startCommand: "gunicorn app:app --workers 2 --threads 2"
```

### 3. Add Health Check Endpoint

Add to `app.py`:
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

Configure in Render:
- Health Check Path: `/health`

---

## Cost Breakdown

| Plan | Price | RAM | Features |
|------|-------|-----|----------|
| Free | $0 | 512MB | Spins down after 15min inactivity |
| Starter | $7/month | 1GB | Always on, custom domain |
| Standard | $25/month | 2GB | Auto-scaling, priority support |

---

## Alternative Deployment Options

### Option 1: Docker Deployment on Render

If you recreate your Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
```

Deploy as Docker service on Render.

### Option 2: Other Platforms

- **Railway**: Similar to Render, GitHub integration
- **Heroku**: Classic PaaS (more expensive)
- **AWS Elastic Beanstalk**: More complex, more control
- **Google Cloud Run**: Serverless, pay per request
- **Azure App Service**: Enterprise-ready

---

## Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] All 742 books appear in dropdown
- [ ] Recommendations work for sample books
- [ ] No errors in Render logs
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled (automatic on Render)
- [ ] Environment variables set (if needed)
- [ ] Monitoring/alerts configured

---

## Continuous Deployment

Render automatically redeploys when you push to `main`:

```powershell
# Make changes
git add .
git commit -m "Update recommendation algorithm"
git push origin main

# Render detects changes and redeploys automatically
```

---

## Getting Help

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Your Logs**: Check Render dashboard for detailed error logs

---

## Summary

**Quick Start** (if artifacts < 100MB):
```powershell
# 1. Add gunicorn to requirements.txt
# 2. Commit everything
git add .
git commit -m "Prepare for Render deployment"
git push origin main

# 3. Go to render.com, create account
# 4. New Web Service → Connect Book_Recommender repo
# 5. Build Command: pip install -r requirements.txt
# 6. Start Command: gunicorn app:app
# 7. Deploy!
```

Your app will be live in 5 minutes! 🚀
