import requests
from requests.auth import HTTPBasicAuth
from decimal import Decimal, ROUND_HALF_UP
import os

class HttpServices:
    @staticmethod
    def pay_order_request(order, payment_order_id):
        merchant_id = os.getenv("MERCHANT_ID")
        openpay_secret = os.getenv("OPENPAY_SECRET_KEY") 
        amount = order.total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        amount_for_openpay = float(amount)
        response = requests.post(
            f"https://sandbox-api.openpay.co/v1/{str(merchant_id)}/charges",
            auth=HTTPBasicAuth(str(openpay_secret), str(merchant_id)),
            json={
                "method" : "bank_account",
                "amount" : int(order.total_amount),
                "currency" : "COP",
                "description" : f"Pago de pedido no {order.id}",
                "order_id" : str(payment_order_id),
                "iva" : "1900",
                "redirect_url":"https://www.openpay.co/",
                "customer" : {
                    "name" : order.customer.first_name,
                    "last_name" : order.customer.last_name,
                    "email" : order.customer.email,
                    "phone_number" : order.customer.phone,
                    "requires_account" : False
                }
            }
        )
        
        print(response.json())
        
        # variable response save the openpay response
        if response.status_code == 200:
            response_obj = {
                "order_gateway_id": payment_order_id,
                "transaction_id": response.json().get("id"),
                "pse_url": response.json().get("payment_method").get("url")
            }
            return response_obj
        
        return {
            "error": "unexpected error ocurred, please retry"
        }