#!/bin/bash

echo "🔍 Verifying Vercel deployment setup..."
echo ""

# Check for vercel.json
if [ -f "vercel.json" ]; then
    echo "✅ vercel.json found"
else
    echo "❌ vercel.json missing"
    exit 1
fi

# Check for frontend files
if [ -f "frontend/package.json" ]; then
    echo "✅ frontend/package.json found"
else
    echo "❌ frontend/package.json missing"
    exit 1
fi

# Check for backend API files
if [ -d "backend/api" ]; then
    echo "✅ backend/api directory found"
    
    if [ -f "backend/api/config.py" ]; then
        echo "  ✅ config.py found"
    else
        echo "  ❌ config.py missing"
    fi
    
    if [ -f "backend/api/create-payment-intent.py" ]; then
        echo "  ✅ create-payment-intent.py found"
    else
        echo "  ❌ create-payment-intent.py missing"
    fi
    
    if [ -f "backend/api/payment-intent.py" ]; then
        echo "  ✅ payment-intent.py found"
    else
        echo "  ❌ payment-intent.py missing"
    fi
    
    if [ -f "backend/api/raw-account.py" ]; then
        echo "  ✅ raw-account.py found"
    else
        echo "  ❌ raw-account.py missing"
    fi
    
    if [ -f "backend/api/requirements.txt" ]; then
        echo "  ✅ requirements.txt found"
    else
        echo "  ❌ requirements.txt missing"
    fi
else
    echo "❌ backend/api directory missing"
    exit 1
fi

# Check for .env files
if [ -f "frontend/.env.production" ]; then
    echo "✅ frontend/.env.production found"
else
    echo "⚠️  frontend/.env.production missing (will use default API URL)"
fi

echo ""
echo "📋 Pre-deployment checklist:"
echo ""
echo "Before deploying to Vercel, make sure you have:"
echo "  1. ☐ Pushed code to GitHub/GitLab/Bitbucket"
echo "  2. ☐ Stripe Publishable Key (pk_test_...)"
echo "  3. ☐ Stripe Secret Key (sk_test_...)"
echo "  4. ☐ Stripe Restricted Key (rk_test_...)"
echo "  5. ☐ Vercel account ready"
echo ""
echo "✨ Setup verification complete!"
echo ""
echo "Next step: Follow VERCEL_DEPLOYMENT.md for deployment instructions"

