import os
import json

def handler(event, context):
    """Vercel serverless function to return Stripe publishable key"""
    
    publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'publishableKey': publishable_key
        })
    }

