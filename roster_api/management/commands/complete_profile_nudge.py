from django.core.management.base import BaseCommand
from django.utils import timezone
from roster_api.models import Users, EmailNotifications, EmailNotificationLogs

class Command(BaseCommand):
    help = 'Nudge users to complete their profile (Port of complete-profile:nudge)'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # 1. Get template
        try:
            template = EmailNotifications.objects.get(code='complete-profile-nudge', active=1)
        except EmailNotifications.DoesNotExist:
            self.stdout.write(self.style.ERROR("Template 'complete-profile-nudge' not found."))
            return

        # 2. Find users with incomplete profiles
        # Laravel criteria: active=1, completion_status < 100
        incomplete_users = Users.objects.filter(
            active=1,
            account_type='user',
            deleted_at__isnull=True
        ).exclude(completion_status='100')
        
        self.stdout.write(f"Found {incomplete_users.count()} users with incomplete profiles.")

        for user in incomplete_users:
            # 3. Check if already nudged recently (e.g., in the last 7 days)
            last_nudge = EmailNotificationLogs.objects.filter(
                user=user,
                email_notification=template
            ).order_by('-created_at').first()
            
            if last_nudge:
                days_since = (now - last_nudge.created_at).days
                if days_since < 7:
                    continue
            
            self.stdout.write(self.style.SUCCESS(f"Nudging user: {user.email} (Status: {user.completion_status})"))
            
            # 4. Log notification
            EmailNotificationLogs.objects.create(
                user=user,
                email_notification=template,
                created_at=now,
                updated_at=now
            )

        self.stdout.write(self.style.SUCCESS("Profile completion nudges processed."))
