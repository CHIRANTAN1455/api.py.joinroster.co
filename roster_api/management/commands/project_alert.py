from django.core.management.base import BaseCommand
from roster_api.models import (
    Projects, Users, ProjectApplications, EmailNotifications, EmailNotificationLogs,
    MatchingSettings, UserSocialProfiles, Settings
)
from django.utils import timezone
from django.db.models import Q
from roster_api.match_service import MatchService
import logging
import uuid
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send alert of new jobs'

    def handle(self, *args, **options):
        # Fetch projects
        projects = Projects.objects.filter(
            deleted_at__isnull=True,
            editor__isnull=True,
            status='open',
            published=1,
            notify_editors=1
        )

        # Fetch active editors
        users = Users.objects.filter(
            deleted_at__isnull=True,
            activated_at__isnull=False,
            account_type='editor',
            active=1
        )

        # Min matched score
        min_score_setting = MatchingSettings.objects.filter(key='project_application_min_score').first()
        project_application_min_score = int(min_score_setting.value) if min_score_setting else 60

        match_service = MatchService()
        
        test_user_uuids = [
            '084c18f3-bee0-4e9a-94df-e48722ba7178',
            '9adbc78f-cebe-46b4-b7de-f4391d79b783',
            'ffeda620-e7e1-46c7-82bd-1d6dff66e954',
        ]

        setting = Settings.objects.filter(key='web_app_url').first()
        base_url = setting.value if setting else 'https://app.joinroster.co'

        for project in projects:
            # Notification template
            code = f'open-project-alert-{project.id}'
            notification = EmailNotifications.objects.filter(code=code).first()
            if not notification:
                notification = EmailNotifications.objects.create(
                    uuid=str(uuid.uuid4()),
                    code=code,
                    name=f'Open Project Alert - Project: {project.id}',
                    active=1,
                    tags=['open-project-alert'],
                    subject=f'Send alert for open project ({project.id}) to editors that match requirements',
                    content='</>',
                    created_at=timezone.now()
                )

            for user in users:
                is_test_user = user.uuid in test_user_uuids

                # Check if already notified
                notified = EmailNotificationLogs.objects.filter(
                    user=user,
                    email_notification=notification
                ).exists()

                if notified and not is_test_user:
                    continue

                # Check if applied
                if not is_test_user:
                    applied = ProjectApplications.objects.filter(
                        user=user,
                        project=project
                    ).exists()
                    if applied:
                        continue
                
                # Calculate match
                match_result = match_service.calculate_match(user, project)
                total_match_score = match_result.get('total_match_score', 0)

                if is_test_user:
                    total_match_score = 90

                if total_match_score >= project_application_min_score or (project.send_alert_to_all == 1 and total_match_score > 0):
                    url = f"{base_url}/jobs/{project.uuid}/details/?utm_source=internal&utm_medium=email&utm_campaign=job-alert"
                    
                    # Job type name
                    job_type_name = "Job"
                    pj = project.projectjobtype_set.first()
                    if pj and pj.job_type:
                        job_type_name = pj.job_type.name
                    
                    budget = round(project.budget) if project.budget else 0

                    # Social Profile stats
                    follower_count = 0
                    follower_count_type = 'followers'
                    channel_link = None
                    
                    # project.user might be lazy loaded, ensure access
                    project_owner = project.user
                    social_profile = UserSocialProfiles.objects.filter(user=project_owner).first()
                    
                    if social_profile:
                        if social_profile.youtube:
                            channel_link = social_profile.youtube
                        elif social_profile.tiktok:
                            channel_link = social_profile.tiktok
                        elif social_profile.instagram:
                            channel_link = social_profile.instagram
                        else:
                            channel_link = social_profile.facebook
                        
                        follower_count = social_profile.followers
                        follower_count_type = social_profile.follower_type

                    # Send Email (Placeholder)
                    self.stdout.write(f"Sending alert to {user.email} (Match: {total_match_score}%)")
                    
                    self.send_email(user, project, url, job_type_name, budget, total_match_score, follower_count, channel_link, follower_count_type, project_application_min_score)

                    # Log
                    EmailNotificationLogs.objects.create(
                        email_notification=notification,
                        user=user,
                        created_at=timezone.now()
                    )

    def send_email(self, user, project, url, job_type, budget, match, followers, link, follower_type, min_score):
        # Placeholder
        pass
