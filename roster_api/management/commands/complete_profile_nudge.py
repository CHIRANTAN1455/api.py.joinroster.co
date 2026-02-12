from django.core.management.base import BaseCommand
from roster_api.models import Users, EmailNotifications, EmailNotificationLogs, Logs
from django.utils import timezone
from datetime import timedelta
from roster_api.profile_helper import ProfileHelper, profile_missing_fields_day1, profile_missing_fields_day3, profile_missing_fields_day7
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send alerts of new jobs (Complete Profile Nudge)'

    def handle(self, *args, **options):
        helper = ProfileHelper()
        now = timezone.now()
        
        job_alert_notification = EmailNotifications.objects.filter(code='complete-profile-nudge').first()
        job_alert_id = job_alert_notification.id if job_alert_notification else 1

        # Get all non-activated suppliers
        # Laravel: User::where('account_type', 'editor')->whereNull('activated_at')...
        users = Users.objects.filter(
            account_type='editor',
            activated_at__isnull=True,
            deleted_at__isnull=True,
            created_at__gte=timezone.datetime(2024, 7, 1, tzinfo=timezone.utc),
            active=1
        ).exclude(
            email='business.davidbier@gmail.com'
        )
        
        # whereHas('job_types')
        users = users.filter(userjobtypes__isnull=False).distinct()
        
        # whereDoesntHave('user_email_unsubscriptions')
        users = users.exclude(
            useremailunsubscriptions__unsubscribe_all=1
        ).exclude(
            useremailunsubscriptions__email_notification_id=job_alert_id
        )

        # Users who didn't skip setup
        skipped_setup_user_ids = Logs.objects.filter(
            action='Skip Setup'
        ).values_list('user_id', flat=True)
        
        users_who_not_skip_setup = users.exclude(id__in=skipped_setup_user_ids)

        for user in users_who_not_skip_setup:
            code_nudge = f'nudge-complete-profile-user-{user.uuid}'
            code_improve = f'nudge-activated-profile-to-improve-user-{user.uuid}'
            
            notif_nudge = EmailNotifications.objects.filter(code=code_nudge).first()
            notif_improve = EmailNotifications.objects.filter(code=code_improve).first()

            if not notif_improve and not notif_nudge:
                days_since_creation = (now - user.created_at).days
                
                if days_since_creation >= 1:
                    profile_status = helper.calculate_profile_completion(user)
                    completion_percent = profile_status['complete_percent']
                    missing_fields = profile_status['missing_fields']

                    if completion_percent < 100 and len(missing_fields) >= 1:
                        self.trigger_base_alert(user, missing_fields, helper)

    def trigger_base_alert(self, user, missing_fields, helper):
         # Helper to send email callback
         def send_email(user, url, code, mapped_missing_fields, subject, preview):
             # Placeholder sending email
             self.stdout.write(f"Sending {code} to {user.email}: {subject}")
             pass

         helper.trigger_base_alert(user, missing_fields, send_email)
