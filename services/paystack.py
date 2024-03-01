import requests
from django.conf import settings

SUBUNIT_CURRENCY = 100


class PayStackSerivce:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.currency = "NGN"
        self.session = requests.Session()

    def initialise_payment(self, email: str, amount: str):
        url = "https://api.paystack.co/transaction/initialize"
        payload = {
            "email": email,
            "amount": str(amount * SUBUNIT_CURRENCY),
            "currency": self.currency,
        }

        response = self.session.post(url, headers=self.headers, json=payload)

        return response.json()

    def verify_payment(self, paystack_ref):
        url = f"https://api.paystack.co/transaction/verify/{paystack_ref}"
        response = self.session.get(url, headers=self.headers)

        while True:
            if response.json()["data"]["status"] == "success":
                return True
            elif response.json()["data"]["status"] in ["ongoing", "pending", "processing", "queued"]:
                continue
            else:
                return False
