from restaurantsystem.celery import app
from channels.layers import get_channel_layer

@app.task
def send_order_update_to_multiple_groups(order_id, status_id, group_names):
    print("holaaaaa mundooooo", order_id, status_id)
    try:
        channel_layer = get_channel_layer()
        for group_name in group_names:
            channel_layer.group_send(
                group_name,
                {
                    'type': 'order_status_update',
                    'order_id': order_id,
                    'status_id': status_id,
                    'message': f"Order {order_id} status updated to {status_id}"
                }
            )
        return f"Message sent to {len(group_names)} groups."
    except Exception as e:
        print(f"Error occurred: {e}")
        raise e