from webhooks.models.webhook import Webhook

class WebhookService:

    def receive_message(self, webhook_data):
        webhook_to_create = Webhook(webhook_body=webhook_data)
        webhook_to_create.save()
        
        return True