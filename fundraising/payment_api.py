import http.client
import json
import base64
import time, random
from django.http import JsonResponse
from dotenv import load_dotenv
import os 


load_dotenv('.env')




api_key: str = os.getenv('API_KEY')

encoded_api_key = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')

def generate_transaction_reference():
    timestamp = int(time.time() * 100)
    random_number = random.randint(100, 999)
    return f'T{timestamp}{random_number}'

def account_reference():
    timestamp = int(time.time() * 10)
    random_number = random.randint(100, 999)
    return f'{timestamp}{random_number}'

    


def charge_card(first_name, last_name, email_address, phone_number, card_number, expiry_month, expiry_year, security_code, amount):
    # Establish a connection to the payment gateway
    transaction_id = generate_transaction_reference()
    conn = http.client.HTTPSConnection("cards-live.78financials.com")


    payload = json.dumps({
        "service_payload": {
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "phone_number": phone_number,
            "amount": amount,  
            "transaction_reference": transaction_id ,
            "currency": "NGN",
            "description": "Test Payment",
            "card": {
                "expiryMonth": expiry_month,
                "expiryYear": expiry_year,
                "securityCode": security_code,
                "cardNumber": card_number
            },
            "callback_url": "https://webhook.site/ed6dd427-dfcf-44a3-8fa7-4cc1ab55e029"
        }
    })


    headers = {
    'Authorization': f'Payaza {encoded_api_key}',  # Add your API key here without needing Base64 encoding
    'Content-Type': 'application/json'
    }

    conn.request("POST", "/card_charge/", payload, headers)

    # Get the response
    res = conn.getresponse()

    # Read and decode the response data
    data = res.read()

    # Print the raw response for debugging
    print("Raw Response: ", data.decode("utf-8"))

    # Parse the JSON response
    response_json = json.loads(data.decode("utf-8"))
    return JsonResponse(response_json)

    # if response_json.get('do3dsAuth'):
    #     creq = response_json.get('formData')  # This would generate the cryptogram (creq) for 3D Secure
    #     threeDsUrl = "https://mtf.gateway.mastercard.com/acs/visa/v2/prompt"  
    #     response_data = {
    #         'statusOk': True,
    #         'do3dsAuth': True,
    #         'threeDsUrl': threeDsUrl,
    #         'formData': creq  # Cryptogram for 3D Secure
    #     }
    #     return JsonResponse(response_data)
    # else:
    #     # If 3D Secure is not needed, complete the payment
    #     return JsonResponse({
    #         'statusOk': response_json.get('statusOk'),
    #         'paymentCompleted': response_json.get('paymentCompleted'),
    #         'amount': response_json.get('amountPaid'),
    #         'messages': response_json.get('message'),
    #         'transaction_reference': transaction_id
    #     })

def transfer_funds( amount, account_name, account_number, bank_code, narration, transaction_reference):
    

    account_reference = account_reference()
    conn = http.client.HTTPSConnection("api.payaza.africa")
    payload = json.dumps({
    "transaction_type": "nuban",
    "service_payload": {
        "payout_amount": amount,
        "transaction_pin": 1111,
        "account_reference": account_reference ,
        "currency": "NGN",
        "country": "NGA",
        "payout_beneficiaries": [
        {
            "credit_amount": amount,
            "account_number": account_number,
            "account_name": account_name,
            "bank_code": bank_code,
            "narration": narration,
            "transaction_reference": transaction_reference,
            "sender": {
            "sender_name": "Joshua Olayemi",
            "sender_id": "",
            "sender_phone_number": "08058830751",
            "sender_address": "123, Ace Street"
            }
        }
        ]
    }
    })
    headers = {
    'Authorization': f'Payaza {encoded_api_key}',
    'X-tenantID': 'test',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/live/payout-receptor/payout", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8")) 

    
    # Parse the JSON response
    response_json = json.loads(data.decode("utf-8"))
    return JsonResponse(response_json)