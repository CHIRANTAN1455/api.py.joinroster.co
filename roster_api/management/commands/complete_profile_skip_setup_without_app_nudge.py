from django.core.management.base import BaseCommand
from roster_api.models import (
    Users,
    EmailNotifications,
    EmailNotificationLogs,
    Logs,
    Settings
)
from django.utils import timezone
from roster_api.profile_helper import ProfileHelper, profile_missing_fields_day1, profile_missing_fields_day3, profile_missing_fields_day7
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send alerts for users who skipped setup without draft application'

    def handle(self, *args, **options):
        helper = ProfileHelper()
        now = timezone.now()
        
        job_alert_notification = EmailNotifications.objects.filter(code='skip-setup-without-application-nudge').first()
        job_alert_id = job_alert_notification.id if job_alert_notification else 1

        users = Users.objects.filter(
            account_type='editor',
            activated_at__isnull=True,
            deleted_at__isnull=True,
            created_at__gte=timezone.datetime(2024, 5, 1, tzinfo=timezone.utc),
            active=1
        ).exclude(email='business.davidbier@gmail.com')

        users = users.filter(userjobtypes__isnull=False).distinct()
        
        users = users.exclude(
            useremailunsubscriptions__unsubscribe_all=1
        ).exclude(
            useremailunsubscriptions__email_notification_id=job_alert_id
        )

        skipped_setup_user_ids = Logs.objects.filter(
            action='Skip Setup'
        ).values_list('user_id', flat=True)

        users = users.filter(id__in=skipped_setup_user_ids)

        # WITHOUT draft application
        users = users.exclude(projectapplications__status='draft').distinct()

        d1_fields = profile_missing_fields_day1()
        d3_fields = profile_missing_fields_day3()
        d7_fields = profile_missing_fields_day7()
        
        base_url = 'https://app.joinroster.co'
        setting = Settings.objects.filter(key='web_app_url').first()
        if setting:
            base_url = setting.value
        url = f"{base_url}/things-to-do?page=profile"

        for user in users:
            code_nudge = f'nudge-complete-profile-user-{user.uuid}'
            code_improve = f'nudge-activated-profile-to-improve-user-{user.uuid}'
            
            notif_nudge = EmailNotifications.objects.filter(code=code_nudge).exists()
            notif_improve = EmailNotifications.objects.filter(code=code_improve).exists()

            if not notif_improve and not notif_nudge:
                days_since_creation = (now - user.created_at).days
                if days_since_creation >= 1:
                    profile_status = helper.calculate_profile_completion(user)
                    completion_percent = profile_status['complete_percent']
                    missing_fields = profile_status['missing_fields']

                    if completion_percent < 100:
                        if 'projects' in missing_fields or 'creators' in missing_fields:
                            # Use skip-profile-no-application flow
                            notif_d1 = EmailNotifications.objects.filter(code='skip-profile-no-application-d1').first()
                            log_d1 = EmailNotificationLogs.objects.filter(
                                user=user,
                                email_notification=notif_d1
                            ).first() if notif_d1 else None
                            
                            if not log_d1 and notif_d1:
                                mapped_fields = [d1_fields.get(f) for f in missing_fields if f in d1_fields]
                                subject = f"{user.first_name} - receive personalized job alerts with creators" if user.first_name else "Receive personalized job alerts with creators"
                                preview = "Didn't find a role? Set up your profile so Roster can send more job recommendations."
                                
                                self.stdout.write(f"Sending skip-profile-no-application-d1 to {user.email}")
                                EmailNotificationLogs.objects.create(
                                    email_notification=notif_d1,
                                    user=user,
                                    created_at=now
                                )
                            elif log_d1:
                                days_since = (now - log_d1.created_at).days
                                if days_since >= 2:
                                    notif_d3 = EmailNotifications.objects.filter(code='skip-profile-no-application-d3').first()
                                    log_d3 = EmailNotificationLogs.objects.filter(
                                        user=user,
                                        email_notification=notif_d3
                                    ).first() if notif_d3 else None
                                    
                                    if not log_d3 and notif_d3:
                                        mapped_fields = [d3_fields.get(f) for f in missing_fields if f in d3_fields]
                                        subject = "Get first dibs for new creator gigs - here's how"
                                        preview = 'We only send job recommendations to completed profiles [Action required]'
                                        
                                        self.stdout.write(f"Sending skip-profile-no-application-d3 to {user.email}")
                                        EmailNotificationLogs.objects.create(
                                            email_notification=notif_d3,
                                            user=user,
                                            created_at=now
                                        )
                                    elif log_d3:
                                         days_since = (now - log_d3.created_at).days
                                         if days_since >= 4:
                                            notif_d7 = EmailNotifications.objects.filter(code='skip-profile-no-application-d7').first()
                                            log_d7 = EmailNotificationLogs.objects.filter(
                                                user=user,
                                                email_notification=notif_d7
                                            ).first() if notif_d7 else None
                                            
                                            if not log_d7 and notif_d7:
                                                mapped_fields = [d7_fields.get(f) for f in missing_fields if f in d7_fields]
                                                subject = f"That's a bummer… I thought we were friends, {user.first_name}" if user.first_name else "That's a bummer… I thought we were friends"
                                                preview = 'Few steps away from your next role with top creators'
                                                
                                                self.stdout.write(f"Sending skip-profile-no-application-d7 to {user.email}")
                                                EmailNotificationLogs.objects.create(
                                                    email_notification=notif_d7,
                                                    user=user,
                                                    created_at=now
                                                )
                        else:
                            self.trigger_base_alert(user, missing_fields, helper)

    def trigger_base_alert(self, user, missing_fields, helper):
         def send_email(user, url, code, mapped_missing_fields, subject, preview):
             self.stdout.write(f"Sending {code} to {user.email} (Base Alert)")
             pass
         helper.trigger_base_alert(user, missing_fields, send_email)
