import http.client
import json
import base64

api_key = 'PZ78-PKTEST-FEB6D9D6-B140-41DF-AEE2-7591E05E4195'

encoded_api_key = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')


def charge_card(first_name, last_name, email_address, phone_number, card_number, expiry_month, expiry_year, security_code, amount):
    # Establish a connection to the payment gateway
    conn = http.client.HTTPSConnection("cards-live.78financials.com")


    payload = json.dumps({
        "service_payload": {
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "phone_number": phone_number,
            "amount": amount,  # You can adjust this as needed
            "transaction_reference": "T13501973673737",  # You can generate this dynamically
            "currency": "Naira",
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

    # Define the headers, including the API key for authorization
    headers = {
    'Authorization': f'Bearer {encoded_api_key}',  # Add your API key here without needing Base64 encoding
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

    if response_json.get("statusOk", False):
        return {
            "success": True,
            "message": response_json.get("message", "Payment successful."),
            "transaction_id": response_json.get("transaction_reference"),
            "amount_paid": amount,
        }
    else:
        return {
            "success": False,
            "message": response_json.get("message", "Payment failed. Try again."),
            "transaction_id": None,
            "amount_paid": 0,
        }
