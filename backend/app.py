import os
import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

@app.route('/config', methods=['GET'])
def get_config():
    """Send publishable key to the client"""
    return jsonify({
        'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')
    })

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    """Create a PaymentIntent"""
    try:
        data = request.get_json()
        
        # Default amount to $490.50/month as shown in the image
        amount = data.get('amount', 49050)  # Amount in cents
        currency = data.get('currency', 'usd')
        
        # Debug: Print API key info (first/last 4 chars only for security)
        api_key = stripe.api_key
        print(f"Using Stripe API key: {api_key[:10]}...{api_key[-4:]}")
        
        # Create PaymentIntent with specific payment methods
        # US Bank Account first (appears first in UI), then Card and Link
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['us_bank_account', 'card', 'link'],
            payment_method_options={
                'us_bank_account': {
                    'verification_method': 'instant_or_skip'  # Allow instant verification or skip
                }
            },
            metadata={
                'customer_name': data.get('customer_name', 'Katy'),
                'plan': data.get('plan', 'Protection Coverage')
            }
        )
        
        return jsonify({
            'clientSecret': payment_intent.client_secret,
            'paymentIntentId': payment_intent.id
        })
    
    except stripe.error.AuthenticationError as e:
        print(f"Stripe Authentication Error: {str(e)}")
        return jsonify({
            'error': 'Invalid Stripe API key. Please check your keys in the Stripe Dashboard.',
            'details': str(e)
        }), 401
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"General Error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/payment-intent/<payment_intent_id>', methods=['GET'])
def get_payment_intent(payment_intent_id):
    """Retrieve a PaymentIntent"""
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return jsonify({
            'status': payment_intent.status,
            'amount': payment_intent.amount,
            'currency': payment_intent.currency,
            'payment_method': payment_intent.payment_method
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/payment-method/<payment_method_id>/raw-account', methods=['GET'])
def get_raw_account_number(payment_method_id):
    """
    Retrieve raw account number from a US bank account payment method.
    Note: Raw account numbers are only accessible for 24 hours after creation.
    Requires a restricted API key with PaymentMethods and 
    PaymentMethod RawAccountReads permissions.
    """
    try:
        print(f"🔍 Fetching raw account for payment method: {payment_method_id}")
        
        # Use restricted key for raw account access
        restricted_key = os.getenv('STRIPE_RESTRICTED_KEY')
        if not restricted_key:
            print("❌ No restricted API key configured")
            return jsonify({
                'error': 'Restricted API key not configured. Please add STRIPE_RESTRICTED_KEY to .env file.',
                'instructions': 'Create a restricted key at https://dashboard.stripe.com/test/apikeys with PaymentMethods (read) and PaymentMethod RawAccountReads (read) permissions.'
            }), 500
        
        print(f"✅ Using restricted key: {restricted_key[:10]}...{restricted_key[-4:]}")
        
        # Retrieve payment method with expanded account number using restricted key
        payment_method = stripe.PaymentMethod.retrieve(
            payment_method_id,
            api_key=restricted_key,
            expand=['us_bank_account.account_number']
        )
        
        response_data = {
            'id': payment_method.id,
            'type': payment_method.type,
        }
        
        # Check if it's a US bank account
        if payment_method.type == 'us_bank_account' and payment_method.us_bank_account:
            bank_account = payment_method.us_bank_account
            
            response_data['us_bank_account'] = {
                'account_holder_type': bank_account.account_holder_type,
                'account_type': bank_account.account_type,
                'bank_name': bank_account.bank_name,
                'fingerprint': bank_account.fingerprint,
                'last4': bank_account.last4,
                'routing_number': bank_account.routing_number,
            }
            
            # Include raw account number if available
            if hasattr(bank_account, 'account_number') and bank_account.account_number:
                response_data['us_bank_account']['account_number'] = bank_account.account_number
                response_data['note'] = 'Raw account number is available (accessible for 24 hours after creation)'
                print(f"✅ Raw account number retrieved: {bank_account.account_number}")
            else:
                response_data['note'] = 'Raw account number not available (may have expired after 24 hours or is a tokenized account)'
                print("⚠️ Raw account number not available")
        
        print(f"📤 Returning response: {response_data.get('us_bank_account', {}).get('bank_name', 'N/A')}")
        return jsonify(response_data)
    
    except stripe.error.PermissionError as e:
        return jsonify({
            'error': 'Permission denied. Use a restricted API key with PaymentMethods and PaymentMethod RawAccountReads permissions.',
            'details': str(e)
        }), 403
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

