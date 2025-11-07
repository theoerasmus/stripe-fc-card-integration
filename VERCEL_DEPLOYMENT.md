# Vercel Deployment Guide

This guide will help you deploy your Stripe Payment Element project to Vercel.

## Prerequisites

- Vercel account (free tier works fine)
- Vercel CLI installed (optional, but recommended)
- Stripe API keys

## Project Structure

The project has been configured for Vercel deployment:

```
stripe-payment-element-project/
├── frontend/              # React + Vite frontend
│   ├── src/
│   ├── dist/             # Build output (created during deployment)
│   └── package.json
├── backend/
│   └── api/              # Vercel Serverless Functions (Python)
│       ├── config.py
│       ├── create-payment-intent.py
│       ├── payment-intent.py
│       ├── raw-account.py
│       └── requirements.txt
├── vercel.json           # Vercel configuration
└── VERCEL_DEPLOYMENT.md  # This file
```

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended for first time)

1. **Push your code to GitHub/GitLab/Bitbucket**
   ```bash
   cd /Users/theoerasmus/stripe-payment-element-project
   git init
   git add .
   git commit -m "Initial commit - ready for Vercel"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click "Add New" → "Project"
   - Import your Git repository

3. **Configure the project**
   - **Project Name**: Choose any name (e.g., `stripe-payment-checkout`)
   - **Framework Preset**: Leave as "Other" or select "Vite"
   - **Root Directory**: Leave as `./` (project root)
   - Vercel will auto-detect settings from `vercel.json`

4. **Add Environment Variables**
   
   Click on "Environment Variables" and add:
   
   | Name | Value | Description |
   |------|-------|-------------|
   | `STRIPE_PUBLISHABLE_KEY` | `pk_test_51...` | Your Stripe publishable key |
   | `STRIPE_SECRET_KEY` | `sk_test_51...` | Your Stripe secret key |
   | `STRIPE_RESTRICTED_KEY` | `rk_test_51...` | Your Stripe restricted key |
   | `VITE_API_URL` | `/api` | API endpoint prefix |

   **Important**: Add these for all environments (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (2-3 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed)
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from project root**
   ```bash
   cd /Users/theoerasmus/stripe-payment-element-project
   vercel
   ```

4. **Follow the prompts**
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N** (first time)
   - What's your project's name? `stripe-payment-checkout`
   - In which directory is your code located? **./

**
   - Want to override settings? **N** (vercel.json will be used)

5. **Add Environment Variables**
   ```bash
   vercel env add STRIPE_PUBLISHABLE_KEY
   vercel env add STRIPE_SECRET_KEY
   vercel env add STRIPE_RESTRICTED_KEY
   ```

6. **Deploy to production**
   ```bash
   vercel --prod
   ```

## Environment Variables Setup

### Get Your Stripe Keys

1. **Publishable Key** (starts with `pk_test_`)
   - https://dashboard.stripe.com/test/apikeys
   - Can be exposed in frontend

2. **Secret Key** (starts with `sk_test_`)
   - https://dashboard.stripe.com/test/apikeys
   - Never expose in frontend

3. **Restricted Key** (starts with `rk_test_`)
   - https://dashboard.stripe.com/test/apikeys
   - Click "Create restricted key"
   - Give it a name: "Raw Account Access"
   - Grant permissions:
     - ✅ **Payment methods**: Read
     - ✅ **PaymentMethod RawAccountReads**: Read
   - Click "Create key"

### Add to Vercel

**Via Dashboard:**
- Go to your project → Settings → Environment Variables
- Add each variable
- Check: ☑️ Production ☑️ Preview ☑️ Development

**Via CLI:**
```bash
vercel env add STRIPE_PUBLISHABLE_KEY production
# Paste your key when prompted
# Repeat for all keys
```

## Testing Your Deployment

1. **Visit your deployed URL**
   - Example: `https://your-project.vercel.app`

2. **Test with Stripe test cards**
   
   **Credit Card:**
   - Number: `4242 4242 4242 4242`
   - Expiry: Any future date (e.g., `12/34`)
   - CVC: Any 3 digits (e.g., `123`)
   
   **US Bank Account:**
   - Routing: `110000000`
   - Account: `000123456789`
   - Account Type: Checking

3. **Check the completion page**
   - Should show payment status
   - Should display bank account details (for bank account payments)

## Troubleshooting

### Build Fails

**Error:** `Module not found: stripe`
**Fix:** Ensure `backend/api/requirements.txt` exists with `stripe==7.4.0`

**Error:** `Cannot find module 'react'`
**Fix:** Check that `frontend/package.json` exists with all dependencies

### API Errors

**Error:** `Invalid API key`
**Fix:** 
- Check environment variables in Vercel dashboard
- Ensure keys start with correct prefixes (`pk_test_`, `sk_test_`, `rk_test_`)
- Redeploy after adding/updating environment variables

**Error:** `Permission denied` for raw account
**Fix:**
- Verify restricted key has correct permissions
- Must have "PaymentMethod RawAccountReads" permission

### CORS Errors

**Error:** `CORS policy blocked`
**Fix:** Headers are already configured in serverless functions. If still seeing errors:
- Clear browser cache
- Check Vercel function logs
- Verify API endpoints are being called correctly

## View Logs

### Via Dashboard
1. Go to your project
2. Click "Deployments"
3. Click on a deployment
4. Click "View Function Logs"

### Via CLI
```bash
vercel logs <deployment-url>
```

## Custom Domain (Optional)

1. Go to your project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Vercel automatically handles SSL certificates

## Updating Your Deployment

**Automatic Deploys:**
- Push to your connected Git repository
- Vercel automatically builds and deploys

**Manual Deploy:**
```bash
cd /Users/theoerasmus/stripe-payment-element-project
git add .
git commit -m "Update message"
git push origin main
```

Or via CLI:
```bash
vercel --prod
```

## Local Development

Your local development environment still works:

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

The frontend will use `http://localhost:5000` locally and `/api` on Vercel.

## Cost

- Vercel Free Tier includes:
  - 100GB bandwidth/month
  - 100GB-hours serverless function execution/month
  - Unlimited deployments
  - **Perfect for this project!**

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Stripe Docs**: https://stripe.com/docs
- **This Project**: See README.md for project-specific documentation

---

## Quick Deploy Checklist

- [ ] Code pushed to Git repository
- [ ] Project imported to Vercel
- [ ] Environment variables added (all 3 Stripe keys + VITE_API_URL)
- [ ] Deployment successful
- [ ] Payment form loads correctly
- [ ] Test payment works
- [ ] Bank account details display on completion page

🎉 **You're live!**

