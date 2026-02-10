import uuid
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Users, Roles, UserRoles
from .utils import generate_password

class UserService:
    def create_user(self, email, first_name=None, last_name=None, role_code=None, account_type='user', active=1, reference=None):
        """
        Port of Laravel UserService->create.
        """
        # 1. Generate password
        raw_password = generate_password()
        
        # 2. Base user data
        user_uuid = str(uuid.uuid4())
        full_name = f"{first_name or ''} {last_name or ''}".strip() or None
        
        # 3. Create user
        user = Users.objects.create(
            uuid=user_uuid,
            email=email,
            first_name=first_name,
            last_name=last_name,
            name=full_name,
            password=make_password(raw_password),
            account_type=account_type,
            active=active,
            reference=reference,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            new_onboarding=1,
            yt_verified=0 # Default from model check
        )
        
        # 4. Handle username generation
        if first_name and last_name:
            base_username = f"{first_name}-{last_name}".lower().replace(' ', '-')
            # Check for conflict
            if Users.objects.filter(username=base_username).exists():
                user.username = f"{base_username}-{user_uuid[-3:]}"
            else:
                user.username = base_username
            user.save()
            
        # 5. Role assignment
        if role_code:
            try:
                role = Roles.objects.get(code=role_code)
                UserRoles.objects.create(user=user, role=role)
            except Roles.DoesNotExist:
                pass # Or log error
                
        return user, raw_password

    def get_user_by_email(self, email):
        return Users.objects.filter(email=email).first()
