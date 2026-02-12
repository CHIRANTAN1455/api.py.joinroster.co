from django.core.management.base import BaseCommand
from roster_api.models import (
    Users, EmailNotifications, EmailNotificationLogs, 
    UserVerifications, UserEmailUnsubscriptions, Settings
)
from django.utils import timezone
from django.db.models import Q
import uuid
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reminder for activated supplier to start submitting verification'

    def handle(self, *args, **options):
        notification_steps = [
            {'code': 'activated-supplier-verification-start-reminder-d3', 'days_after_activation': 3},
            {'code': 'activated-supplier-verification-start-reminder-d8', 'days_after_previous': 5},
            {'code': 'activated-supplier-verification-start-reminder-d11', 'days_after_previous': 3},
        ]

        # Fetch eligible users: activated, not verified
        users = Users.objects.filter(
            activated_at__isnull=False,
            verified_at__isnull=True
        ).exclude(
            useremailunsubscriptions__isnull=False
        ).exclude(
            userverifications__isnull=False
        )

        setting = Settings.objects.filter(key='web_app_url').first()
        url = setting.value if setting else 'https://app.joinroster.co'

        for user in users:
            # Double check user has no verifications (redundant given exclude query but safe)
            if UserVerifications.objects.filter(user=user).exists():
                continue

            # Find last notification log
            last_log = EmailNotificationLogs.objects.filter(
                user=user,
                email_notification__code__startswith='activated-supplier-verification-start-reminder-'
            ).order_by('-created_at').first()

            next_step_index = 0
            if last_log:
                last_code = last_log.email_notification.code
                # Python simpler equivalent of collect search
                try:
                    last_step_index = next((index for (index, d) in enumerate(notification_steps) if d["code"] == last_code), None)
                    
                    if last_step_index is not None and last_step_index < len(notification_steps) - 1:
                        next_step_index = last_step_index + 1
                    else:
                        continue # All steps sent
                except:
                    continue
            
            next_step = notification_steps[next_step_index]
            code = next_step['code']
            should_send = False

            if next_step_index == 0:
                # 3 days after activation
                # PHP: $activatedAt->lte(now()->subDays(3))
                # i.e. Activated date is BEFORE (Now - 3 days) => Activated more than 3 days ago
                cutoff = timezone.now() - timedelta(days=next_step['days_after_activation'])
                if user.activated_at <= cutoff:
                    should_send = True
            else:
                # Days after previous
                # PHP: $daysSinceLast >= $nextStep['days_after_previous']
                # i.e. LastLog.created_at + days <= Now
                if last_log:
                    days_diff = (timezone.now() - last_log.created_at).days
                    if days_diff >= next_step['days_after_previous']:
                        should_send = True
            
            if should_send:
                # Create notification if needed
                notification = EmailNotifications.objects.filter(code=code).first()
                if not notification:
                    day_label = next_step['days_after_activation'] if next_step_index == 0 else (8 if next_step_index == 1 else 11)
                    notification = EmailNotifications.objects.create(
                        uuid=str(uuid.uuid4()),
                        name=f"Verification reminder for activated suppliers who haven't started D {day_label}",
                        code=code,
                        subject=f"Verification reminder for activated suppliers who haven't started D {day_label}",
                        active=1,
                        content="",
                        tags=[],
                        created_at=timezone.now()
                    )
                
                # Check duplication
                already_sent = EmailNotificationLogs.objects.filter(
                    user=user,
                    email_notification=notification
                ).exists()

                if not already_sent:
                    # Send Email (Placeholder)
                    self.send_email(user, url, code)

                    # Log
                    EmailNotificationLogs.objects.create(
                        user=user,
                        email_notification=notification,
                        created_at=timezone.now()
                    )
                    self.stdout.write(f"Sent {code} to user {user.id}")

    def send_email(self, user, url, code):
        # Placeholder
        pass
