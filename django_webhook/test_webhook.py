from datetime import datetime

from django_webhook.models import Webhook
from django_webhook.tasks import fire_webhook
import json
from django.core.serializers.json import DjangoJSONEncoder


def send_test(webhook: Webhook, payload=None, topic=None):
    """
    Send a test webhook request with the provided payload.

    Args:
        payload (dict, optional): Custom payload to send. If not provided, a default test payload will be used.
        topic (str, optional): Topic to use for the test. If not provided, a default test topic will be used.

    Returns:
        WebhookEvent: The created webhook event object if STORE_EVENTS is enabled, None otherwise.
    """

    if not webhook.active:
        raise ValueError("Cannot send test webhook to inactive webhook")

    if payload is None:
        payload = {
            "test": True,
            "message": "This is a test webhook",
            "timestamp": str(datetime.now()),
            "webhook_uuid": str(webhook.uuid),
            "webhook_id": webhook.id,
        }

    if topic is None:
        topic = "test/webhook"

    # Convert payload to JSON string
    payload_str = json.dumps(payload, cls=DjangoJSONEncoder)

    # Send the webhook synchronously to get immediate feedback
    result = fire_webhook.apply(
        args=[webhook.id, payload_str, topic, "test"],
        throw=True
    ).get()

    return result
