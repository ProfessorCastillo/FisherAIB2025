#!/bin/bash

# GitHub Pages Deployment Script
echo "Setting up GitHub Pages deployment..."

# Initialize git if not already
if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "Initial commit - AIB 2025 Conference Search"
fi

echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "   Name it: FisherAIB2025"
echo ""
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR-USERNAME/FisherAIB2025.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Pages:"
echo "   - Go to Settings → Pages"
echo "   - Source: Deploy from branch"
echo "   - Branch: main, folder: / (root)"
echo "   - Save"
echo ""
echo "4. Your site will be live at:"
echo "   https://YOUR-USERNAME.github.io/FisherAIB2025/conference-search.html"