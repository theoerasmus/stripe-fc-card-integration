# Stripe Payment Element Integration

A full-stack application demonstrating Stripe Payment Element integration with React frontend and Python Flask backend.

## Project Structure

```
stripe-payment-element-project/
├── backend/           # Python Flask backend
│   ├── app.py        # Main Flask application
│   ├── requirements.txt
│   └── env.example   # Environment variables template
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── CheckoutPage.jsx
│   │   │   ├── CheckoutPage.css
│   │   │   ├── CompletionPage.jsx
│   │   │   └── CompletionPage.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Features

- ✅ Stripe Payment Element with PaymentIntent
- ✅ Support for both credit cards and bank accounts (ACH)
- ✅ Modern, responsive UI matching Ethos design
- ✅ Progress stepper showing checkout flow
- ✅ Payment confirmation page
- ✅ Secure SSL badge and Norton verification display
- ✅ Real-time payment status updates

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Stripe account with API keys

## Setup Instructions

### 1. Get Stripe API Keys

1. Sign up or log in to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to Developers → API keys
3. Copy your **Publishable key** (starts with `pk_test_`)
4. Copy your **Secret key** (starts with `sk_test_`)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env

# Edit .env file and add your Stripe keys
# STRIPE_SECRET_KEY=sk_test_your_secret_key_here
# STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# The frontend will automatically connect to the backend at http://localhost:5000
```

## Running the Application

### Start Backend Server

```bash
# In backend directory with virtual environment activated
python app.py

# Server will start at http://localhost:5000
```

### Start Frontend Development Server

```bash
# In frontend directory
npm run dev

# App will open at http://localhost:3000
```

## Testing the Integration

### Test Credit Card Numbers

Use these test card numbers from Stripe:

- **Success:** 4242 4242 4242 4242
- **Requires authentication:** 4000 0025 0000 3155
- **Declined:** 4000 0000 0000 9995

Use any future expiry date, any 3-digit CVC, and any postal code.

### Test Bank Account (ACH)

- **Routing number:** 110000000
- **Account number:** 000123456789

## API Endpoints

### Backend Endpoints

- `GET /health` - Health check endpoint
- `GET /config` - Returns Stripe publishable key
- `POST /create-payment-intent` - Creates a new PaymentIntent
  - Body: `{ amount: number, currency: string, customer_name: string }`
  - Returns: `{ clientSecret: string, paymentIntentId: string }`
- `GET /payment-intent/:id` - Retrieves PaymentIntent status

## Key Features Explained

### Payment Element

The Payment Element is Stripe's pre-built UI component that:
- Automatically displays relevant payment methods
- Handles payment method validation
- Supports multiple payment types (cards, ACH, etc.)
- Provides a consistent, localized experience

### PaymentIntent

PaymentIntents are Stripe objects that represent your intent to collect payment:
- Track payment lifecycle from creation to completion
- Handle authentication (3D Secure)
- Support multiple payment methods
- Can be confirmed on the client or server side

## Customization

### Changing Payment Amount

Edit `CheckoutPage.jsx`:

```javascript
body: JSON.stringify({
  amount: 49050, // Amount in cents ($490.50)
  currency: 'usd',
}),
```

### Styling Payment Element

Modify the `options` prop in `CheckoutPage.jsx`:

```javascript
<PaymentElement 
  options={{
    layout: {
      type: 'accordion',
      defaultCollapsed: false,
      radios: true,
    },
  }}
/>
```

### Changing Colors and Fonts

Edit `CheckoutPage.css` to match your brand colors and typography.

## Security Best Practices

✅ **Implemented:**
- API keys stored in environment variables
- CORS configured for specific origins
- Client-side and server-side payment validation
- HTTPS required in production (use a reverse proxy)

⚠️ **For Production:**
- Use live API keys (pk_live_ and sk_live_)
- Enable webhook signature verification
- Implement rate limiting
- Add user authentication
- Deploy with HTTPS enabled
- Set up proper error monitoring

## Deployment

### Backend Deployment

1. Set environment variables on your hosting platform
2. Use a production WSGI server (e.g., Gunicorn):
   ```bash
   gunicorn app:app
   ```
3. Configure CORS for your production domain

### Frontend Deployment

1. Update API_URL in frontend code to your production backend URL
2. Build the production bundle:
   ```bash
   npm run build
   ```
3. Deploy the `dist` folder to your hosting platform (Vercel, Netlify, etc.)

## Troubleshooting

### "Connection refused" error
- Make sure both backend and frontend servers are running
- Check that backend is on port 5000 and frontend on port 3000

### "Invalid API key" error
- Verify your Stripe API keys in the `.env` file
- Make sure you're using test keys (pk_test_ and sk_test_)

### Payment Element not showing
- Check browser console for errors
- Verify Stripe publishable key is being loaded
- Ensure PaymentIntent client secret is created successfully

## Resources

- [Stripe Payment Element Documentation](https://stripe.com/docs/payments/payment-element)
- [Stripe API Reference](https://stripe.com/docs/api)
- [React Stripe.js Documentation](https://stripe.com/docs/stripe-js/react)
- [Flask Documentation](https://flask.palletsprojects.com/)

## License

MIT License - Feel free to use this project as a template for your own applications.

## Support

For Stripe-related questions, visit [Stripe Support](https://support.stripe.com/)

For issues with this implementation, please check the code comments and Stripe documentation.

