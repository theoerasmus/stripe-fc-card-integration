import os
import json
import stripe

def handler(event, context):
    """Vercel serverless function to retrieve raw bank account details"""
    
    try:
        # Get payment method ID from query parameters
        query_params = event.get('queryStringParameters', {})
        payment_method_id = query_params.get('payment_method')
        
        if not payment_method_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Payment method ID is required'})
            }
        
        # Use restricted key for raw account access
        restricted_key = os.environ.get('STRIPE_RESTRICTED_KEY')
        if not restricted_key:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Restricted API key not configured',
                    'instructions': 'Add STRIPE_RESTRICTED_KEY environment variable'
                })
            }
        
        # Retrieve payment method with expanded account number
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
                response_data['note'] = 'Raw account number not available (may have expired after 24 hours)'
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_data)
        }
    
    except stripe.error.PermissionError as e:
        return {
            'statusCode': 403,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Permission denied. Use a restricted API key with correct permissions.',
                'details': str(e)
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

