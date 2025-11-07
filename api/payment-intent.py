import os
import json
import stripe
from urllib.parse import parse_qs

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def handler(event, context):
    """Vercel serverless function to retrieve a PaymentIntent"""
    
    try:
        # Get payment intent ID from query parameters
        query_params = event.get('queryStringParameters', {})
        payment_intent_id = query_params.get('id')
        
        if not payment_intent_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Payment intent ID is required'})
            }
        
        # Retrieve the payment intent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
                'payment_method': payment_intent.payment_method
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

