# Authentication and User Management Helper Functions

import secrets
import string
from django.utils import timezone
from datetime import timedelta

def generate_otp(length=6):
    """Generate a random OTP code"""
    return ''.join(secrets.choice(string.digits) for _ in range(length))

def generate_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def create_access_token(user):
    """Create a personal access token for the user"""
    from roster_api.models import PersonalAccessTokens
    import hashlib
    import secrets
    
    # Generate a unique token
    plain_token = secrets.token_urlsafe(40)
    hashed_token = hashlib.sha256(plain_token.encode()).hexdigest()
    
    # Create token record
    token = PersonalAccessTokens.objects.create(
        tokenable_type='App\\Models\\User',
        tokenable_id=user.id,
        name='auth',
        token=hashed_token[:64],  # Ensure it fits in the 64 char field
        abilities='*',
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return f"{token.id}|{plain_token}"

def verify_access_token(token_string):
    """Verify and return user from access token"""
    from roster_api.models import PersonalAccessTokens, Users
    import hashlib
    
    try:
        token_id, plain_token = token_string.split('|', 1)
        hashed_token = hashlib.sha256(plain_token.encode()).hexdigest()[:64]
        
        token = PersonalAccessTokens.objects.filter(
            id=token_id,
            token=hashed_token
        ).first()
        
        if not token:
            return None
            
        # Update last used timestamp
        token.last_used_at = timezone.now()
        token.save()
        
        # Get user
        user = Users.objects.filter(id=token.tokenable_id).first()
        return user
    except:
        return None

def send_otp_email(user, otp_code):
    """Send OTP code via email (placeholder - needs email service integration)"""
    # TODO: Integrate with SendGrid or email service
    print(f"OTP for {user.email}: {otp_code}")
    return True

def check_laravel_password(password, hashed):
    """
    Check password against hash, handling Laravel $2y$ bcrypt prefix.
    """
    from django.contrib.auth.hashers import check_password
    import bcrypt
    
    if hashed and hashed.startswith('$2y$'):
        # Laravel uses $2y$, python-bcrypt uses $2b$
        compatible_hash = '$2b$' + hashed[4:]
        try:
            return bcrypt.checkpw(password.encode('utf-8'), compatible_hash.encode('utf-8'))
        except Exception:
            return False
            
    # Fallback to standard Django check (PBKDF2, Argon2, or standard Bcrypt $2b$)
    return check_password(password, hashed)

