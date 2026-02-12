from django.core.management.base import BaseCommand
from roster_api.models import Settings
from django.utils import timezone
import requests
import socket
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Ping /test-supervisor endpoint and alert Slack if queue is not running'

    def handle(self, *args, **options):
        now = timezone.now()
        hostname = socket.gethostname()

        # Get Slack webhook URL from settings
        slack_setting = Settings.objects.filter(key='generic_slack_webhook_url').first()
        
        if not slack_setting or not slack_setting.value:
            logger.warning("Slack webhook URL not configured for queue check.")
            self.stdout.write(self.style.WARNING("Slack webhook URL not configured."))
            return

        slack_webhook_url = slack_setting.value

        try:
            # Pings the endpoint
            response = requests.get('https://tenet-api.joinroster.co/test-supervisor', timeout=10)
            
            content = ""
            if response.status_code != 200 or 'RUNNING' not in response.text:
                content = f"🚨 *Queue worker is NOT running* on `{hostname}` at {now}"
            else:
                content = f"✅ Queue is running correctly at {now} on {hostname}"
            
            # Send notification
            self.send_slack_notification(slack_webhook_url, content)
            
        except Exception as e:
            logger.error(f"Queue check request failed: {str(e)}")
            content = f"🚨 *Queue status check request failed* on `{hostname}` at {now}"
            self.send_slack_notification(slack_webhook_url, content)

    def send_slack_notification(self, webhook_url, message):
        try:
            payload = {'text': message}
            requests.post(webhook_url, json=payload)
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {str(e)}")
