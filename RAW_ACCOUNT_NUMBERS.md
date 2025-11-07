# Raw Account Number Access Guide

This document explains how to access raw bank account numbers from US bank account payment methods in your Stripe integration.

## Overview

When customers pay with US bank accounts, you can retrieve the full account and routing numbers for 24 hours after the payment method is created. This is useful for record-keeping, reconciliation, or integration with other systems.

## Features Implemented

### 1. Skip Verification for Bank Accounts

The PaymentIntent is configured with `verification_method: 'instant_or_skip'` which allows:
- **Instant verification**: Using Financial Connections for immediate verification
- **Skip verification**: Allowing customers to manually enter their account details without micro-deposits

**Location:** `backend/app.py` - `create_payment_intent()` function

```python
payment_method_options={
    'us_bank_account': {
        'verification_method': 'instant_or_skip'
    }
}
```

### 2. Raw Account Number Retrieval

A new endpoint retrieves the full account details including the raw account number.

**Endpoint:** `GET /payment-method/<payment_method_id>/raw-account`

**Location:** `backend/app.py` - `get_raw_account_number()` function

#### Response Example:

```json
{
  "id": "pm_xxxxx",
  "type": "us_bank_account",
  "us_bank_account": {
    "account_holder_type": "individual",
    "account_type": "checking",
    "bank_name": "STRIPE TEST BANK",
    "fingerprint": "xxxxx",
    "last4": "6789",
    "routing_number": "110000000",
    "account_number": "000123456789"
  },
  "note": "Raw account number is available (accessible for 24 hours after creation)"
}
```

### 3. Display on Success Page

After a successful payment, the completion page automatically fetches and displays:
- Bank name
- Account type (checking/savings)
- Routing number
- Full account number (if available within 24 hours)
- A note about availability

## Important Limitations

### 24-Hour Access Window

⏰ **Raw account numbers are only accessible for 24 hours** after:
- Creation of the Payment Method (manual entry)
- Creation of the Financial Connections Account (instant verification)

After 24 hours, only the last 4 digits remain accessible.

### Tokenized Account Numbers (TANs)

Some banks return Tokenized Account Numbers instead of raw account details:

| Bank  | Routing Number | Notes                    |
|-------|----------------|--------------------------|
| Chase | 028000121      | Uses TAN                 |
| PNC   | 063214312      | Uses TAN                 |

For these banks:
- Only the last 4 digits are available
- The TAN can still be used for transactions
- Customers can manually add accounts to get raw numbers

### ACH Notification of Change (NOC)

When a bank sends an NOC (updated account information):
- Stripe automatically updates the PaymentMethod
- The 24-hour access window is **refreshed** for another 24 hours
- You receive a `payment_method.automatically_updated` webhook event

## Production Requirements

### Restricted API Keys

For production, create a **restricted API key** with these permissions:
1. Navigate to: https://dashboard.stripe.com/apikeys
2. Create a new restricted key
3. Grant these permissions:
   - `PaymentMethods` (read)
   - `PaymentMethod RawAccountReads` (read)

**Why?** This limits the scope of the API key to only what's needed for account access.

### Security Best Practices

✅ **DO:**
- Use restricted keys in production
- Store raw account numbers securely (encrypted at rest)
- Log access to raw account numbers for audit trails
- Delete raw account numbers when no longer needed
- Use HTTPS for all API calls

❌ **DON'T:**
- Expose raw account numbers in client-side code
- Store raw account numbers in browser local storage
- Log raw account numbers in plain text
- Share restricted keys across multiple services

## Testing

### Test Bank Account Details

Use these test details in your integration:

**Routing Number:** `110000000`  
**Account Number:** `000123456789`

### Testing the Flow

1. Start your servers:
   ```bash
   # Backend
   cd backend && python app.py
   
   # Frontend
   cd frontend && npm run dev
   ```

2. Visit http://localhost:5174

3. Complete the payment form with test bank account

4. On the success page, you'll see:
   - Payment confirmation
   - Bank account details
   - Raw account number (available for 24 hours)

### Testing the API Directly

```bash
# Get payment intent details
curl http://localhost:5000/payment-intent/<payment_intent_id>

# Get raw account number (within 24 hours)
curl http://localhost:5000/payment-method/<payment_method_id>/raw-account
```

## Integration with Your System

### Option 1: Real-time Capture

Capture the raw account number immediately after payment success:

```javascript
// In your success handler
fetch(`${API_URL}/payment-method/${paymentMethodId}/raw-account`)
  .then(res => res.json())
  .then(data => {
    if (data.us_bank_account.account_number) {
      // Store in your database
      saveToDatabase({
        routing: data.us_bank_account.routing_number,
        account: data.us_bank_account.account_number
      });
    }
  });
```

### Option 2: Webhook Handler

Set up a webhook to capture account details asynchronously:

```python
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    event = stripe.Webhook.construct_event(
        request.data,
        request.headers['Stripe-Signature'],
        webhook_secret
    )
    
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        payment_method_id = payment_intent.payment_method
        
        # Retrieve raw account details
        payment_method = stripe.PaymentMethod.retrieve(
            payment_method_id,
            expand=['us_bank_account.account_number']
        )
        
        # Store in your system
        # ...
    
    return jsonify({'status': 'success'})
```

## Troubleshooting

### "Raw account number not available"

**Causes:**
- More than 24 hours have passed since creation
- Bank uses Tokenized Account Numbers (Chase, PNC)
- Permission error with API key

**Solutions:**
- Capture account numbers immediately after creation
- Use a restricted API key with proper permissions
- For TAN banks, consider micro-deposit verification

### Permission Errors

**Error:** `Permission denied. Use a restricted API key...`

**Solution:** Create and use a restricted API key with:
- PaymentMethods (read)
- PaymentMethod RawAccountReads (read)

## Resources

- [Stripe ACH Direct Debit Guide](https://docs.stripe.com/payments/ach-direct-debit)
- [Financial Connections Documentation](https://docs.stripe.com/financial-connections)
- [Payment Methods API](https://docs.stripe.com/api/payment_methods)
- [Restricted API Keys](https://docs.stripe.com/keys)

## Support

For questions about this implementation:
1. Check the Stripe API documentation
2. Review your Stripe Dashboard logs
3. Contact Stripe Support for account-specific issues

