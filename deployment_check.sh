#!/bin/bash
# Deployment Preparation Script for Render
# Run this script before deploying to Render

echo "=========================================="
echo "Book Recommender - Render Deployment Check"
echo "=========================================="
echo ""

# Check if artifacts exist
echo "1. Checking artifacts..."
if [ -d "artifacts" ]; then
    echo "   ✓ artifacts/ folder exists"
    
    if [ -f "artifacts/model.pkl" ] && [ -f "artifacts/book_name.pkl" ] && [ -f "artifacts/final_ratings.pkl" ] && [ -f "artifacts/book_matrix.pkl" ]; then
        echo "   ✓ All required .pkl files found"
        
        # Check file sizes
        echo ""
        echo "2. Artifact file sizes:"
        ls -lh artifacts/*.pkl | awk '{print "   " $9 ": " $5}'
    else
        echo "   ✗ Missing required .pkl files"
        echo "   Please run: python main.py to train the model"
        exit 1
    fi
else
    echo "   ✗ artifacts/ folder not found"
    exit 1
fi

echo ""
echo "3. Checking requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "   ✓ requirements.txt exists"
    
    if grep -q "gunicorn" requirements.txt; then
        echo "   ✓ gunicorn is included"
    else
        echo "   ✗ gunicorn not found in requirements.txt"
        exit 1
    fi
else
    echo "   ✗ requirements.txt not found"
    exit 1
fi

echo ""
echo "4. Checking render.yaml..."
if [ -f "render.yaml" ]; then
    echo "   ✓ render.yaml exists"
else
    echo "   ⚠ render.yaml not found (optional)"
fi

echo ""
echo "5. Checking git status..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "   ✓ Git repository initialized"
    
    # Check if artifacts are tracked
    if git ls-files artifacts/*.pkl > /dev/null 2>&1; then
        echo "   ✓ Artifacts are tracked by git"
    else
        echo "   ⚠ Artifacts not tracked. Run:"
        echo "     git add artifacts/*.pkl"
        echo "     git commit -m 'Add model artifacts'"
    fi
    
    # Check for uncommitted changes
    if [ -z "$(git status --porcelain)" ]; then
        echo "   ✓ No uncommitted changes"
    else
        echo "   ⚠ You have uncommitted changes:"
        git status --short
    fi
else
    echo "   ✗ Not a git repository"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Pre-deployment check complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to https://dashboard.render.com"
echo "3. Create new Web Service"
echo "4. Connect your repository"
echo "5. Use these settings:"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: gunicorn app:app"
echo ""
echo "See RENDER_DEPLOYMENT.md for detailed instructions"
echo ""
