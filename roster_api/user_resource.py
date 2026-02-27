from django.db.models import F
from django.db.utils import OperationalError, ProgrammingError

from roster_api.serializers import (
    UserPricingSerializer,
    UserCreatorSerializer,
    UserSocialProfileSerializer,
)
from roster_api.models import (
    ContentVerticals,
    CreativeStyles,
    Equipment,
    JobTypes,
    Platforms,
    Skills,
    Software,
    UserJobTypes,
    UserLanguage,
    UserPricing,
    UserSocialProfile,
)


def _is_mysql_missing_table_or_column(exc: Exception) -> bool:
    """
    MySQL error codes we want to treat as "schema not present yet" in staging:
    - 1146: table doesn't exist
    - 1054: unknown column
    """
    args = getattr(exc, "args", None)
    if not args or not isinstance(args, (list, tuple)) or len(args) < 1:
        return False
    return args[0] in (1146, 1054)


def _basic_resource(obj):
    """
    Mirrors Laravel resources like UserSkillResource/UserPlatformResource/etc:
    { id: uuid, icon, name, description }
    """
    return {
        "id": getattr(obj, "uuid", None),
        "icon": getattr(obj, "icon", None),
        "name": getattr(obj, "name", None),
        "description": getattr(obj, "description", None),
    }

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
    
    # 2. Creators (best-effort)
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
    
    # Pricing (best-effort)
    try:
        pricing = UserPricing.objects.filter(user=user).first()
        pricing_data = UserPricingSerializer(pricing).data if pricing else None
    except Exception:
        pricing_data = None

    # Social profile (best-effort)
    try:
        social_profile = UserSocialProfile.objects.filter(user=user).first()
        social_profiles_data = UserSocialProfileSerializer(social_profile).data if social_profile else None
    except Exception:
        social_profiles_data = None

    # Foreign relations should match Laravel resources:
    # - skills/platforms/softwares/equipments/creative_styles/content_verticals -> related entity resources
    # - job_types -> related entity resource + primary_job from pivot
    try:
        skills_data = [_basic_resource(s) for s in Skills.objects.filter(userskills__user=user).distinct()]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            skills_data = []
        else:
            raise

    try:
        content_verticals_data = [
            _basic_resource(v)
            for v in ContentVerticals.objects.filter(usercontentverticals__user=user).distinct()
        ]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            content_verticals_data = []
        else:
            raise

    try:
        platforms_data = [_basic_resource(p) for p in Platforms.objects.filter(userplatforms__user=user).distinct()]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            platforms_data = []
        else:
            raise

    try:
        softwares_data = [_basic_resource(s) for s in Software.objects.filter(usersoftware__user=user).distinct()]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            softwares_data = []
        else:
            raise

    try:
        equipments_data = [_basic_resource(e) for e in Equipment.objects.filter(userequipments__user=user).distinct()]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            equipments_data = []
        else:
            raise

    try:
        creative_styles_data = [
            _basic_resource(cs) for cs in CreativeStyles.objects.filter(usercreativestyles__user=user).distinct()
        ]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            creative_styles_data = []
        else:
            raise

    try:
        job_types_data = [
            {
                **_basic_resource(jt),
                "primary_job": getattr(jt, "primary_job", None),
            }
            for jt in JobTypes.objects.filter(userjobtypes__user=user)
            .annotate(primary_job=F("userjobtypes__primary_job"))
            .distinct()
        ]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            job_types_data = []
        else:
            raise

    try:
        languages_data = [
            {"id": l.uuid, "proficiency": l.proficiency, "language": l.name}
            for l in UserLanguage.objects.filter(user=user).order_by("created_at")
        ]
    except (OperationalError, ProgrammingError) as e:
        if _is_mysql_missing_table_or_column(e):
            languages_data = []
        else:
            raise

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
        'social_profiles': social_profiles_data,
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

