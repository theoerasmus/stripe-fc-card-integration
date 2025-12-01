import os
from http.server import BaseHTTPRequestHandler
import json
import stripe
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse the URL to get the payment method ID
            # URL will be like: /api/raw-account?payment_method=pm_xxx
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            
            payment_method_id = query_params.get('payment_method', [None])[0]
            
            if not payment_method_id:
                raise ValueError('Payment method ID is required')
            
            # Use restricted key for raw account access
            restricted_key = os.environ.get('STRIPE_RESTRICTED_KEY')
            if not restricted_key:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    'error': 'Restricted API key not configured.',
                    'instructions': 'Add STRIPE_RESTRICTED_KEY environment variable in Vercel'
                }
                self.wfile.write(json.dumps(error_response).encode())
                return
            
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
                else:
                    response_data['note'] = 'Raw account number not available (may have expired after 24 hours or is a tokenized account)'
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except stripe.error.PermissionError as e:
            self.send_response(403)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'error': 'Permission denied. Use a restricted API key with PaymentMethods and PaymentMethod RawAccountReads permissions.',
                'details': str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())
            
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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return



