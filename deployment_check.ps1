# PowerShell Deployment Preparation Script for Render
# Run this script before deploying to Render

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Book Recommender - Render Deployment Check" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if artifacts exist
Write-Host "1. Checking artifacts..." -ForegroundColor Yellow
if (Test-Path "artifacts") {
    Write-Host "   ✓ artifacts/ folder exists" -ForegroundColor Green
    
    $requiredFiles = @("model.pkl", "book_name.pkl", "final_ratings.pkl", "book_matrix.pkl")
    $allExist = $true
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path "artifacts\$file")) {
            Write-Host "   ✗ Missing: $file" -ForegroundColor Red
            $allExist = $false
        }
    }
    
    if ($allExist) {
        Write-Host "   ✓ All required .pkl files found" -ForegroundColor Green
        
        # Check file sizes
        Write-Host ""
        Write-Host "2. Artifact file sizes:" -ForegroundColor Yellow
        Get-ChildItem -Path "artifacts\*.pkl" | ForEach-Object {
            $sizeMB = [math]::Round($_.Length / 1MB, 2)
            $status = if ($sizeMB -lt 100) { "✓" } else { "✗ TOO LARGE" }
            Write-Host "   $status $($_.Name): $sizeMB MB" -ForegroundColor $(if ($sizeMB -lt 100) { "Green" } else { "Red" })
        }
    } else {
        Write-Host "   ✗ Please run: python main.py to train the model" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ✗ artifacts/ folder not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "3. Checking requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "   ✓ requirements.txt exists" -ForegroundColor Green
    
    $content = Get-Content "requirements.txt" -Raw
    if ($content -match "gunicorn") {
        Write-Host "   ✓ gunicorn is included" -ForegroundColor Green
    } else {
        Write-Host "   ✗ gunicorn not found in requirements.txt" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ✗ requirements.txt not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "4. Checking render.yaml..." -ForegroundColor Yellow
if (Test-Path "render.yaml") {
    Write-Host "   ✓ render.yaml exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠ render.yaml not found (optional)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "5. Checking git status..." -ForegroundColor Yellow
try {
    $gitStatus = git rev-parse --git-dir 2>&1
    Write-Host "   ✓ Git repository initialized" -ForegroundColor Green
    
    # Check if artifacts are tracked
    $trackedArtifacts = git ls-files "artifacts/*.pkl" 2>&1
    if ($trackedArtifacts) {
        Write-Host "   ✓ Artifacts are tracked by git" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Artifacts not tracked. Run:" -ForegroundColor Yellow
        Write-Host "     git add artifacts/*.pkl" -ForegroundColor White
        Write-Host "     git commit -m 'Add model artifacts'" -ForegroundColor White
    }
    
    # Check for uncommitted changes
    $changes = git status --porcelain
    if (-not $changes) {
        Write-Host "   ✓ No uncommitted changes" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ You have uncommitted changes:" -ForegroundColor Yellow
        git status --short
    }
} catch {
    Write-Host "   ✗ Not a git repository" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ Pre-deployment check complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Commit and push to GitHub:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Prepare for Render deployment'" -ForegroundColor Gray
Write-Host "   git push origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Go to https://dashboard.render.com" -ForegroundColor White
Write-Host "3. Create new Web Service" -ForegroundColor White
Write-Host "4. Connect your repository: smt2208/Book_Recommender" -ForegroundColor White
Write-Host "5. Use these settings:" -ForegroundColor White
Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   Start Command: gunicorn app:app" -ForegroundColor Gray
Write-Host ""
Write-Host "See RENDER_DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
