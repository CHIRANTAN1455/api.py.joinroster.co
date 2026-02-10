import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from roster_api.models import EditorInvitations, Matchings, Users
from roster_api.user_service import UserService

class Command(BaseCommand):
    help = 'Process pending editor invitations (Port of editor:invite)'

    def handle(self, *args, **options):
        pending_invites = EditorInvitations.objects.filter(status='pending')
        user_service = UserService()
        
        self.stdout.write(self.style.SUCCESS(f"Found {pending_invites.count()} pending invitations."))
        
        for invite in pending_invites:
            try:
                self.stdout.write(f"Processing invitation for {invite.email}...")
                
                # Check if user already exists
                user = user_service.get_user_by_email(invite.email)
                
                if not user:
                    # Create user
                    # In Laravel: account_type='editor', active=0
                    user, raw_password = user_service.create_user(
                        email=invite.email,
                        first_name=invite.first_name,
                        last_name=invite.last_name,
                        role_code='editor',
                        account_type='editor',
                        active=0,
                        reference=f"Invited through a past project - {invite.referrer.name if invite.referrer else 'Unknown'}"
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created new user for {invite.email} (UUID: {user.uuid})"))
                else:
                    self.stdout.write(f"User {invite.email} already exists (UUID: {user.uuid}).")

                # Create Matching if referrer_project exists
                if invite.referrer_project:
                    # check if matching already exists
                    # Using ForeignKey field 'project'
                    if not Matchings.objects.filter(project=invite.referrer_project, user=user).exists():
                        Matchings.objects.create(
                            uuid=str(uuid.uuid4()),
                            project=invite.referrer_project,
                            user=user,
                            status='pending'
                        )
                        self.stdout.write(f"Created matching for project ID {invite.referrer_project.id}")

                # Update invitation status
                invite.status = 'invited'
                invite.updated_at = timezone.now()
                # invite.password_reset_link = ... 
                invite.save()
                
                self.stdout.write(self.style.SUCCESS(f"Invitation for {invite.email} marked as 'invited'."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {invite.email}: {str(e)}"))
