import os
import json
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def handler(event, context):
    """Vercel serverless function to create a PaymentIntent"""
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Default amount to $4900.50
        amount = body.get('amount', 490050)
        currency = body.get('currency', 'usd')
        
        # Create PaymentIntent with specific payment methods
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
                'customer_name': body.get('customer_name', 'Katy'),
                'plan': body.get('plan', 'Protection Coverage')
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'clientSecret': payment_intent.client_secret,
                'paymentIntentId': payment_intent.id
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

