import requests
from requests.auth import HTTPBasicAuth
from decimal import Decimal

class HttpServices:
    @staticmethod
    def pay_order_request(order, payment_order_id):
        
        response = requests.post(
            "https://sandbox-api.openpay.co/v1/m58o2ppbhnxvda4bdbbk/charges",
            auth=HTTPBasicAuth('sk_572944e2f89740f2b7dbad9fef8d6b89',"m58o2ppbhnxvda4bdbbk"),
            json={
                "method" : "bank_account",
                "amount" : int(order.total_amount * 1000),
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
        
        if response.status_code == 200:
            response_obj = {
                "transaction_id": response.json().get("id"),
                "pse_url": response.json().get("payment_method").get("url")
            }
            return response_obj
        
        return {
            "error": "unexpected error ocurred, please retry"
        }