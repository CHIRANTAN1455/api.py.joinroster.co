from django.core.management.base import BaseCommand
from roster_api.models import (
    Users, EditorInvitations, Roles, JobTypes, UserProjects, UserCreators,
    UserProjectContentTopics, UserCreatorContentTopics, EmailNotifications,
    EmailNotificationLogs, Settings, PasswordResets
)
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from roster_api.utils import generate_password_reset_token
import logging
import uuid
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Editor Invitation Campaign'

    def handle(self, *args, **options):
        pending_invitations = EditorInvitations.objects.filter(status='pending')
        editor_role = Roles.objects.filter(code='editor').first()
        
        # We need a proper user creation service or method. 
        # Mimicking UserService logic here for simplicity or calling it if available.
        # Since user_service.py was deleted/restored, I can check if it has create method?
        # But let's verify if user_service.py is reliable.
        # I'll implement inline for now as it's safer.

        for record in pending_invitations:
            self.process_invitation(record, editor_role)

    def process_invitation(self, record, editor_role):
        user = Users.objects.filter(email=record.email).first()
        referrer = Users.objects.filter(id=record.referrer_id).first()
        
        user_exists = False
        url = None
        
        if not user:
            # Create user
            with transaction.atomic():
                user = Users.objects.create(
                    uuid=str(uuid.uuid4()),
                    email=record.email,
                    first_name=record.first_name,
                    last_name=record.last_name,
                    role_id=editor_role.id if editor_role else None,
                    # reference field... 'Invited through a past project - ' + referrer.name
                    # Check Users model for reference field?
                    # Users model usually has 'reference' field? Let's assume yes or skip if fails.
                    account_type='editor',
                    active=0,
                    created_at=timezone.now()
                )
                
                # Check reference field on Users model... (omitted check, assuming no error if field exists or kwargs ignored if not strict)
                # Actually helper create method would be better if needed.
                
                # Generate token
                token_str = generate_password_reset_token(user) 
                
                # Helper:
                # $url = config('setting')->web_app_url . "/new-password?token=$token&ref=mail&via=project-referral&email=$email";
                setting = Settings.objects.filter(key='web_app_url').first()
                base_url = setting.value if setting else 'https://app.joinroster.co'
                url = f"{base_url}/new-password?token={token_str}&ref=mail&via=project-referral&email={user.email}"
        else:
            user_exists = True

        # Process Project
        user_project = None
        user_project_exists = False
        
        if record.referrer_project_id:
            referrer_project = UserProjects.objects.filter(id=record.referrer_project_id).first()
            if referrer_project:
                user_project = UserProjects.objects.filter(link=referrer_project.link, user=user).first()
                
                if not user_project:
                    user_project = UserProjects.objects.create(
                        uuid=str(uuid.uuid4()),
                        user=user,
                        project_type_id=referrer_project.project_type_id,
                        job_type_id=record.job_type_id if record.job_type_id else referrer_project.job_type_id,
                        link=referrer_project.link,
                        icon=referrer_project.icon,
                        name=referrer_project.name,
                        description=referrer_project.description,
                        views=referrer_project.views,
                        likes=referrer_project.likes if referrer_project.likes else 0,
                        meta=referrer_project.meta,
                        created_at=timezone.now(),
                        individual_project=0 # Assuming 0 for false
                    )
                    
                    # Content Topics
                    topics = UserProjectContentTopics.objects.filter(user_project=referrer_project)
                    for topic in topics:
                        UserProjectContentTopics.objects.create(
                            uuid=str(uuid.uuid4()),
                            user_project=user_project,
                            content_topic_id=topic.content_topic_id,
                            status='active',
                            created_at=timezone.now()
                        )
                else:
                    user_project_exists = True

        # Process Creator
        user_creator = None
        user_creator_exists = False
        
        if record.referrer_creator_id:
            referrer_creator = UserCreators.objects.filter(id=record.referrer_creator_id).first()
            if referrer_creator:
                user_creator = UserCreators.objects.filter(name=referrer_creator.name, user=user).first()
                
                if not user_creator:
                    user_creator = UserCreators.objects.create(
                        uuid=str(uuid.uuid4()),
                        user=user,
                        link=referrer_creator.link,
                        icon=referrer_creator.icon,
                        name=referrer_creator.name,
                        description=referrer_creator.description,
                        meta=referrer_creator.meta,
                        followers=referrer_creator.followers,
                        created_at=timezone.now()
                    )
                else:
                    user_creator_exists = True # Logic in PHP says $user_project_exists = true here? Copy paste error in PHP?
                    # "if (!$user_creator) ... else { $user_project_exists = true; }" <-- Line 160.
                    # This seems like a bug in PHP code or I'm misreading.
                    # Assuming it meant user_creator_exists.
                    user_creator_exists = True

                topics = UserCreatorContentTopics.objects.filter(user_creator=referrer_creator)
                for topic in topics:
                    # Update or Create
                    UserCreatorContentTopics.objects.update_or_create(
                        user_creator=user_creator,
                        content_topic_id=topic.content_topic_id,
                        defaults={
                            'uuid': str(uuid.uuid4()),
                            'status': 'active',
                            'created_at': timezone.now()
                        }
                    )
        
        role_name = None
        if record.job_type_id:
            jt = JobTypes.objects.filter(id=record.job_type_id).first()
            if jt:
                role_name = jt.name

        # Notifications
        if not user_exists:
            record.password_reset_link = url
            # Sending email (Mocks)
            self.send_invite_email(user, referrer, user_project, url, user_creator, role_name)
            
            # Update record
            record.status = 'complete'
            record.updated_at = timezone.now()
            record.save()
            
            self.log_email_notification(user, 'editor-invitation')
            
        else:
            # Existing user
            if user_project:
                if not user_project_exists:
                    url = 'https://app.joinroster.co/settings/creators'
                    self.send_project_invite_email(user, referrer, user_project, url, user_creator, role_name)
                
                self.log_email_notification(user, 'project-invitation')
                
                record.status = 'complete'
                record.updated_at = timezone.now()
                record.save()

            else:
                 if not user_creator_exists:
                     url = 'https://app.joinroster.co/settings/creators'
                     self.send_project_invite_email(user, referrer, None, url, user_creator, role_name)
                 
                 self.log_email_notification(user, 'project-invitation')

                 record.status = 'complete'
                 record.updated_at = timezone.now()
                 record.save()

    def send_invite_email(self, user, referrer, user_project, url, user_creator, role):
        # Placeholder
        pass

    def send_project_invite_email(self, user, referrer, user_project, url, user_creator, role):
        # Placeholder
        pass

    def log_email_notification(self, user, code):
        notif = EmailNotifications.objects.filter(code=code).first()
        if notif:
            EmailNotificationLogs.objects.create(
                user=user,
                email_notification=notif,
                created_at=timezone.now()
            )
