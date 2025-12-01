import os
from http.server import BaseHTTPRequestHandler
import json
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Default amount to $4900.50 as shown in the image
            amount = data.get('amount', 490050)
            currency = data.get('currency', 'usd')
            
            # Create PaymentIntent with specific payment methods
            # US Bank Account first (appears first in UI), then Card and Link
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['us_bank_account', 'card', 'link'],
                payment_method_options={
                    'us_bank_account': {
                        'verification_method': 'instant_or_skip'
                    }
                },
                metadata={
                    'customer_name': data.get('customer_name', 'Katy'),
                    'plan': data.get('plan', 'Protection Coverage')
                }
            )
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                'clientSecret': payment_intent.client_secret,
                'paymentIntentId': payment_intent.id
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return



