from roster_api.serializers import (
    UserSkillSerializer, UserJobTypeSerializer, UserContentVerticalSerializer,
    UserPlatformSerializer, UserSoftwareSerializer, UserEquipmentSerializer,
    UserCreativeStyleSerializer, UserPricingSerializer, UserCreatorSerializer,
    UserLanguageSerializer, CustomerSerializer, UserJobTypes
)
from roster_api.models import UserPricing

def format_date(dt):
    """Format datetime as ISO string or return None"""
    if dt:
        return dt.isoformat()
    return None

def get_user_resource_dict(user):
    """
    Replicates the exact shape of Laravel's UserResource.toArray()
    """
    # 1. Helper fields
    # Handle primary job
    primary_job = None
    try:
        # UserJobTypes junction might have a 'primary_job' field if it exists
        job_types = user.userjobtypes_set.all()
        for jt in job_types:
            if getattr(jt, 'primary_job', 0) == 1:
                primary_job = jt.job_type.name if hasattr(jt, 'job_type') else None
                break
    except Exception:
        pass
    
    # 2. Creators
    # Simplified version of the Laravel logic which filters and sorts creators
    try:
        creators = user.usercreators_set.exclude(deleted_at__isnull=False)
        has_creators = creators.exists()
        creators_data = UserCreatorSerializer(creators, many=True).data
    except Exception:
        has_creators = False
        creators_data = []

    # 3. Activation & Verification
    is_activated = bool(user.activated_at)
    is_verified = bool(user.verified_at)
    
    # Pricing
    try:
        pricing = UserPricing.objects.filter(user=user).first()
        pricing_data = UserPricingSerializer(pricing).data if pricing else None
    except Exception:
        pricing_data = None

    # Foreign Relations (many-to-one or many-to-many through)
    try:
        skills_data = UserSkillSerializer(user.userskills_set.all(), many=True).data
    except Exception:
        skills_data = []

    try:
        job_types_data = UserJobTypeSerializer(user.userjobtypes_set.all(), many=True).data
    except Exception:
        job_types_data = []

    try:
        content_verticals_data = UserContentVerticalSerializer(user.usercontentverticals_set.all(), many=True).data
    except Exception:
        content_verticals_data = []

    try:
        platforms_data = UserPlatformSerializer(user.userplatforms_set.all(), many=True).data
    except Exception:
        platforms_data = []

    try:
        softwares_data = UserSoftwareSerializer(user.usersoftware_set.all(), many=True).data
    except Exception:
        softwares_data = []

    try:
        equipments_data = UserEquipmentSerializer(user.userequipments_set.all(), many=True).data
    except Exception:
        equipments_data = []

    try:
        creative_styles_data = UserCreativeStyleSerializer(user.usercreativestyles_set.all(), many=True).data
    except Exception:
        creative_styles_data = []
        
    try:
        languages_data = UserLanguageSerializer(user.userlanguage_set.all(), many=True).data
    except Exception:
        languages_data = []

    # Customer info
    customer_data = None
    try:
        customer = getattr(user, 'customers_set', None)
        if customer and customer.exists():
            c = customer.first()
            customer_data = {
                'payment_type': getattr(getattr(c, 'payment_type', None), 'name', None),
                'payment_status': getattr(getattr(c, 'payment_status', None), 'name', None),
            }
    except Exception:
        pass

    # Project stats
    try:
        projects_count = user.projects_set.count()
        has_min_1_project = projects_count >= 1
        has_min_3_projects = projects_count >= 3
    except Exception:
        has_min_1_project = False
        has_min_3_projects = False

    try:
        referral_count = user.referrals_set.count()
    except Exception:
        referral_count = 0

    return {
        'id': user.uuid,
        'db_id': user.id,
        'photo': user.photo,
        'name': user.name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'dob': format_date(user.dob) if user.dob else None,
        'gender': user.gender,
        'email': user.email,
        'email_verified_at': format_date(user.email_verified_at) if user.email_verified_at else None,
        'phone': user.phone,
        'phone_verified_at': format_date(user.phone_verified_at) if user.phone_verified_at else None,
        'address': user.address,
        'city': user.city.strip() if user.city else None,
        'country': user.country.strip() if user.country else None,
        'company': user.company,
        'job_title': primary_job if primary_job else user.job_title,
        'username': user.username,
        'fun_fact': user.fun_fact,
        'created_at': format_date(user.created_at) if user.created_at else None,
        'updated_at': format_date(user.updated_at) if user.updated_at else None,
        'activated_at': format_date(user.activated_at) if user.activated_at else None,
        'is_activated': is_activated,
        'verified_at': format_date(user.verified_at) if user.verified_at else None,
        'is_verified': is_verified,
        'open_for_work': bool(user.open_for_work),
        'active': bool(user.active),
        'completion': 0, # Placeholder for $this->completion(false)
        'account_type': user.account_type,
        'reference': user.reference,
        'utc_offset': float(user.utc_offset) if user.utc_offset is not None else None,
        'timezone': user.timezone,
        'referral_code': user.referral_code,
        'pricing': pricing_data,
        'skills': skills_data,
        'job_types': job_types_data,
        'content_verticals': content_verticals_data,
        'platforms': platforms_data,
        'softwares': softwares_data,
        'equipments': equipments_data,
        'creative_styles': creative_styles_data,
        'social_profiles': None, # new SocialProfileResource($this->social_profiles)
        'customer': customer_data,
        'creators': creators_data,
        'has_creators': has_creators,
        'has_min_1_project': has_min_1_project,
        'has_min_3_projects': has_min_3_projects,
        'has_creators_with_projects': None, # $this->has_creators_with_projects()
        'has_creative_styles': len(creative_styles_data) > 0,
        'has_creator_with_details': False, # Placeholder
        'resume': user.resume,
        'resume_updated_at': format_date(user.resume_updated_at) if user.resume_updated_at else None,
        'worked_with_creators': bool(user.worked_with_creators),
        'new_onboarding': bool(user.new_onboarding),
        'count_non_youtube_projects': 0, # Placeholder
        'via_affiliate': bool(user.via_affiliate),
        'email_unsubscriptions': None, # Field might not exist
        'import_via_linkedin': bool(user.import_via_linkedin),
        'import_via_resume': bool(user.import_via_resume),
        'languages': languages_data,
        'policy_accepted': bool(user.policy_accepted),
        'policy_accepted_at': format_date(user.policy_accepted_at) if user.policy_accepted_at else None,
        'referral_count': referral_count,
        'yt_verified': bool(user.yt_verified),
    }

