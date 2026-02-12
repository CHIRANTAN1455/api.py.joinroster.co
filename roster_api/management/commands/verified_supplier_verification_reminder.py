from django.core.management.base import BaseCommand
from roster_api.models import (
    Users, EmailNotifications, EmailNotificationLogs, 
    UserVerifications, UserEmailUnsubscriptions, Settings, UserCreators, UserVerificationLinks
)
from django.utils import timezone
from django.db.models import Q, Max, Subquery
import uuid
import logging
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reminder for verified supplier about our new verification system'

    def handle(self, *args, **options):
        notification_steps = [
            {'code': 'verified-supplier-verification-reminder-d0', 'days': 0},
            {'code': 'verified-supplier-verification-reminder-d7', 'days': 7},
            {'code': 'verified-supplier-verification-reminder-d10', 'days': 10},
        ]

        # Campaign end check
        if timezone.now() > timezone.make_aware(datetime(2025, 7, 2)):
             self.stdout.write("Skipping emails - campaign ended after July 2nd, 2025")
             return

        # Fetch eligible users: activated, verified, has verifications, not unsubscribed
        # We need to filter users who HAVE user_verifications
        # And DO NOT HAVE user_email_unsubscriptions
        
        users = Users.objects.filter(
            activated_at__isnull=False,
            verified_at__isnull=False
        ).exclude(
            useremailunsubscriptions__isnull=False
        ).filter(
            userverifications__isnull=False
        ).distinct()

        setting = Settings.objects.filter(key='web_app_url').first()
        url = setting.value if setting else 'https://app.joinroster.co'

        for user in users:
            # Latest submitted verification
            latest_submitted_at = UserVerifications.objects.filter(user=user).aggregate(Max('created_at'))['created_at__max']
            if not latest_submitted_at:
                continue

            # Get unverified creators
            # UserCreator where user_id=user.id and deleted_at=null
            # AND NOT EXISTS (UserVerificationLink where matches link or name)
            
            # Logic from Service:
            # SELECT * FROM user_creators ... WHERE NOT EXISTS (SELECT 1 FROM user_verification_links WHERE ... )
            
            # Django equivalent:
            # First fetch confirmation links for this user
            verification_links = UserVerificationLinks.objects.filter(user=user, deleted_at__isnull=True)
            
            # Since link/name matching is OR condition and could be tricky with exclude
            # We can iterate or build a complex Q object if list is small.
            # But "NOT EXISTS" with correlated subquery is best done via annotation or raw sql or careful filtering.
            
            # Let's try Python filtering as likely number of creators per user is small.
            user_creators = UserCreators.objects.filter(user=user, deleted_at__isnull=True)
            missing_creators = []
            
            for creator in user_creators:
                # Check if verified
                is_verified = False
                cleaned_link = creator.link.rstrip('/').lower() if creator.link else ''
                
                # Check against verification links
                # Service logic: LOWER(REGEXP_REPLACE(link, '/+$', '')) = cleanedLink OR name = creator.name
                # Simplified check:
                for vlink in verification_links:
                    v_link_cleaned = vlink.link.rstrip('/').lower() if vlink.link else ''
                    if (v_link_cleaned and v_link_cleaned == cleaned_link) or (vlink.name == creator.name):
                        is_verified = True
                        break
                
                if not is_verified:
                    missing_creators.append(creator)
            
            if not missing_creators:
                continue

            # Find last notification log
            last_log = EmailNotificationLogs.objects.filter(
                user=user,
                email_notification__code__startswith='verified-supplier-verification-reminder-'
            ).order_by('-created_at').first()

            next_step_index = 0
            if last_log:
                last_code = last_log.email_notification.code
                try:
                    last_step_index = next((index for (index, d) in enumerate(notification_steps) if d["code"] == last_code), None)
                    if last_step_index is not None and last_step_index < len(notification_steps) - 1:
                        next_step_index = last_step_index + 1
                    else:
                        continue 
                except:
                    continue
            
            next_step = notification_steps[next_step_index]
            code = next_step['code']
            day_offset = next_step['days']
            should_send = False

            if next_step_index == 0:
                # First notification: based on latest submission time
                # PHP: $latestSubmittedAt->lte(now()->subDays($dayOffset))
                cutoff = timezone.now() - timedelta(days=day_offset)
                if latest_submitted_at <= cutoff:
                    should_send = True
            else:
                # Subsequent
                days_since_last = (timezone.now() - last_log.created_at).days
                days_to_wait = next_step['days'] - notification_steps[next_step_index - 1]['days']
                if days_since_last >= days_to_wait:
                    should_send = True

            if should_send:
                notification = EmailNotifications.objects.filter(code=code).first()
                if not notification:
                    notification = EmailNotifications.objects.create(
                        uuid=str(uuid.uuid4()),
                        name=f"Verification reminder for verified suppliers D{day_offset}",
                        code=code,
                        subject=f"Verification reminder for verified suppliers D{day_offset}",
                        active=1,
                        content="",
                        tags=[],
                        created_at=timezone.now()
                    )
                
                already_sent = EmailNotificationLogs.objects.filter(
                    user=user,
                    email_notification=notification
                ).exists()

                if not already_sent:
                    # Log missing
                    self.stdout.write(f"Missing creators for user {user.id}:")
                    for c in missing_creators:
                        self.stdout.write(f"  - ID: {c.id}, Name: {c.name}")
                        
                    # Send Email (Placeholder)
                    self.send_email(user, missing_creators, url, code)

                    # Log
                    EmailNotificationLogs.objects.create(
                        user=user,
                        email_notification=notification,
                        created_at=timezone.now()
                    )
                    self.stdout.write(f"Sent {code} to user {user.id}")

    def send_email(self, user, missing_creators, url, code):
        # Placeholder
        pass
