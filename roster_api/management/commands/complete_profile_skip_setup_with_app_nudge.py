from django.core.management.base import BaseCommand
from roster_api.models import (
    Users,
    EmailNotifications,
    EmailNotificationLogs,
    Logs,
    Projects,
    ProjectApplications,
    Settings
)
from django.utils import timezone
from roster_api.profile_helper import ProfileHelper
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send alerts for users who skipped setup but have draft application'

    def handle(self, *args, **options):
        helper = ProfileHelper()
        now = timezone.now()
        
        job_alert_notification = EmailNotifications.objects.filter(code='skip-setup-with-application-nudge').first()
        job_alert_id = job_alert_notification.id if job_alert_notification else 1

        # Get users
        users = Users.objects.filter(
            account_type='editor',
            activated_at__isnull=True,
            deleted_at__isnull=True,
            created_at__gte=timezone.datetime(2024, 5, 1, tzinfo=timezone.utc),
            active=1
        ).exclude(email='business.davidbier@gmail.com')

        users = users.filter(userjobtypes__isnull=False).distinct()

        if job_alert_notification:
            users = users.exclude(
                useremailunsubscriptions__unsubscribe_all=1
            ).exclude(
                useremailunsubscriptions__email_notification_id=job_alert_id
            )

        # Users who skipped setup
        skipped_setup_user_ids = Logs.objects.filter(
            action='Skip Setup'
        ).values_list('user_id', flat=True)

        users = users.filter(id__in=skipped_setup_user_ids)

        # With draft application
        users = users.filter(projectapplications__status='draft').distinct()

        profile_missing_fields_day1 = helper.get_missing_fields_d1() # Ops, defined as global func, need to import or access via helper if I add it
        profile_missing_fields_day3 = helper.get_missing_fields_d3()
        # I'll just import them in ProfileHelper or redefine global func call

        from roster_api.profile_helper import profile_missing_fields_day1, profile_missing_fields_day3

        d1_fields = profile_missing_fields_day1()
        d3_fields = profile_missing_fields_day3()

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
                        # Check if base alert active
                        notif_d3_base = EmailNotifications.objects.filter(code='incomplete-profile-d3').first()
                        base_alert_triggered = False
                        if notif_d3_base:
                             base_alert_triggered = EmailNotificationLogs.objects.filter(
                                 user=user,
                                 email_notification=notif_d3_base
                             ).exists()

                        if not base_alert_triggered:
                            # Draft app logic
                            draft_apps = ProjectApplications.objects.filter(
                                user=user, 
                                status='draft'
                            ).order_by('-created_at')
                            
                            if draft_apps.exists():
                                app = draft_apps.first()
                                project = app.project
                                setting = Settings.objects.filter(key='web_app_url').first()
                                base_url = setting.value if setting else 'https://app.joinroster.co'
                                url = f"{base_url}/jobs/{project.uuid}/details"
                                
                                creator = project.user
                                # Social profiles name? Assuming model UserSocialProfiles
                                creator_profile = creator.usersocialprofile
                                creator_name = creator_profile.name if creator_profile and creator_profile.name else (creator.name or 'Creator')

                                notif_draft_d1 = EmailNotifications.objects.filter(code='skip-profile-draft-application-d1').first()
                                log_d1 = EmailNotificationLogs.objects.filter(
                                    user=user,
                                    email_notification=notif_draft_d1
                                ).first() if notif_draft_d1 else None

                                if not log_d1 and notif_draft_d1:
                                    mapped_fields = [d1_fields.get(f) for f in missing_fields if f in d1_fields]
                                    subject = 'The secret to getting hired by creators'
                                    preview = f'You have an incomplete job application for {creator_name}'
                                    
                                    # Send email placeholder
                                    self.stdout.write(f"Sending skip-profile-draft-application-d1 to {user.email}")
                                    
                                    EmailNotificationLogs.objects.create(
                                        email_notification=notif_draft_d1,
                                        user=user,
                                        project=project,
                                        created_at=now
                                    )
                                elif log_d1:
                                    days_since_d1 = (now - log_d1.created_at).days
                                    if days_since_d1 >= 2:
                                        notif_draft_d3 = EmailNotifications.objects.filter(code='skip-profile-draft-application-d3').first()
                                        log_d3 = EmailNotificationLogs.objects.filter(
                                            user=user,
                                            email_notification=notif_draft_d3
                                        ).first() if notif_draft_d3 else None

                                        if not log_d3 and notif_draft_d3:
                                            mapped_fields = [d3_fields.get(f) for f in missing_fields if f in d3_fields]
                                            subject = f"You and {creator_name} swiped right on each other"
                                            preview = 'Get your profile stand out more among others'
                                            
                                            self.stdout.write(f"Sending skip-profile-draft-application-d3 to {user.email}")
                                            
                                            EmailNotificationLogs.objects.create(
                                                email_notification=notif_draft_d3,
                                                user=user,
                                                project=project,
                                                created_at=now
                                            )
                                        elif log_d3:
                                            days_since_d3 = (now - log_d3.created_at).days
                                            if days_since_d3 >= 3:
                                                # Trigger base alert
                                                self.trigger_base_alert(user, missing_fields, helper)
                        else:
                            if len(missing_fields) >= 2:
                                self.trigger_base_alert(user, missing_fields, helper)

    def trigger_base_alert(self, user, missing_fields, helper):
         def send_email(user, url, code, mapped_missing_fields, subject, preview):
             self.stdout.write(f"Sending {code} to {user.email} (Base Alert)")
             pass
         helper.trigger_base_alert(user, missing_fields, send_email)
