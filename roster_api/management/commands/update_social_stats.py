from django.core.management.base import BaseCommand
from django.utils import timezone
from roster_api.models import UserSocialProfile, Users
from roster_api.utils import get_meta

class Command(BaseCommand):
    help = 'Update user social profile stats (Port of user-social-profile:update)'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Filtering active 'user' type accounts (creators)
        active_users = Users.objects.filter(
            active=1, 
            account_type='user', 
            deleted_at__isnull=True
        )
        
        self.stdout.write(f"Analyzing {active_users.count()} active users for social stats update.")
        
        for user in active_users:
            try:
                # OneToOne relationship
                profile = user.usersocialprofile
            except UserSocialProfile.DoesNotExist:
                continue

            # Prioritize links: YouTube > TikTok > Instagram > LinkedIn > Twitter
            primary_link = (
                profile.youtube or 
                profile.tiktok or 
                profile.instagram or 
                profile.linkedin or 
                profile.twitter
            )
            
            if primary_link:
                try:
                    self.stdout.write(f"Fetching stats for {user.email} from {primary_link}...")
                    result = get_meta(primary_link, type='followers')
                    
                    updated = False
                    if result.get('name'):
                        profile.name = result['name']
                        updated = True
                    
                    if result.get('followers', 0) > 0:
                        # Update if current is 0 or if new count is higher (growth)
                        if not profile.followers or result['followers'] > profile.followers:
                            profile.followers = result['followers']
                            updated = True
                    
                    if updated:
                        profile.updated_at = now
                        profile.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated stats for {user.email}"))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to fetch stats for {user.email}: {str(e)}"))
            else:
                # self.stdout.write(f"User {user.email} has no social links.")
                pass

        self.stdout.write(self.style.SUCCESS("Social stats update complete."))
