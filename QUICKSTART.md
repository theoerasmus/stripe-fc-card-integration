# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Get Your Stripe Keys

1. Go to https://dashboard.stripe.com/test/apikeys
2. Copy your **Publishable key** (pk_test_...)
3. Copy your **Secret key** (sk_test_...)

## Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env
```

Edit `backend/.env`:
```
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
```

## Step 3: Setup Frontend

```bash
# Open new terminal
cd frontend
npm install
```

## Step 4: Run the Application

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
python app.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Step 5: Test It Out!

1. Open http://localhost:3000
2. Click on the Payment Element
3. Use test card: `4242 4242 4242 4242`
4. Any future date, any CVC, any ZIP
5. Click "Start my coverage"

## Alternative: Use the Start Script

On macOS/Linux, you can use the provided script:

```bash
chmod +x start-dev.sh
./start-dev.sh
```

## What You'll See

- A beautiful checkout page styled like the Ethos design
- Payment Element with support for cards and bank accounts
- Progress stepper showing the checkout flow
- Payment summary showing $490.50/month
- Success page after completing payment

## Need Help?

- Check the main README.md for detailed documentation
- Visit https://stripe.com/docs/testing for more test cards
- Check browser console for any errors

## Pro Tips

💡 The Payment Element automatically shows the most relevant payment methods
💡 Try the test routing number `110000000` with account `000123456789` for ACH
💡 Use card `4000 0025 0000 3155` to test 3D Secure authentication
💡 All test payments will appear in your Stripe Dashboard under Test mode

