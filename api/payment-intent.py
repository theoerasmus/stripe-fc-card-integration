import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import stripe

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
        
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            payment_intent_id = query_params.get('id', [None])[0]
            
            if not payment_intent_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Payment intent ID is required'}).encode())
                return
            
            # Retrieve the payment intent
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
                'payment_method': payment_intent.payment_method
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
