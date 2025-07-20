import json
import requests
from django.conf import settings

class KhaltiClient:
    def __init__(self, public_key, secret_key, sandbox=settings.SANDBOX):
        self.public_key = public_key
        self.secret_key = secret_key
        self.sandbox = sandbox
        self.session = requests.Session()

        self.base_url = (
            settings.KHALTI_SANDBOX_BASE_URL if sandbox else settings.KHALTI_LIVE_BASE_URL
        )

    def _get_headers(self):
        return {
            "Authorization": f"Key {self.secret_key}",
            "Content-Type": "application/json"
        }

    def create_intent(self, amount, customer_info, fee_details=None):
        """
        Create Khalti payment intent.

        :param amount: Amount in Rupees (string or float)
        :param customer_info: Dict with name, email, phone
        :param fee_details: Optional dict with:
            - order_name: str
            - product_details: list
        :return: Parsed response JSON from Khalti
        """
        if amount is None:
            raise ValueError("Amount is required.")

        try:
            amount_in_paisa = int(float(amount) * 100)
        except (ValueError, TypeError):
            raise ValueError("Invalid amount value. Must be a number.")

        order_name = fee_details.get("order_name", "Student Fee Payment") if fee_details else "Student Fee Payment"
        product_details = fee_details.get("product_details", []) if fee_details else []

        payload = {
            "return_url": f"{settings.WEB_UI_URL}/payment-success",
            "website_url": settings.WEB_UI_URL,
            "amount": amount_in_paisa,
            "purchase_order_name": order_name,
            "customer_info": customer_info,
            "purchase_order_id": "ORDER123",
            "product_details": product_details,
        }

        response = self.session.post(
            f"{self.base_url}/epayment/initiate/",
            data=json.dumps(payload),
            headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Khalti Error: {response.status_code} - {response.text}")

        return response.json()


