import requests
from requests.auth import HTTPBasicAuth

class HttpServices:
    @staticmethod
    def pay_order_request(order):
        response = requests.post(
            "https://sandbox-api.openpay.co/v1/m58o2ppbhnxvda4bdbbk/charges",
            auth=HTTPBasicAuth('sk_572944e2f89740f2b7dbad9fef8d6b89',"m58o2ppbhnxvda4bdbbk"),
            json={
                "method" : "bank_account",
                "amount" : order.total_amount,
                "currency" : "COP",
                "description" : f"Pago de orden no {order.id}",
                "order_id" : f"{order.id}",
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
        
        if response.status_code == 200:
            response_obj = {
                "pse_url": response.json().get("payment_method").get("url")
            }
            return response_obj
        
        return {
            "error": "unexpected error ocurred, please retry"
        }