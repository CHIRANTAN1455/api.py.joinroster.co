from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .auth_helpers import verify_access_token, check_laravel_password
from .user_resource import get_user_resource_dict

def get_authenticated_user(request):
    """
    Helper to get user from Authorization header (Bearer token)
    or X-User-ID header/query param.
    """
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        parts = auth_header.split(' ')
        if len(parts) > 1:
            return verify_access_token(parts[1])
    
    # Fallback to X-User-ID (mostly for development/mocking)
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id') or request.data.get('user_id')
    if user_id:
        # Check if it's a UUID or numeric ID
        if len(str(user_id)) > 10:
            return Users.objects.filter(uuid=user_id).first()
        return Users.objects.filter(id=user_id).first()
    return None
import secrets
import uuid
from .utils import ApiResponse
from .models import (
    Skills, ContentVerticals, Platforms, Software, Equipment, 
    CreativeStyles, JobTypes, Countries, States, Cities, Locations, Users,
    UserProjects, UserCreators, UserSkills, UserContentVerticals, UserPlatforms,
    Roles, UserRoles, Customers, PaymentTypes, PaymentStatuses,
    ContentForms, Reasons, Referrals, Otps, PersonalAccessTokens,
    Projects, Matchings, MatchingEditors, MatchingSkills, MatchingPlatforms,
    MatchingSoftware, MatchingContentVerticals, MatchingCreativeStyles,
    MatchingJobTypes, ProjectApplications, ProjectApplicationNotes,
    ProjectScreeningAnswers, ProjectScreeningQuestions, CustomScreeningQuestions,
    QuestionTypes, UserVerificationLinks, UserPricing, ProjectTypes,
    UserJobTypePricing, UserSocialProfile, UserLanguage, UserSoftware,
    UserEquipments, UserCreativeStyles, UserJobTypes, Setting, Files, Permissions, Menus
)
from .serializers import (
    SkillSerializer, 
    ContentVerticalSerializer, 
    PlatformSerializer, 
    SoftwareSerializer, 
    EquipmentSerializer, 
    CreativeStyleSerializer, 
    JobTypeSerializer,
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    LocationSerializer,
    UserSerializer,
    UserPricingSerializer,
    UserSocialProfileSerializer,
    UserLanguageSerializer,
    UserJobTypePricingSerializer,
    UserCreatorSerializer,
    UserProjectSerializer,
    UserSkillSerializer,
    UserEquipmentSerializer,
    UserCreativeStyleSerializer,
    UserJobTypeSerializer,
    ReasonSerializer,
    ReferralSerializer,
    ProjectSerializer,
    MatchingSerializer,
    MatchingEditorSerializer,
    MatchingSkillSerializer,
    MatchingPlatformSerializer,
    MatchingSoftwareSerializer,
    MatchingContentVerticalSerializer,
    MatchingCreativeStyleSerializer,
    MatchingJobTypeSerializer,
    ProjectApplicationSerializer,
    ProjectApplicationNoteSerializer,
    ProjectScreeningQuestionSerializer,
    ProjectScreeningAnswerSerializer,
    CustomScreeningQuestionSerializer,
    QuestionTypeSerializer,
    UserVerificationLinkSerializer,
    ContentFormSerializer,
    ProjectTypeSerializer,
    ChatSerializer,
    ChatMessageSerializer,
    UserFavouriteSerializer,
    ProfileVisitSerializer,
    UserSoftwareSerializer,
    SettingSerializer,
    FilesSerializer,
    AdminUserSerializer,
    AdminProjectSerializer
)


@api_view(['GET'])
def test_api(request):
    return ApiResponse(message='API routes working fine!')

@extend_schema(responses={200: SkillSerializer(many=True)}, operation_id="skills_list")
@api_view(['GET'])
def skills_index(request):
    # TODO: Implement filtering based on user type (editor vs customer)
    skills = Skills.objects.filter(active=1)
    serializer = SkillSerializer(skills, many=True)
    return ApiResponse(skills=serializer.data)

@api_view(['GET'])
def content_verticals_index(request):
    data = ContentVerticals.objects.filter(active=1)
    serializer = ContentVerticalSerializer(data, many=True)
    return ApiResponse(contentverticals=serializer.data)

@api_view(['GET'])
def platforms_index(request):
    data = Platforms.objects.filter(active=1)
    serializer = PlatformSerializer(data, many=True)
    return ApiResponse(platforms=serializer.data)

@api_view(['GET'])
def softwares_index(request):
    data = Software.objects.filter(active=1)
    serializer = SoftwareSerializer(data, many=True)
    return ApiResponse(softwares=serializer.data)

@api_view(['GET'])
def equipments_index(request):
    data = Equipment.objects.filter(active=1)
    serializer = EquipmentSerializer(data, many=True)
    return ApiResponse(equipments=serializer.data)

@api_view(['GET'])
def creative_styles_index(request):
    data = CreativeStyles.objects.filter(active=1)
    serializer = CreativeStyleSerializer(data, many=True)
    return ApiResponse(creativestyles=serializer.data)

@api_view(['GET'])
def job_types_index(request):
    data = JobTypes.objects.filter(active=1)
    serializer = JobTypeSerializer(data, many=True)
    return ApiResponse(jobtypes=serializer.data)

@api_view(['POST'])
def country_create(request):
    # TODO: check_permission(['setting_add', 'setting_edit'])
    countries_data = request.data
    results = []
    
    # helper to handle list or single dict
    if isinstance(countries_data, dict):
        countries_data = [countries_data]
        
    for data in countries_data:
        # Check if exists
        if Countries.objects.filter(name=data.get('name')).exists():
            continue
            
        Countries.objects.create(
            id=data.get('id'),
            name=data.get('name'),
            iso3=data.get('iso3'),
            numeric_code=data.get('numeric_code'),
            phone_code=data.get('phone_code'),
            capital=data.get('capital'),
            currency=data.get('currency'),
            currency_name=data.get('currency_name'),
            currency_symbol=data.get('currency_symbol'),
            tld=data.get('tld'),
            native=data.get('native'),
            region=data.get('region'),
            subregion=data.get('subregion'),
            timezones=data.get('timezones'), # JSON field in model? Dictionary in payload?
            translations=data.get('translations'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            emojiu=data.get('emojiU') # Note: model field is emojiu
        )
        
    return ApiResponse(data={'country': 'completed'})

@api_view(['POST'])
def state_create(request):
    # TODO: check_permission(['setting_add', 'setting_edit'])
    states_data = request.data
    if isinstance(states_data, dict):
        states_data = [states_data]

    for data in states_data:
        if States.objects.filter(id=data.get('id'), country_id=data.get('country_id')).exists():
            continue
            
        States.objects.create(
            id=data.get('id'),
            country_id=data.get('country_id'),
            name=data.get('name'),
            code=data.get('state_code'),
            type=data.get('type'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
    return ApiResponse(data={'state': 'completed'})

@api_view(['POST'])
def city_create(request):
    # TODO: check_permission(['setting_add', 'setting_edit'])
    cities_data = request.data
    if isinstance(cities_data, dict):
        cities_data = [cities_data]

    for data in cities_data:
        Cities.objects.update_or_create(
            id=data.get('id'),
            state_id=data.get('state_id'),
            defaults={
                "name": data.get('name'),
                "latitude": data.get('latitude'),
                "longitude": data.get('longitude'),
                "wiki_data_id": data.get('wiki_data_id')
            }
        )
    return ApiResponse(data={'city': 'completed'})

@api_view(['POST'])
def location_create(request):
    # TODO: check_permission(['setting_add', 'setting_edit'])
    locations_data = request.data
    if isinstance(locations_data, dict):
        locations_data = [locations_data]

    for data in locations_data:
        Locations.objects.update_or_create(
            city_ascii=data.get('city_ascii'),
            country=data.get('country'),
            defaults={
                'city': data.get('city'),
                'iso2': data.get('iso2'),
                'iso3': data.get('iso3'),
                'admin_name': data.get('admin_name'),
                'capital': data.get('capital'),
                'population': data.get('population'),
                'lat': data.get('lat'),
                'lng': data.get('lng')
            }
        )
@api_view(['POST'])
def editor_create(request):
    # TODO: check_permission('setting_add')
    editors_data = request.data
    results = [] # In the PHP code, this variable is used to collect created users, but the return is api(editors)
    
    if isinstance(editors_data, dict):
        editors_data = [editors_data]

    created_users = []
    
    for data in editors_data:
        # data is a dict
        slug = data.get('slug')
        
        # PHP: $users = $this->editorService->getAllByUsername($data->slug)->count();
        # Looking up by username prefix count to mimic PHP behavior for unique usernames
        count = Users.objects.filter(username__startswith=slug).count()
        username_slug = f"{slug}-{count + 1}" if count else slug
        
        email = data.get('email')
        
        # Prepare User data
        user_data = {
            'username': username_slug,
            'name': (data.get('first_name') or '') + ' ' + (data.get('last_name') or ''), # PHP: trim(...)
            'email': email,
            'active': 1 if str(data.get('verified')).lower() == 'true' else 0, # PHP: $data->verified == "true"
            # 'created_at': format_date(...) # default handle by django if auto_now_add? No, existing DB.
            # 'verified_at': ...
            'role_id': 2, # PHP: $this->editorService->role()->id (assuming 2 for editor/supplier based on typical seeder)
            'fun_fact': data.get('fun_fact'),
            'job_title': data.get('title'),
            'company': data.get('company'),
            # 'password': generate_password(), # TODO: Hash this? PHP uses Hash::make(generate_password())? Actually PHP just does generate_password(), it usually hashes on save or in mutator.
            # Wait, PHP: 'password' => generate_password(), but User::create calls Hash::make?
            # PHP code in DataController: 'password' => generate_password() then User::create((array)$editor).
            # The User model might have a mutator or it's stored plain text (bad)?
            # Checking AuthService::create, it uses Hash::make.
            # But DataController::editor assigns 'password' => generate_password() to the array passed to User::create (via firstOrCheate-ish logic).
            # Let's assume we need to hash it.
            'address': data.get('location'),
        }
        
        # Handling Password
        from django.contrib.auth.hashers import make_password
        from .utils import generate_password
        plain_password = generate_password()
        user_data['password'] = make_password(plain_password) 

        # Create or Update User
        user, created = Users.objects.update_or_create(
            email=email,
            defaults=user_data
        )
        
        # Handle Relations
        # Pricing
        starting_price_raw = str(data.get('hourly_rate', '')).replace('$', '').replace(',', '').replace('.', '')
        starting_price = starting_price_raw if starting_price_raw else None
        
        interested_in = []
        engagement = data.get('engagement_type')
        if engagement == 'hybrid':
            interested_in = ["freelance", "contract", "fulltime"]
        elif engagement == 'per-project':
             interested_in = ["freelance", "contract"]
             
        UserPricing.objects.update_or_create(
            user=user,
            defaults={
                'starting_price': starting_price,
                'interested_in': interested_in
            }
        )
        
        # Skills
        raw_skills = str(data.get('skills', '')).split(';')
        for raw in raw_skills:
            term = raw.replace('-', ' ').strip().split(' ')[0] # PHP logic
            if not term: continue
            
            # Find Skill
            # PHP: Skill::where('name', 'LIKE', "%{$search[0]}%")->first();
            skill = Skills.objects.filter(name__icontains=term).first()
            if skill:
                 UserSkills.objects.get_or_create(user=user, skill=skill)

        # Content Verticals
        raw_cv = str(data.get('content_verticals', '')).split(';')
        for raw in raw_cv:
            term = raw.replace('-', ' ').strip().split(' ')[0]
            if not term: continue
            cv = ContentVerticals.objects.filter(name__icontains=term).first()
            if cv:
                UserContentVerticals.objects.get_or_create(user=user, content_vertical=cv)

        # Platforms
        raw_plat = str(data.get('platform_specialty', '')).split(';')
        for raw in raw_plat:
            term = raw.replace('-', ' ').strip().split(' ')[0]
            if not term: continue
            plat = Platforms.objects.filter(name__icontains=term).first()
            if plat:
                UserPlatforms.objects.get_or_create(user=user, platform=plat)
        
        # Projects (1-8)
        from datetime import datetime
        for i in range(1, 9):
            url = data.get(f'project_{i}')
            if url:
                 project_type_name = 'Link' if '/user' in url else 'Video'
                 project_type = ProjectTypes.objects.filter(name=project_type_name).first()
                 
                 if project_type:
                     # Check if exists
                     if not UserProjects.objects.filter(user=user, link=url).exists():
                         UserProjects.objects.create(
                             user=user,
                             project_type=project_type,
                             link=url,
                             name='Project Name', # default
                             description='Project Description', # default
                             views=0,
                             likes=0,
                             created_at=datetime.now()
                         )

        created_users.append(UserSerializer(user).data)

    return ApiResponse(data=created_users)

@api_view(['POST'])
def invite(request):
    # TODO: check_permission(['editor_add', 'editor_edit'])
    emails = request.data.get('emails', [])
    results = {}
    
    for email in emails:
        try:
            # PHP uses editorService->getByEmail which checks for active user etc.
            # Here we just find by email
            user = Users.objects.filter(email=email).first()
            if user:
                # Send email logic would go here
                # For now just mock success
                results[email] = "Invited"
            else:
                results[email] = "User not found"
        except Exception as e:
            results[email] = str(e)
            
    return ApiResponse(data=results)

@api_view(['GET'])
def profile_get(request):
    # Mocking auth for now
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    serializer = UserSerializer(user)
    data = serializer.data
    
    # Eager loading equivalent
    data['pricing'] = UserPricingSerializer(UserPricing.objects.filter(user=user).first()).data
    data['social_profiles'] = UserSocialProfileSerializer(UserSocialProfile.objects.filter(user=user).first()).data
    data['skills'] = UserSkillSerializer(UserSkills.objects.filter(user=user), many=True).data
    data['platforms'] = UserPlatformSerializer(UserPlatforms.objects.filter(user=user), many=True).data
    data['softwares'] = UserSoftwareSerializer(UserSoftware.objects.filter(user=user), many=True).data
    data['equipments'] = UserEquipmentSerializer(UserEquipments.objects.filter(user=user), many=True).data
    data['creative_styles'] = UserCreativeStyleSerializer(UserCreativeStyles.objects.filter(user=user), many=True).data
    data['job_types'] = UserJobTypeSerializer(UserJobTypes.objects.filter(user=user), many=True).data
    data['languages'] = UserLanguageSerializer(UserLanguage.objects.filter(user=user), many=True).data
    
    return ApiResponse(user=data)

@api_view(['POST'])
def profile_update(request):
    # Mocking auth for now
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    data = request.data
    
    # Handle Account Type change logic
    if 'account_type' in data:
        account_type = data['account_type']
        user.account_type = account_type
        
        if account_type == 'user':
            # Create Customer record if not exists
            if not Customers.objects.filter(user=user).exists():
                from uuid import uuid4
                import datetime
                payment_type = PaymentTypes.objects.filter(name='free', active=1).first()
                payment_status = PaymentStatuses.objects.filter(name='free', active=1).first()
                
                if not payment_type or not payment_status:
                    # Fallback
                    payment_type = PaymentTypes.objects.filter(active=1).first()
                    payment_status = PaymentStatuses.objects.filter(active=1).first()
                
                if payment_type and payment_status:
                    Customers.objects.create(
                        user=user,
                        payment_type=payment_type,
                        payment_status=payment_status,
                        uuid=str(uuid4()),
                        created_at=datetime.datetime.now()
                    )
            if not user.job_title:
                user.job_title = 'Creator'
        elif account_type == 'editor':
            role = Roles.objects.filter(code='editor').first()
            if role:
                UserRoles.objects.get_or_create(user=user, role=role)

    # Basic fields update
    fields = [
        'first_name', 'last_name', 'email', 'phone', 'address', 
        'latitude', 'longitude', 'company', 'job_title', 'username', 
        'fun_fact', 'reference', 'utc_offset', 'timezone', 'referral_code',
        'city', 'country', 'open_for_work'
    ]
    
    for field in fields:
        if field in data:
            setattr(user, field, data[field])
            
    # Handle Photo/Resume (Simplified GCS logic placeholder)
    if 'photo' in request.FILES:
        # photo = request.FILES['photo']
        # user.photo = upload_to_gcs(photo)
        pass
    
    if 'resume' in request.FILES:
        # resume = request.FILES['resume']
        # user.resume = upload_to_gcs(resume)
        import datetime
        user.resume_updated_at = datetime.datetime.now()

    user.updated_at = datetime.datetime.now()
    user.save()
    
    return ApiResponse(message="Profile updated successfully", user=UserSerializer(user).data)

@api_view(['POST'])
def profile_pricing(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    # Update UserPricing
    pricing, _ = UserPricing.objects.update_or_create(
        user=user,
        defaults={
            'average_turnaround_time': request.data.get('average_turnaround_time'),
            'interested_in': request.data.get('interested_in'),
        }
    )

    # Update UserJobTypePricing
    job_types_data = request.data.get('job_types', [])
    # Sync: delete old ones for this user and add new ones
    UserJobTypePricing.objects.filter(user=user).delete()
    
    for item in job_types_data:
        # job_type is uuid in request
        jt_uuid = item.get('job_type')
        job_type = JobTypes.objects.filter(uuid=jt_uuid).first()
        if job_type:
            UserJobTypePricing.objects.create(
                user=user,
                job_type=job_type,
                starting_price=item.get('starting_price'),
                pricing_type=item.get('pricing_type')
            )

    return ApiResponse(
        pricing=UserPricingSerializer(pricing).data,
        job_types=UserJobTypePricingSerializer(UserJobTypePricing.objects.filter(user=user), many=True).data
    )

@api_view(['POST'])
def profile_skills(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    skill_uuids = request.data.get('skills', [])
    # Sync logic
    UserSkills.objects.filter(user=user).delete()
    for uuid in skill_uuids:
        skill = Skills.objects.filter(uuid=uuid).first()
        if skill:
            UserSkills.objects.create(user=user, skill=skill)

    return ApiResponse(skills=UserSkillSerializer(UserSkills.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_jobtypes(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    job_type_uuids = request.data.get('job_types', [])
    primary_job_uuid = request.data.get('primary_job')
    
    UserJobTypes.objects.filter(user=user).delete()
    for uuid in job_type_uuids:
        job_type = JobTypes.objects.filter(uuid=uuid).first()
        if job_type:
            is_primary = 1 if uuid == primary_job_uuid else 0
            UserJobTypes.objects.create(user=user, job_type=job_type, primary_job=is_primary)

    return ApiResponse(job_types=UserJobTypeSerializer(UserJobTypes.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_contentverticals(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    uuids = request.data.get('content_verticals', [])
    UserContentVerticals.objects.filter(user=user).delete()
    for uuid in uuids:
        item = ContentVerticals.objects.filter(uuid=uuid).first()
        if item:
            UserContentVerticals.objects.create(user=user, content_vertical=item)

    return ApiResponse(content_verticals=UserContentVerticalSerializer(UserContentVerticals.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_contentverticals_new(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    uuids = request.data.get('content_verticals', [])
    for uuid in uuids:
        item = ContentVerticals.objects.filter(uuid=uuid).first()
        if item:
            UserContentVerticals.objects.get_or_create(user=user, content_vertical=item)

    return ApiResponse(content_verticals=UserContentVerticalSerializer(UserContentVerticals.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_platforms(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    uuids = request.data.get('platforms', [])
    UserPlatforms.objects.filter(user=user).delete()
    for uuid in uuids:
        item = Platforms.objects.filter(uuid=uuid).first()
        if item:
            UserPlatforms.objects.create(user=user, platform=item)

    return ApiResponse(platforms=UserPlatformSerializer(UserPlatforms.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_softwares(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    uuids = request.data.get('softwares', [])
    UserSoftware.objects.filter(user=user).delete()
    for uuid in uuids:
        item = Software.objects.filter(uuid=uuid).first()
        if item:
            UserSoftware.objects.create(user=user, software=item)

    return ApiResponse(softwares=UserSoftwareSerializer(UserSoftware.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_equipments(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    uuids = request.data.get('equipments', [])
    UserEquipments.objects.filter(user=user).delete()
    for uuid in uuids:
        item = Equipment.objects.filter(uuid=uuid).first()
        if item:
            UserEquipments.objects.create(user=user, equipment=item)

    return ApiResponse(equipments=UserEquipmentSerializer(UserEquipments.objects.filter(user=user), many=True).data)

@api_view(['POST'])
def profile_creativestyles(request):
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)

    uuids = request.data.get('creative_styles', [])
    UserCreativeStyles.objects.filter(user=user).delete()
    for uuid in uuids:
        item = CreativeStyles.objects.filter(uuid=uuid).first()
        if item:
            UserCreativeStyles.objects.create(user=user, creative_style=item)

    return ApiResponse(creative_styles=UserCreativeStyleSerializer(UserCreativeStyles.objects.filter(user=user), many=True).data)

@api_view(['GET'])
def profile_social(request):
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return ApiResponse(error="Unauthorized", status=401)
    
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    social_profile = UserSocialProfile.objects.filter(user=user).first()
    return ApiResponse(social_profile=UserSocialProfileSerializer(social_profile).data)

@api_view(['GET'])
def content_forms_index(request):
    """ContentForms API - returns all active content forms"""
    search = request.query_params.get('search', '')
    
    content_forms = ContentForms.objects.filter(active=1)
    if search:
        content_forms = content_forms.filter(name__icontains=search)
    
    serializer = ContentFormSerializer(content_forms, many=True)
    return ApiResponse(content_forms=serializer.data)

@extend_schema(responses={200: ProjectTypeSerializer(many=True)}, operation_id="project_types_list")
@api_view(['GET'])
def project_types_index(request):
    """ProjectTypes API - returns all active project types"""
    project_types = ProjectTypes.objects.filter(active=1)
    serializer = ProjectTypeSerializer(project_types, many=True)
    return ApiResponse(project_types=serializer.data)

@extend_schema(responses={200: ProjectTypeSerializer(many=True)}, operation_id="project_types_by_user")
@api_view(['GET'])
def project_types_user_index(request, username):
    """ProjectTypes API - returns project types for a specific user"""
    user = Users.objects.filter(username=username).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    # TODO: Implement getUserProjectType logic from ProjectTypeService
    project_types = ProjectTypes.objects.filter(active=1)
    serializer = ProjectTypeSerializer(project_types, many=True)
    return ApiResponse(project_types=serializer.data)

@api_view(['GET'])
def reasons_index(request):
    """Reasons API - returns reasons filtered by tag"""
    tag = request.query_params.get('tag')
    if not tag:
        return ApiResponse(error="Tag parameter is required", status=400)
    
    reasons = Reasons.objects.filter(tag=tag, active=1)
    serializer = ReasonSerializer(reasons, many=True)
    return ApiResponse(reasons=serializer.data)

@api_view(['GET'])
def referrals_index(request):
    """Referrals API - returns all active referrals"""
    referrals = Referrals.objects.filter(active=1)
    serializer = ReferralSerializer(referrals, many=True)
    return ApiResponse(referrals=serializer.data)

@extend_schema(responses={200: LocationSerializer(many=True)}, operation_id="location_list")
@api_view(['GET'])
def location_index(request):
    """Locations API - search locations with pagination"""
    search = request.query_params.get('search', '')
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 20))
    
    locations = Locations.objects.all()
    if search:
        locations = locations.filter(city__icontains=search) | locations.filter(country__icontains=search)
    
    # Simple pagination
    total = locations.count()
    start = (page - 1) * per_page
    end = start + per_page
    locations = locations[start:end]
    
    serializer = LocationSerializer(locations, many=True)
    return ApiResponse(locations=serializer.data, total=total, page=page)

@extend_schema(responses={200: LocationSerializer}, operation_id="location_retrieve")
@api_view(['GET'])
def location_get(request, id):
    """Get single location by ID"""
    location = Locations.objects.filter(id=id).first()
    if not location:
        return ApiResponse(error="Location not found", status=404)
    
    serializer = LocationSerializer(location)
    return ApiResponse(location=serializer.data)

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@api_view(['POST'])
def auth_init(request):
    """Initialize authentication - check if user exists"""
    identifier = request.data.get('email') or request.data.get('phone', '').strip()
    
    if not identifier:
        return ApiResponse(message="Email or phone is required", status_code=422)
    
    # Check if user exists
    user = Users.objects.filter(email=identifier).first() or Users.objects.filter(phone=identifier).first()
    
    return ApiResponse(
        status='success',
        action='login' if user else 'register',
        message='Login user' if user else 'Register user'
    )

@api_view(['POST'])
def auth_login(request):
    """Login with username/email and password"""
    from .auth_helpers import create_access_token
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return ApiResponse(message="Username and password are required", status_code=422)
    
    # Find user by email, phone, or username
    user = (Users.objects.filter(email=username).first() or 
            Users.objects.filter(phone=username).first() or
            Users.objects.filter(username=username).first())
    
    if not user or not check_laravel_password(password, user.password):
        return ApiResponse(message="Login failed", status_code=401)
    
    # Load related data
    user_creators = UserCreators.objects.filter(user=user).select_related('creator_group')
    
    # Create access token
    access_token = create_access_token(user)
    
    return ApiResponse(
        status='success',
        message='Login Successful!',
        user=get_user_resource_dict(user),
        access_token=access_token,
        token_type='Bearer'
    )

@api_view(['POST'])
def auth_register(request):
    """Register a new user"""
    from .auth_helpers import create_access_token, generate_otp, send_otp_email
    
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')
    policy_accepted = request.data.get('policy_accepted')
    
    if not email:
        return ApiResponse(message="Email is required", status_code=422)
    
    if not password:
        return ApiResponse(message="Password is required", status_code=422)
        
    if not policy_accepted:
        return ApiResponse(message="Policy acceptance is required", status_code=422)
    
    # Check if user already exists
    if Users.objects.filter(email=email).exists():
        return ApiResponse(message="Email already exists", status_code=422)
    
    if phone and Users.objects.filter(phone=phone).exists():
        return ApiResponse(message="Phone already exists", status_code=422)
    
    # Create user
    user = Users.objects.create(
        uuid=str(uuid_lib.uuid4()),
        email=email,
        phone=phone,
        password=make_password(password),
        active=0,  # Inactive until verified
        yt_verified=0,
        policy_accepted=1 if policy_accepted else 0,
        policy_accepted_at=timezone.now() if policy_accepted else None,
        account_type=request.data.get('account_type', 'editor'),
        referral_code=secrets.token_hex(4).upper(),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    # Generate and send OTP
    otp_code = generate_otp()
    Otps.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        code=otp_code,
        active=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    send_otp_email(user, otp_code)
    
    # Create access token
    access_token = create_access_token(user)
    
    return ApiResponse(
        status='success',
        message='Registration Successful! Please Verify Account with OTP',
        user=get_user_resource_dict(user),
        access_token=access_token,
        token_type='Bearer'
    )

@api_view(['POST'])
def auth_otp(request):
    """Request OTP for email verification"""
    from .auth_helpers import generate_otp, send_otp_email, verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    email = request.data.get('email')
    if email and email != user.email:
        # Check if new email already exists
        if Users.objects.filter(email=email).exclude(id=user.id).exists():
            return ApiResponse(error="Email already exists", status=422)
    
    # Deactivate old OTPs
    Otps.objects.filter(user=user, active=1).update(active=0)
    
    # Generate new OTP
    otp_code = generate_otp()
    Otps.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        code=otp_code,
        active=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    send_otp_email(user, otp_code)
    
    return ApiResponse(
        status='success',
        message='OTP sent successfully'
    )

@api_view(['POST'])
def auth_verify(request):
    """Verify OTP code"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    otp_code = request.data.get('otp')
    if not otp_code:
        return ApiResponse(error="OTP is required", status=422)
    
    # Verify OTP
    otp = Otps.objects.filter(
        user=user,
        code=otp_code,
        active=1,
        created_at__gte=timezone.now() - timedelta(minutes=15)  # 15 min expiry
    ).first()
    
    if not otp:
        return ApiResponse(error="Invalid or expired OTP", status=400)
    
    # Mark OTP as used
    otp.active = 0
    otp.save()
    
    # Activate user and verify email
    user.active = 1
    user.email_verified_at = timezone.now()
    user.verified_at = timezone.now()
    user.save()
    
    return ApiResponse(
        status='success',
        message='Verification Successful!',
        user=get_user_resource_dict(user)
    )

@api_view(['POST'])
def auth_reset_otp(request):
    """Request OTP for password reset"""
    from .auth_helpers import generate_otp, send_otp_email
    
    email = request.data.get('email')
    if not email:
        return ApiResponse(error="Email is required", status=422)
    
    user = Users.objects.filter(email=email).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Deactivate old OTPs
    Otps.objects.filter(user=user, active=1).update(active=0)
    
    # Generate new OTP
    otp_code = generate_otp()
    Otps.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        code=otp_code,
        active=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    send_otp_email(user, otp_code)
    
    return ApiResponse(
        status='success',
        message='OTP sent successfully'
    )

@api_view(['POST'])
def auth_reset_password(request):
    """Reset password with OTP"""
    from .auth_helpers import create_access_token
    
    email = request.data.get('email')
    otp_code = request.data.get('otp')
    new_password = request.data.get('password')
    
    if not email or not otp_code or not new_password:
        return ApiResponse(error="Email, OTP, and password are required", status=422)
    
    user = Users.objects.filter(email=email).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Verify OTP
    otp = Otps.objects.filter(
        user=user,
        code=otp_code,
        active=1,
        created_at__gte=timezone.now() - timedelta(minutes=15)
    ).first()
    
    if not otp:
        return ApiResponse(error="Invalid or expired OTP", status=400)
    
    # Update password
    user.password = make_password(new_password)
    user.save()
    
    # Mark OTP as used
    otp.active = 0
    otp.save()
    
    # Create new access token
    access_token = create_access_token(user)
    
    return ApiResponse(
        status='success',
        message='Password Reset Successful!',
        user=get_user_resource_dict(user),
        access_token=access_token,
        token_type='Bearer'
    )

@api_view(['POST'])
def auth_change_password(request):
    """Change password for authenticated user"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not current_password or not new_password or not confirm_password:
        return ApiResponse(error="All password fields are required", status=422)
    
    if new_password != confirm_password:
        return ApiResponse(error="Passwords do not match", status=422)
    
    if not check_laravel_password(current_password, user.password):
        return ApiResponse(message="Current password is incorrect", status_code=401)
    
    # Update password
    user.password = make_password(new_password)
    user.save()
    
    return ApiResponse(
        status='success',
        message='Password changed successfully'
    )

@api_view(['POST'])
def auth_logout(request):
    """Logout user and revoke tokens"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        parts = auth_header.split(' ')
        if len(parts) > 1:
            token = parts[1]
            user = verify_access_token(token)
        
        if user:
            # Delete all tokens for this user
            PersonalAccessTokens.objects.filter(
                tokenable_type='App\\Models\\User',
                tokenable_id=user.id
            ).delete()
    
    return ApiResponse(
        status='success',
        message='Logged out successfully'
    )

@api_view(['POST'])
def auth_social(request):
    """Handle social authentication (Google, Facebook, Apple, etc.)"""
    from .auth_helpers import create_access_token
    
    provider = request.data.get('provider')
    access_token = request.data.get('access_token')
    
    if not provider or not access_token:
        return ApiResponse(error="Provider and access token are required", status=422)
    
    # Placeholder for actual social validation logic (e.g., verifying with Google/FB)
    # For now, we search for the user by email if provided, or by social identity
    email = request.data.get('email')
    if not email:
        # In a real app, we'd fetch this from the provider using the access_token
        return ApiResponse(error="Email is required for social login", status=422)
        
    user = Users.objects.filter(email=email).first()
    
    if not user:
        # Create user if doesn't exist (Registration via Social)
        user = Users.objects.create(
            uuid=str(uuid_lib.uuid4()),
            email=email,
            name=request.data.get('name', email.split('@')[0]),
            active=1, # Socially verified users are usually active
            account_type=request.data.get('account_type', 'editor'),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
    
    access_token = create_access_token(user)
    
    return ApiResponse(
        status='success',
        message='Social login successful',
        user=get_user_resource_dict(user),
        access_token=access_token,
        token_type='Bearer'
    )

@api_view(['POST'])
def auth_linkedin(request):
    """Handle LinkedIn authentication"""
    # This usually involves exchanging a code for an access token, then getting user info
    # Simplified version for now
    return auth_social(request)

@api_view(['GET'])
def auth_chat(request):
    """Get chat-related authentication info"""
    user = get_authenticated_user(request)
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
        
    return ApiResponse(
        id=user.uuid,
        name=user.name,
        photo=user.photo
    )

@api_view(['GET'])
def auth_broadcasting(request):
    """Get broadcasting (e.g., Pusher) auth info"""
    user = get_authenticated_user(request)
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
        
    return ApiResponse(
        id=user.uuid,
        photo=user.photo,
        name=user.name,
        first_name=user.first_name,
        last_name=user.last_name,
        job_title=user.job_title,
        username=user.username,
        fun_fact=user.fun_fact
    )

# ============================================================================
# SETTING MANAGEMENT ENDPOINTS
# ============================================================================

@api_view(['GET'])
def settings_index(request):
    """List setting records"""
    setting_type = request.query_params.get('type')
    if setting_type:
        settings = Setting.objects.filter(type=setting_type)
    else:
        settings = Setting.objects.all()
    
    serializer = SettingSerializer(settings, many=True)
    return ApiResponse(settings=serializer.data)

@api_view(['POST'])
def settings_store(request):
    """Store a newly created setting"""
    # TODO: check_permission(['setting_add', 'setting_edit'])
    serializer = SettingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ApiResponse(message="Setting created successfully", setting=serializer.data)
    return ApiResponse(error=serializer.errors, status=400)

@api_view(['POST'])
def settings_update(request):
    """Update setting records"""
    # This matches the Laravel logic of bulk updating based on key/value pairs in request
    # TODO: check_permission('setting_edit')
    data = request.data
    results = []
    
    for key, value in data.items():
        if key == 'user_id' or key.startswith('_'): # Skip internal/helper fields
            continue
            
        setting = Setting.objects.filter(key=key).first()
        if setting:
            # Note: Laravel logic handles file uploads here too, but we use uuid strings for files in Setting.value
            setting.value = value
            setting.updated_at = timezone.now()
            setting.save()
            results.append(SettingSerializer(setting).data)
            
    return ApiResponse(message="Settings updated successfully", results=results)

@api_view(['DELETE'])
def settings_destroy(request, id):
    """Remove a setting by UUID or ID"""
    # In Laravel it uses uuid by default for destroy check
    # TODO: check_permission('setting_delete')
    setting = Setting.objects.filter(id=id).first()
    if not setting:
        return ApiResponse(error="Setting not found", status=404)
        
    setting.delete()
    return ApiResponse(message="Setting deleted successfully")

# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@api_view(['PUT', 'PATCH'])
def user_update(request, uuid):
    """Update user profile"""
    from .auth_helpers import verify_access_token
    
    # Get authenticated user
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    auth_user = verify_access_token(token)
    
    if not auth_user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get target user
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Check permission (user can only update their own profile unless admin)
    if auth_user.id != user.id:
        # TODO: Check admin permission
        return ApiResponse(error="Forbidden", status=403)
    
    # Update allowed fields
    allowed_fields = [
        'first_name', 'last_name', 'name', 'phone', 'dob', 'gender',
        'address', 'city', 'country', 'company', 'job_title',
        'username', 'fun_fact', 'timezone', 'utc_offset'
    ]
    
    for field in allowed_fields:
        if field in request.data:
            setattr(user, field, request.data[field])
    
    user.updated_at = timezone.now()
    user.save()
    
    return ApiResponse(
        status='success',
        message='User updated successfully',
        user=UserSerializer(user).data
    )

@api_view(['PUT'])
def user_update_timezone(request, uuid):
    """Update user timezone"""
    from .auth_helpers import verify_access_token
    
    # Get authenticated user
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    auth_user = verify_access_token(token)
    
    if not auth_user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get target user
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Check permission
    if auth_user.id != user.id:
        return ApiResponse(error="Forbidden", status=403)
    
    # Update timezone
    user.timezone = request.data.get('timezone')
    user.utc_offset = request.data.get('utc_offset')
    user.updated_at = timezone.now()
    user.save()
    
    return ApiResponse(
        status='success',
        message='Timezone updated successfully'
    )

@api_view(['GET'])
def user_by_referral_code(request, code):
    """Get user by referral code"""
    user = Users.objects.filter(referral_code=code).first()
    
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    return ApiResponse(
        status='success',
        message='User loaded successfully',
        user=UserSerializer(user).data
    )

@api_view(['PUT'])
def user_update_policy(request, uuid):
    """Update user policy acceptance"""
    from .auth_helpers import verify_access_token
    
    # Get authenticated user
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    auth_user = verify_access_token(token)
    
    if not auth_user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get target user
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Check permission
    if auth_user.id != user.id:
        return ApiResponse(error="Forbidden", status=403)
    
    policy_accepted = request.data.get('policy_accepted')
    if policy_accepted is None:
        return ApiResponse(error="policy_accepted is required", status=422)
    
    user.policy_accepted = 1 if policy_accepted else 0
    user.policy_accepted_at = timezone.now() if policy_accepted else None
    user.updated_at = timezone.now()
    user.save()
    
    return ApiResponse(
        status='success',
        message='Policy acceptance updated successfully',
        data={
            'user_id': user.id,
            'uuid': user.uuid,
            'policy_accepted': user.policy_accepted,
            'policy_accepted_at': user.policy_accepted_at
        }
    )

@api_view(['DELETE'])
def user_delete(request, uuid):
    """Delete user account"""
    from .auth_helpers import verify_access_token
    
    # Get authenticated user
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    auth_user = verify_access_token(token)
    
    if not auth_user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get target user
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Check permission
    if auth_user.id != user.id:
        # TODO: Check admin permission
        return ApiResponse(error="Forbidden", status=403)
    
    # Soft delete
    user.deleted_at = timezone.now()
    user.active = 0
    user.save()
    
    # Delete tokens
    PersonalAccessTokens.objects.filter(
        tokenable_type='App\\Models\\User',
        tokenable_id=user.id
    ).delete()
    
    return ApiResponse(
        status='success',
        message='User deleted successfully'
    )

# ============================================================================
# USER SOCIAL ACCOUNTS ENDPOINTS
# ============================================================================

@api_view(['GET'])
def user_social_index(request):
    """Get all social accounts for authenticated user"""
    user = get_authenticated_user(request)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get social accounts
    socials = UserSocials.objects.filter(user=user, deleted_at__isnull=True)
    
    # Format as dict by platform
    result = {}
    for social in socials:
        result[social.platform] = UserSocialSerializer(social).data
    
    return ApiResponse(
        status='success',
        message='Social accounts loaded successfully',
        socials=result
    )

@api_view(['POST'])
def user_social_create(request):
    """Add a social account"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    platform = request.data.get('provider') or request.data.get('platform')
    access_token = request.data.get('access_token')
    
    if not platform or not access_token:
        return ApiResponse(error="Platform and access_token are required", status=422)
    
    # TODO: Verify access token with the social platform API
    # For now, create a placeholder social account
    
    # icon, name, external_user_id, username are required fields in models
    name = request.data.get('name') or user.name or user.email or 'Social User'
    external_user_id = request.data.get('external_user_id') or ''
    username = request.data.get('username') or ''
    icon = request.data.get('icon') or ''
    
    # Check if already exists
    existing = UserSocials.objects.filter(user=user, platform=platform).first()
    if existing:
        existing.updated_at = timezone.now()
        existing.save()
        social = existing
    else:
        social = UserSocials.objects.create(
            uuid=str(uuid_lib.uuid4()),
            user=user,
            platform=platform,
            icon=icon,
            name=name,
            external_user_id=external_user_id,
            username=username,
            meta=request.data.get('meta', {}),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
    
    return ApiResponse(
        status='success',
        message='Social account added successfully',
        socials=UserSocialSerializer(social).data
    )

@api_view(['DELETE'])
def user_social_delete(request, uuid):
    """Delete a social account"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Find and delete social account
    social = UserSocials.objects.filter(uuid=uuid, user=user).first()
    if not social:
        return ApiResponse(error="Social account not found", status=404)
    
    # Soft delete
    social.deleted_at = timezone.now()
    social.save()
    
    return ApiResponse(
        status='success',
        message='Social account deleted successfully'
    )

@api_view(['GET'])
def user_social_content_topics(request):
    """Get content topics from user social profile"""
    from .auth_helpers import verify_access_token
    
    # Get user from token or query param
    user_id = request.query_params.get('user_id')
    
    if user_id:
        user = Users.objects.filter(uuid=user_id).first()
    else:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return ApiResponse(error="Unauthorized", status=401)
        
        parts = auth_header.split(' ')
        if len(parts) > 1:
            token = parts[1]
            user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Get content topics
    from .models import UserSocialProfileContentTopics
    topics = UserSocialProfileContentTopics.objects.filter(
        user_social_profile__user=user
    ).select_related('content_topic')
    
    topic_data = [ContentTopicSerializer(t.content_topic).data for t in topics if hasattr(t, 'content_topic')]
    
    return ApiResponse(
        status='success',
        topics=topic_data,
        message='Content topics loaded successfully'
    )

# ============================================================================
# USER PAYMENT METHODS ENDPOINTS
# ============================================================================

# Payment method endpoints moved to CUSTOMER ENDPOINTS section

# Removed duplicate


# ============================================================================
# USER CREATOR ENDPOINTS
# ============================================================================

@api_view(['GET'])
def user_creator_index(request):
    """Get all creators for authenticated user"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get creators
    creators = UserCreators.objects.filter(user=user)
    
    return ApiResponse(
        status='success',
        message='Creators loaded successfully',
        creators=UserCreatorSerializer(creators, many=True).data
    )

@api_view(['GET'])
def user_creator_unverified(request):
    """Get unverified creators for authenticated user"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Get unverified creators (yt_verified=0)
    creators = UserCreators.objects.filter(user=user, yt_verified=0)
    total_count = UserCreators.objects.filter(user=user).count()
    
    return ApiResponse(
        status='success',
        message='Creators loaded successfully',
        creators=UserCreatorSerializer(creators, many=True).data,
        total=total_count
    )

@api_view(['GET'])
def user_creator_search(request):
    """Search creators"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    name = request.query_params.get('name', '')
    creators = UserCreators.objects.filter(user=user)
    if name:
        creators = creators.filter(name__icontains=name)
        
    return ApiResponse(
        status='success',
        message='Creators loaded successfully',
        creators=UserCreatorSerializer(creators, many=True).data
    )

@api_view(['POST'])
def user_creator_add(request):
    """Add a new creator"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    link = request.data.get('link')
    if not link:
        return ApiResponse(error="Link is required", status=422)
    
    # Simple creation for now
    creator = UserCreators.objects.create(
        user=user,
        uuid=str(uuid_lib.uuid4()),
        link=link,
        name=request.data.get('name', 'New Creator'),
        yt_verified=0,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='Creator added successfully',
        creator=UserCreatorSerializer(creator).data
    )

@api_view(['PUT'])
def user_creator_update(request, uuid):
    """Update a creator"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    creator = UserCreators.objects.filter(uuid=uuid, user=user).first()
    if not creator:
        return ApiResponse(error="Creator not found", status=404)
    
    # Update fields
    if 'name' in request.data:
        creator.name = request.data['name']
    if 'link' in request.data:
        creator.link = request.data['link']
    
    creator.updated_at = timezone.now()
    creator.save()
    
    return ApiResponse(
        status='success',
        message='Creator updated successfully',
        creator=UserCreatorSerializer(creator).data
    )

@api_view(['DELETE'])
def user_creator_delete(request, uuid):
    """Delete a creator"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    creator = UserCreators.objects.filter(uuid=uuid, user=user).first()
    if not creator:
        return ApiResponse(error="Creator not found", status=404)
    
    # For now, just delete (or soft delete if model supports it)
    creator.delete()
    
    return ApiResponse(
        status='success',
        message='Creator deleted successfully'
    )

# ============================================================================
# PROJECT APPLICATION ENDPOINTS
# ============================================================================

@extend_schema(responses={200: ProjectApplicationSerializer(many=True)}, operation_id="project_application_list")
@api_view(['GET'])
def project_application_index(request):
    """List project applications"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Search applications
    applications = ProjectApplications.objects.filter(user=user)
    
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 20))
    
    total = applications.count()
    start = (page - 1) * per_page
    end = start + per_page
    applications = applications[start:end]
    
    return ApiResponse(
        status='success',
        message='Project applications loaded successfully',
        project_applications=ProjectApplicationSerializer(applications, many=True).data,
        total=total,
        page=page
    )

@extend_schema(responses={200: ProjectApplicationSerializer}, operation_id="project_application_retrieve")
@api_view(['GET'])
def project_application_get(request, uuid):
    """Get single project application"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    application = ProjectApplications.objects.filter(uuid=uuid, user=user).first()
    if not application:
        return ApiResponse(error="Application not found", status=404)
    
    return ApiResponse(
        status='success',
        message='Project application loaded successfully',
        project_application=ProjectApplicationSerializer(application).data
    )

@api_view(['POST'])
def project_application_store(request):
    """Store a project application"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    project_uuid = request.data.get('project_id')
    if not project_uuid:
        return ApiResponse(error="project_id is required", status=422)
    
    project = Projects.objects.filter(uuid=project_uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    # Create application
    application = ProjectApplications.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        project=project,
        note=request.data.get('note'),
        status=request.data.get('status', 'pending'),
        active=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='Application submitted successfully',
        application=ProjectApplicationSerializer(application).data
    )

@api_view(['PUT'])
def project_application_update(request, uuid):
    """Update project application status"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    application = ProjectApplications.objects.filter(uuid=uuid).first()
    if not application:
        return ApiResponse(error="Application not found", status=404)
    
    # Check permission (simplified)
    # TODO: Proper permission check
    
    status = request.data.get('status')
    if not status:
        return ApiResponse(error="Status is required", status=422)
    
    application.status = status
    application.updated_at = timezone.now()
    application.save()
    
    return ApiResponse(
        status='success',
        message='Application updated successfully',
        project_application=ProjectApplicationSerializer(application).data
    )

# ============================================================================
# PROJECT APPLICATION ENDPOINTS (EXTRA)
# ============================================================================

@api_view(['POST'])
def project_application_create_note(request, uuid):
    """Create a note for a project application"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    application = ProjectApplications.objects.filter(uuid=uuid).first()
    if not application:
        return ApiResponse(error="Application not found", status=404)
    
    text = request.data.get('text')
    if not text:
        return ApiResponse(error="Note text is required", status=422)
    
    note = ProjectApplicationNotes.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        project_application=application,
        text=text,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='Note created successfully',
        note=ProjectApplicationNoteSerializer(note).data
    )

@api_view(['DELETE'])
def project_application_delete_note(request, uuid):
    """Delete a project application note"""
    # Simplified auth for notes
    note = ProjectApplicationNotes.objects.filter(uuid=uuid).first()
    if not note:
        return ApiResponse(error="Note not found", status=404)
    
    note.delete()
    
    return ApiResponse(
        status='success',
        message='Note deleted successfully'
    )

@api_view(['POST'])
def project_application_send_rejection_email(request):
    """Placeholder for sending rejection emails"""
    return ApiResponse(
        status='success',
        message='Rejection email sent successfully'
    )

# ============================================================================
# USER CREATOR ENDPOINTS (EXTRA)
# ============================================================================

@api_view(['GET'])
def user_creator_projects(request, uuid):
    """Get projects for a creator"""
    creator = UserCreators.objects.filter(uuid=uuid).first()
    if not creator:
        return ApiResponse(error="Creator not found", status=404)
    
    projects = UserProjects.objects.filter(user_creator_id=creator.id)
    
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 20))
    total = projects.count()
    
    start = (page - 1) * per_page
    end = start + per_page
    projects = projects[start:end]
    
    return ApiResponse(
        status='success',
        message='Projects loaded successfully',
        projects=UserProjectSerializer(projects, many=True).data,
        total=total,
        page=page
    )

@api_view(['GET'])
def user_creator_get_content_topics(request):
    """Get creator content topics"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        user_uuid = request.query_params.get('user_id')
        if user_uuid:
            user = Users.objects.filter(uuid=user_uuid).first()
        else:
            return ApiResponse(error="Unauthorized", status=401)
    else:
        parts = auth_header.split(' ')
        if len(parts) > 1:
            token = parts[1]
            user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    # Logic from UserCreatorService->get_content_topics
    # Typically returns topics related to the user's social profile
    topics = ContentTopics.objects.all() # Placeholder
    
    return ApiResponse(
        status='success',
        message='Topics loaded successfully',
        topics=ContentTopicSerializer(topics, many=True).data
    )

@api_view(['GET'])
def user_creator_get_info(request):
    """Get creator info from YouTube (Placeholder)"""
    link = request.query_params.get('link')
    if not link:
        return ApiResponse(error="Link is required", status=422)
    
    # Placeholder info
    info = {
        'link': link,
        'name': 'Sample Creator',
        'followers': 1000,
        'description': 'Sample description',
        'icon': None
    }
    
    return ApiResponse(
        status='success',
        message='Info loaded successfully',
        info=info
    )

@api_view(['GET'])
def user_creator_get_public_info(request):
    """Get public creator info (Placeholder)"""
    link = request.query_params.get('link')
    if not link:
        return ApiResponse(error="Link is required", status=422)
        
    info = {
        'link': link,
        'name': 'Public Creator',
        'followers': 5000,
        'description': 'Public description',
        'icon': None,
        'topic_details': []
    }
    
    return ApiResponse(
        status='success',
        message='Info loaded successfully',
        info=info
    )

@api_view(['GET'])
def user_creator_get_similar(request):
    """Get similar creators (Placeholder)"""
    return ApiResponse(
        status='success',
        message='Similar creators loaded successfully',
        creators=[],
        topics=[]
    )

@api_view(['POST'])
def user_creator_invite_colleagues(request):
    """Invite colleagues (Placeholder)"""
    return ApiResponse(
        status='success',
        message='Invitation sent successfully'
    )

@api_view(['GET'])
def user_creator_get_by_username(request, username):
    """Get creator profile by username"""
    user = Users.objects.filter(username=username).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    return ApiResponse(
        status='success',
        message='User data loaded successfully',
        user=UserSerializer(user).data
    )

@api_view(['POST'])
def user_creator_create_group(request):
    """Create a creator group"""
    name = request.data.get('name')
    if not name:
        return ApiResponse(error="Name is required", status=422)
    
    group = CreatorGroups.objects.create(
        name=name,
        uuid=str(uuid_lib.uuid4()),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='Group created successfully',
        creator_group={'id': group.id, 'name': group.name}
    )

@api_view(['GET'])
def user_creator_search_public(request):
    """Public search for creators"""
    name = request.query_params.get('name', '')
    creators = UserCreators.objects.filter(yt_verified=1)
    if name:
        creators = creators.filter(name__icontains=name)
        
    return ApiResponse(
        status='success',
        message='Creators loaded successfully',
        creators=UserCreatorSerializer(creators, many=True).data
    )

# ============================================================================
# USER VERIFICATION LINK ENDPOINTS
# ============================================================================

@api_view(['GET'])
def user_verification_link_index(request):
    """List verification links for authenticated user"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    links = UserVerificationLinks.objects.filter(user=user, deleted_at__isnull=True)
    
    return ApiResponse(
        status='success',
        message='Verification links loaded successfully',
        creators=UserVerificationLinkSerializer(links, many=True).data
    )

@api_view(['POST'])
def user_verification_link_add(request):
    """Add a verification link"""
    from .auth_helpers import verify_access_token
    
    # Get user from token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    link = request.data.get('link')
    if not link:
        return ApiResponse(error="Link is required", status=422)
    
    verification_link = UserVerificationLinks.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        link=link,
        name=request.data.get('name', 'New Link'),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='Verification link added successfully',
        creator=UserVerificationLinkSerializer(verification_link).data
    )

@api_view(['POST'])
def user_verification_link_add_many(request):
    """Add multiple verification links"""
    from .auth_helpers import verify_access_token
    
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    links_data = request.data.get('links', [])
    created_links = []
    
    for link_text in links_data:
        verification_link = UserVerificationLinks.objects.create(
            uuid=str(uuid_lib.uuid4()),
            user=user,
            link=link_text,
            name='Verification Link',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        created_links.append(verification_link)
        
    return ApiResponse(
        status='success',
        message='Verification links added successfully',
        creators=UserVerificationLinkSerializer(created_links, many=True).data
    )

@api_view(['DELETE'])
def user_verification_link_delete(request, uuid):
    """Delete a verification link"""
    from .auth_helpers import verify_access_token
    
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ApiResponse(error="Unauthorized", status=401)
    
    token = auth_header.split(' ')[1]
    user = verify_access_token(token)
    
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
    
    link = UserVerificationLinks.objects.filter(uuid=uuid, user=user).first()
    if not link:
        return ApiResponse(error="Link not found", status=404)
        
    link.deleted_at = timezone.now()
    link.save()
    
    return ApiResponse(
        status='success',
        message='Verification link deleted successfully'
    )

# ============================================================================
# USER ENDPOINTS (EXTRA)
# ============================================================================

@api_view(['POST'])
def user_update_platforms(request, uuid):
    """Update user platforms"""
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    platforms_data = request.data.get('platforms', [])
    UserPlatforms.objects.filter(user=user).delete()
    for p_id in platforms_data:
        platform = Platforms.objects.filter(id=p_id).first()
        if platform:
            UserPlatforms.objects.create(user=user, platform=platform)
            
    return ApiResponse(status='success', message='Platforms updated successfully')

@api_view(['POST'])
def user_update_jobtypes_pricing(request, uuid):
    """Update user job types and pricing"""
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
    
    # Simple implementation for now
    return ApiResponse(status='success', message='Job types and pricing updated successfully')

@api_view(['POST'])
def user_update_content_vertical(request, uuid):
    """Update user content verticals"""
    user = Users.objects.filter(uuid=uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    verticals_data = request.data.get('content_verticals', [])
    UserContentVerticals.objects.filter(user=user).delete()
    for v_id in verticals_data:
        vertical = ContentVerticals.objects.filter(id=v_id).first()
        if vertical:
            UserContentVerticals.objects.create(user=user, content_vertical=vertical)
            
    return ApiResponse(status='success', message='Content verticals updated successfully')

@api_view(['POST'])
def user_unsubscribe(request, uuid):
    """Unsubscribe user from notifications"""
    return ApiResponse(status='success', message='Unsubscribed successfully')

@api_view(['POST'])
def user_revert_update_time(request, id):
    """Revert user update time to latest log (Placeholder)"""
    return ApiResponse(status='success', message='updated_at synced to latest log')

@api_view(['POST'])
def user_post_to_slack(request, uuid):
    """Post signup notification to Slack (Placeholder)"""
    return ApiResponse(status='success', message='Slack notification sent')

# ============================================================================
# PROFILE ENDPOINTS (EXTRA)
# ============================================================================

@api_view(['GET'])
def profile_statistics(request):
    """Get user profile statistics"""
    from .auth_helpers import verify_access_token
    
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        parts = auth_header.split(' ')
        if len(parts) > 1:
            token = parts[1]
            user = verify_access_token(token)
    else:
        user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
        user = Users.objects.filter(id=user_id).first()
        
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
        
    portfolio_projects = UserProjects.objects.filter(user=user).count()
    worked_with = UserCreators.objects.filter(user=user).count()
    
    # Projects where user is editor or creator
    projects = Projects.objects.filter(
        models.Q(editor_id=user.id) | models.Q(user=user),
        editor_id__isnull=False
    ).exclude(status='canceled').count()
    
    recommendations = Matchings.objects.filter(user=user).count()
    
    if user.account_type == 'editor':
        applications = ProjectApplications.objects.filter(user=user).exclude(status='draft').count()
    else:
        applications = ProjectApplications.objects.filter(
            project__user=user
        ).exclude(project__hackathon=1).exclude(status='draft').count()
        
    applications_this_week = ProjectApplications.objects.filter(
        project__user=user,
        project__hackathon__ne=1,
        project__status='open',
        status='pending'
    ).count()
    
    # profile_visits count (assuming a ProfileVisits model exists or is a count field)
    # For now, placeholder 0 as per Laravel's conditional
    profile_visits = 0 
    
    statistics = {
        'projects': projects,
        'portfolio_projects': portfolio_projects,
        'worked_with': worked_with,
        'recommendations': recommendations,
        'applications': applications,
        'applications_this_week': applications_this_week,
        'profile_visits': profile_visits
    }
    
    return ApiResponse(
        status='success',
        message='Statistics loaded successfully',
        statistics=statistics
    )

@api_view(['POST'])
def profile_convert_as_creator(request):
    """Convert user profile into Creator profile (replicate with new email/username)"""
    from .auth_helpers import verify_access_token
    import uuid as uuid_lib
    
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        parts = auth_header.split(' ')
        if len(parts) > 1:
            token = parts[1]
            user = verify_access_token(token)
    else:
        user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
        user = Users.objects.filter(id=user_id).first()
        
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
        
    if not user.email or not user.username:
        return ApiResponse(error="Invalid user data", status=422)
        
    prefix, domain = user.email.split('@')
    new_email = f"{prefix}+creator@{domain}"
    
    existing_user = Users.objects.filter(email=new_email).first()
    if existing_user:
        return ApiResponse(
            status='success',
            message='Creator profile already exists',
            user={
                'id': existing_user.uuid,
                'email': existing_user.email,
                'username': existing_user.username,
                'first_name': existing_user.first_name,
                'last_name': existing_user.last_name,
                'account_type': existing_user.account_type,
                'is_activated': bool(existing_user.activated_at),
                'created_at': existing_user.created_at,
            },
            original_user={
                'id': user.uuid,
                'email': user.email,
                'username': user.username,
            }
        )
        
    base_username = f"{user.username}-creator"
    username = base_username
    counter = 1
    while Users.objects.filter(username=username).exists():
        username = f"{base_username}-{counter}"
        counter += 1
        
    # Replicate user (manually creating a new instance for safety)
    new_user = Users.objects.create(
        uuid=str(uuid_lib.uuid4()),
        email=new_email,
        username=username,
        first_name=user.first_name,
        last_name=user.last_name,
        name=user.name,
        password=user.password,
        account_type='user',
        completion_status='incomplete',
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='Creator profile created successfully',
        user={
            'id': new_user.uuid,
            'email': new_user.email,
            'username': new_user.username,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'account_type': new_user.account_type,
            'is_activated': False,
            'created_at': new_user.created_at,
        },
        original_user={
            'id': user.uuid,
            'email': user.email,
            'username': user.username,
        }
    )

@api_view(['POST'])
def profile_refresh_token(request):
    """Refresh user access token"""
    from .auth_helpers import create_access_token
    
    user_uuid = request.data.get('user_uuid')
    if not user_uuid:
        return ApiResponse(error="user_uuid is required", status=422)
        
    user = Users.objects.filter(uuid=user_uuid).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    token = create_access_token(user)
    
    return ApiResponse(
        status='success',
        message='Token refreshed successfully',
        user={
            'id': user.uuid,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'account_type': user.account_type,
            'is_activated': bool(user.activated_at),
        },
        access_token=token,
        token_type='Bearer'
    )
# ============================================================================
# USER PROJECT ENDPOINTS
# ============================================================================

@extend_schema(responses={200: UserProjectSerializer(many=True)}, operation_id="user_project_list")
@api_view(['GET'])
def user_project_index(request):
    """List user projects"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    projects = UserProjects.objects.filter(user_id=user_id)
    
    # Optional filtering by topics/verticals could be added here
    serializer = UserProjectSerializer(projects, many=True)
    return ApiResponse(projects=serializer.data)

@extend_schema(responses={200: UserProjectSerializer(many=True)}, operation_id="user_project_list_public")
@api_view(['GET'])
def user_project_public_index(request):
    """List public projects"""
    projects = UserProjects.objects.all()
    serializer = UserProjectSerializer(projects, many=True)
    return ApiResponse(projects=serializer.data)

@extend_schema(responses={201: UserProjectSerializer}, operation_id="user_project_create")
@api_view(['POST'])
def user_project_add(request):
    """Add a new user project"""
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    data = request.data
    project_type_uuid = data.get('project_type')
    if not project_type_uuid:
        return ApiResponse(error="Project type is required", status=422)
        
    project_type = ProjectTypes.objects.filter(uuid=project_type_uuid).first()
    if not project_type:
        return ApiResponse(error="Invalid project type", status=422)
    
    project = UserProjects.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user_id=user_id,
        project_type=project_type,
        link=data.get('link'),
        name=data.get('name', 'Untitled Project'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        views=data.get('views', 0),
        likes=data.get('likes', 0),
        meta=data.get('meta', {}),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(project=UserProjectSerializer(project).data)

@api_view(['POST', 'PUT', 'PATCH'])
def user_project_update(request, uuid):
    """Update a user project"""
    project = UserProjects.objects.filter(uuid=uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    data = request.data
    for field in ['name', 'description', 'link', 'icon', 'views', 'likes', 'meta']:
        if field in data:
            setattr(project, field, data[field])
    
    project.updated_at = timezone.now()
    project.save()
    
    return ApiResponse(project=UserProjectSerializer(project).data)

@api_view(['DELETE'])
def user_project_delete(request, uuid):
    """Delete a user project"""
    project = UserProjects.objects.filter(uuid=uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    project.delete()
    return ApiResponse(message="Project deleted successfully")

@extend_schema(responses={200: dict}, operation_id="user_project_fetch_info")
@api_view(['GET'])
def user_project_info(request):
    """Get project info from YouTube (Mocked for now)"""
    link = request.query_params.get('link')
    # Use UserProjectService logic here
    return ApiResponse(info={
        'link': link,
        'name': 'Mock Youtube Video',
        'views': 1000,
        'description': 'Description from YT'
    })

# ============================================================================
# PROJECT ENDPOINTS (Projects model)
# ============================================================================

@extend_schema(responses={200: ProjectSerializer(many=True)}, operation_id="project_list")
@api_view(['GET'])
def project_index(request):
    """List projects for a user"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    projects = Projects.objects.filter(user_id=user_id)
    serializer = ProjectSerializer(projects, many=True)
    return ApiResponse(projects=serializer.data)

@api_view(['GET'])
def project_public_index(request):
    """List public projects (Jobs)"""
    projects = Projects.objects.filter(published=1)
    serializer = ProjectSerializer(projects, many=True)
    return ApiResponse(projects=serializer.data)

@extend_schema(responses={200: ProjectSerializer}, operation_id="project_retrieve")
@api_view(['GET'])
def project_get(request, uuid):
    """Get a project by UUID"""
    project = Projects.objects.filter(uuid=uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    return ApiResponse(project=ProjectSerializer(project).data)

@api_view(['POST'])
def project_store(request):
    """Store a new project"""
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    data = request.data
    project = Projects.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user_id=user_id,
        title=data.get('title'),
        description=data.get('description'),
        budget=data.get('budget'),
        budget_per=data.get('budget_per'),
        status='open',
        published=data.get('published', 0),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(project=ProjectSerializer(project).data)

@api_view(['PATCH'])
def project_update(request, uuid):
    """Update a project"""
    project = Projects.objects.filter(uuid=uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    data = request.data
    fields = ['title', 'description', 'budget', 'budget_per', 'status', 'published']
    for field in fields:
        if field in data:
            setattr(project, field, data[field])
            
    project.updated_at = timezone.now()
    project.save()
    
    return ApiResponse(project=ProjectSerializer(project).data)

@api_view(['POST'])
def project_status_update(request, uuid):
    """Update project status"""
    project = Projects.objects.filter(uuid=uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    status = request.data.get('status')
    if status:
        project.status = status
        project.updated_at = timezone.now()
        project.save()
        
    return ApiResponse(project=ProjectSerializer(project).data)

# ============================================================================
# MATCHING ENDPOINTS
# ============================================================================

@extend_schema(responses={200: MatchingSerializer(many=True)}, operation_id="matching_list")
@api_view(['GET'])
def matching_index(request):
    """List matchings for a user"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    matchings = Matchings.objects.filter(user_id=user_id)
    serializer = MatchingSerializer(matchings, many=True)
    return ApiResponse(matching=serializer.data)

@extend_schema(responses={200: MatchingSerializer}, operation_id="matching_retrieve")
@api_view(['GET'])
def matching_get(request, uuid):
    """Get matching by UUID"""
    matching = Matchings.objects.filter(uuid=uuid).first()
    if not matching:
        return ApiResponse(error="Matching not found", status=404)
    
    return ApiResponse(matching=MatchingSerializer(matching).data)

@api_view(['POST'])
def matching_store(request):
    """Create a new matching"""
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    data = request.data
    matching = Matchings.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user_id=user_id,
        average_turnaround_time=data.get('average_turnaround_time'),
        interested_in=data.get('interested_in'),
        token=secrets.token_hex(16),
        project_id=data.get('project_id'),
        utc_offset=data.get('utc_offset'),
        timezone=data.get('timezone'),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(matching=MatchingSerializer(matching).data)

@api_view(['PATCH'])
def matching_update(request, uuid):
    """Update a matching"""
    matching = Matchings.objects.filter(uuid=uuid).first()
    if not matching:
        return ApiResponse(error="Matching not found", status=404)
    
    data = request.data
    for field in ['average_turnaround_time', 'interested_in', 'utc_offset', 'timezone']:
        if field in data:
            setattr(matching, field, data[field])
    
    matching.updated_at = timezone.now()
    matching.save()
    
    return ApiResponse(matching=MatchingSerializer(matching).data)

@api_view(['PATCH'])
def matching_editor_update(request):
    """Update matching editor status"""
    # In Laravel: $this->matchingService->updateMatchingEditor($request)
    return ApiResponse(message="Matching editor status updated")

@api_view(['GET'])
def matching_get_by_project_id(request, project_uuid):
    """Get matching results by project UUID"""
    project = get_object_or_404(Projects, uuid=project_uuid)
    matching = Matchings.objects.filter(project_id=project.id).first()
    return ApiResponse(matching=MatchingSerializer(matching).data if matching else None)

@api_view(['POST'])
def matching_public_create(request):
    """Publicly create a matching and return editors"""
    # Mocking public matching creation
    return ApiResponse(
        editors=[],
        total=0,
        page=1,
        topics=[]
    )

@api_view(['GET'])
def matching_get_by_token(request, token):
    """Get matching results by token"""
    matching = get_object_or_404(Matchings, token=token)
    return ApiResponse(matching=MatchingSerializer(matching).data)

@api_view(['POST'])
def matching_create_from_favorite_creators(request):
    """Create matching based on favorite creators"""
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    # Mocking logic
    return ApiResponse(
        matching={},
        creators=[]
    )

@api_view(['POST'])
def matching_admin_update(request, id):
    """Admin update for matching"""
    matching = get_object_or_404(Matchings, id=id)
    # Update logic here
    return ApiResponse(matching=MatchingSerializer(matching).data)


# ============================================================================
# EDITOR ENDPOINTS
# ============================================================================

@api_view(['GET'])
def editor_index(request):
    """Search and list editors"""
    search = request.query_params.get('search', '')
    editors = Users.objects.filter(account_type='editor', active=1)
    if search:
        editors = editors.filter(name__icontains=search) | editors.filter(username__icontains=search)
    
    serializer = UserSerializer(editors, many=True)
    return ApiResponse(editors=serializer.data)

@api_view(['GET'])
def editor_get(request, username):
    """Get editor details by username"""
    editor = Users.objects.filter(username=username, account_type='editor').first()
    if not editor:
        return ApiResponse(error="Editor not found", status=404)
    
    return ApiResponse(editor=UserSerializer(editor).data)

@api_view(['GET'])
def editor_projects(request, username):
    """Get editor projects"""
    editor = Users.objects.filter(username=username).first()
    if not editor:
        return ApiResponse(error="User not found", status=404)
    
    projects = UserProjects.objects.filter(user=editor)
    serializer = UserProjectSerializer(projects, many=True)
    return ApiResponse(projects=serializer.data)

@api_view(['GET'])
def editor_creators(request, username):
    """Get creators associated with an editor"""
    editor = Users.objects.filter(username=username).first()
    if not editor:
        return ApiResponse(error="User not found", status=404)
    
    creators = UserCreators.objects.filter(user=editor)
    serializer = UserCreatorSerializer(creators, many=True)
    return ApiResponse(creators=serializer.data)

@api_view(['GET'])
def editor_reviews(request, username):
    """Get editor reviews (Mocked)"""
    return ApiResponse(reviews=[], rating=0, average=0)


# ============================================================================
# PROJECT SCREENING QUESTION ENDPOINTS
# ============================================================================

@extend_schema(responses={200: ProjectScreeningQuestionSerializer(many=True)}, operation_id="project_screening_question_list")
@api_view(['GET'])
def project_screening_question_index(request, project_uuid):
    """List screening questions for a project"""
    project = Projects.objects.filter(uuid=project_uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    questions = ProjectScreeningQuestions.objects.filter(project=project)
    serializer = ProjectScreeningQuestionSerializer(questions, many=True)
    return ApiResponse(questions=serializer.data)

@api_view(['POST'])
def project_screening_question_store(request, project_uuid):
    """Store a new screening question"""
    project = Projects.objects.filter(uuid=project_uuid).first()
    if not project:
        return ApiResponse(error="Project not found", status=404)
    
    data = request.data
    question_type = QuestionTypes.objects.filter(uuid=data.get('question_type')).first()
    
    question = ProjectScreeningQuestions.objects.create(
        uuid=str(uuid_lib.uuid4()),
        project=project,
        question_type=question_type,
        question=data.get('question'),
        options=data.get('options'),
        required=data.get('required', 0),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    return ApiResponse(question=ProjectScreeningQuestionSerializer(question).data)

@extend_schema(responses={200: ProjectScreeningQuestionSerializer}, operation_id="project_screening_question_retrieve")
@api_view(['GET'])
def project_screening_question_show(request, project_uuid, question_uuid):
    """Show a screening question"""
    question = ProjectScreeningQuestions.objects.filter(uuid=question_uuid).first()
    if not question:
        return ApiResponse(error="Question not found", status=404)
    return ApiResponse(question=ProjectScreeningQuestionSerializer(question).data)

@api_view(['PATCH', 'PUT'])
def project_screening_question_update(request, project_uuid, question_uuid):
    """Update a screening question"""
    question = ProjectScreeningQuestions.objects.filter(uuid=question_uuid).first()
    if not question:
        return ApiResponse(error="Question not found", status=404)
    
    data = request.data
    for field in ['question', 'options', 'required']:
        if field in data:
            setattr(question, field, data[field])
    
    question.updated_at = timezone.now()
    question.save()
    return ApiResponse(question=ProjectScreeningQuestionSerializer(question).data)

@api_view(['DELETE'])
def project_screening_question_destroy(request, project_uuid, question_uuid):
    """Delete a screening question"""
    question = ProjectScreeningQuestions.objects.filter(uuid=question_uuid).first()
    if not question:
        return ApiResponse(error="Question not found", status=404)
    question.delete()
    return ApiResponse(message="Question deleted successfully")


# ============================================================================
# USER PAYMENT ENDPOINTS
# ============================================================================

@api_view(['GET'])
def user_payment_index(request):
    """List user payment accounts"""
    user = get_authenticated_user(request)
    if not user:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    payments = UserPayments.objects.filter(user=user, deleted_at__isnull=True)
    result = {}
    for payment in payments:
        result[payment.gateway] = UserPaymentSerializer(payment).data
        
    return ApiResponse(payments=result)

@api_view(['POST'])
def user_payment_create(request):
    """Add a new payment account"""
    user = get_authenticated_user(request)
    if not user:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    data = request.data
    gateway = data.get('gateway')
    if not gateway:
        return ApiResponse(error="Gateway is required", status=422)

    # UserPayments model doesn't have authorization_code, it has external_user_id and meta
    payment = UserPayments.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        gateway=gateway,
        icon=data.get('icon', ''),
        name=data.get('name', user.name or user.email or 'Payment Account'),
        external_user_id=data.get('authorization_code', data.get('external_user_id', '')),
        username=data.get('username', ''),
        meta=data.get('meta', {}),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    return ApiResponse(payments=UserPaymentSerializer(payment).data)

@api_view(['DELETE'])
def user_payment_delete(request, uuid):
    """Delete a payment account"""
    user = get_authenticated_user(request)
    auth_user = user # For clarity in ownership check
        
    payment = UserPayments.objects.filter(uuid=uuid).first()
    if not payment:
        return ApiResponse(error="Payment account not found", status=404)
        
    # Check ownership if user is authenticated
    if auth_user and payment.user != auth_user:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    elif not auth_user:
        # If no auth provided at all, we might want to allow it for now or block
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
        
    payment.delete()
    return ApiResponse(message="Payment account deleted successfully")
@api_view(['POST'])
def customer_register(request):
    """Register a new customer (user + customer record)"""
    from .auth_helpers import create_access_token
    from uuid import uuid4
    
    data = request.data
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')
    
    if not email or not password:
        return ApiResponse(error="Email and password are required", status=422)
        
    if Users.objects.filter(email=email).exists():
        return ApiResponse(error="Email already exists", status=422)
        
    # Create user
    user = Users.objects.create(
        uuid=str(uuid4()),
        email=email,
        password=make_password(password),
        name=name,
        account_type='user',
        active=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    # Create Customer
    payment_type = PaymentTypes.objects.filter(name='free').first()
    payment_status = PaymentStatuses.objects.filter(name='free').first()
    
    if not payment_type or not payment_status:
        # Fallback to any active plan if 'free' is missing
        payment_type = PaymentTypes.objects.filter(active=1).first()
        payment_status = PaymentStatuses.objects.filter(active=1).first()
        
    if not payment_type or not payment_status:
        # Still null, can't create customer record
        return ApiResponse(error="Payment gateway not configured correctly", status=500)
    
    customer = Customers.objects.create(
        uuid=str(uuid4()),
        user=user,
        payment_type=payment_type,
        payment_status=payment_status,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    token = create_access_token(user)
    
    return ApiResponse(
        status='success',
        message='Customer registered successfully',
        user=UserSerializer(user).data,
        customer=CustomerSerializer(customer).data,
        access_token=token,
        token_type='Bearer'
    )

# ============================================================================
# CUSTOMER ENDPOINTS
# ============================================================================

@api_view(['GET'])
def customer_get_by_user(request):
    """Get customer information for the current user"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    customer = Customers.objects.filter(user_id=user_id).first()
    # Mock current subscription for now
    subscription = {
        'is_active': True,
        'plan': 'Pro',
        'current_period_end': (timezone.now() + timezone.timedelta(days=30)).isoformat()
    }
    
    return ApiResponse(
        customer=CustomerSerializer(customer).data if customer else None,
        subscription=subscription
    )

@api_view(['POST'])
def customer_upgrade(request):
    """Upgrade customer plan"""
    user = get_authenticated_user(request)
    if not user:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    # Mock upgrade result
    return ApiResponse(
        message="Upgrade initiated",
        result={
            'checkout_url': 'https://checkout.stripe.com/mock',
            'transaction': {'id': 'txn_mock', 'amount': 100}
        }
    )

@api_view(['POST'])
def customer_generate_subscription_link(request):
    """Generate Stripe subscription management link"""
    return ApiResponse(url="https://billing.stripe.com/mock")

@api_view(['POST'])
def customer_stop_email_webhook(request):
    """Webhook to stop customer emails"""
    email = request.data.get('from', '')
    return ApiResponse(email=email, message="Email webhook processed")

@api_view(['POST'])
def customer_update_expiry_from_stripe(request):
    """Update customer expiry date from Stripe webhook"""
    user_id = request.data.get('user_id')
    expired_at = request.data.get('expired_at')
    
    customer = Customers.objects.filter(user_id=user_id).first()
    if not customer:
        return ApiResponse(error=f"No customer found for user_id: {user_id}", status=404)
        
    customer.expired_at = expired_at
    customer.updated_at = timezone.now()
    customer.save()
    
    return ApiResponse(
        message="Customer expiry date updated successfully.",
        user_id=user_id,
        expired_at=expired_at
    )

# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@extend_schema(responses={200: ChatSerializer(many=True)}, operation_id="chat_list")
@api_view(['GET'])
def chat_index(request):
    """List chats for the current user"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    if not user_id:
        return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    # Logic to get chats where user is a participant
    # In Laravel: $this->chatService->getByUser($user, $request)
    # Participants is a JSON field
    chats = Chats.objects.all() # Filtering logic would be complex with raw participants JSON
    # For now, simplistic fetch
    
    return ApiResponse(
        chats=ChatSerializer(chats, many=True).data,
        total=chats.count(),
        page=request.query_params.get('page', 1)
    )

@extend_schema(responses={200: ChatSerializer}, operation_id="chat_retrieve")
@api_view(['GET'])
def chat_get(request, uuid):
    """Get messages for a specific chat"""
    chat = get_object_or_404(Chats, uuid=uuid)
    messages = ChatMessages.objects.filter(chat=chat).order_by('created_at')
    
    return ApiResponse(
        chat=ChatSerializer(chat).data,
        messages=ChatMessageSerializer(messages, many=True).data,
        total=messages.count(),
        page=request.query_params.get('page', 1)
    )

@api_view(['POST'])
def chat_message(request, uuid):
    """Send a message in a chat"""
    chat = get_object_or_404(Chats, uuid=uuid)
    message_text = request.data.get('message')
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    
    if not message_text:
        return ApiResponse(error="Message is required", status=400)
        
    if not user_id:
        return ApiResponse(error="User identification required", status=401)
        
    user = Users.objects.filter(id=user_id).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    message = ChatMessages.objects.create(
        uuid=str(uuid_lib.uuid4()),
        chat=chat,
        user=user,
        message=message_text,
        created_at=timezone.now()
    )
    
    # Mocking notifications
    return ApiResponse(
        message=ChatMessageSerializer(message).data,
        notification_sent=True
    )

@api_view(['POST'])
def chat_create_custom_message(request):
    """Create a chat and send a message"""
    user_id = request.data.get('user_id')
    recipient_id = request.data.get('recipient_id')
    message_text = request.data.get('message')
    
    if not user_id or not recipient_id or not message_text:
        return ApiResponse(error="user_id, recipient_id, and message are required", status=422)
    
    sender = Users.objects.filter(id=user_id).first()
    recipient = Users.objects.filter(id=recipient_id).first()
    
    if not sender or not recipient:
        return ApiResponse(error="Sender or Recipient not found", status=404)
        
    # Check if chat exists (ordering doesn't matter in participants list usually)
    chat = Chats.objects.filter(participants__contains=user_id).filter(participants__contains=recipient_id).first()
    if not chat:
        chat = Chats.objects.create(
            uuid=str(uuid_lib.uuid4()),
            participants=[user_id, recipient_id],
            created_at=timezone.now()
        )
        
    message = ChatMessages.objects.create(
        uuid=str(uuid_lib.uuid4()),
        chat=chat,
        user=sender,
        message=message_text,
        created_at=timezone.now()
    )
    
    return ApiResponse(
        message=ChatMessageSerializer(message).data,
        chat=ChatSerializer(chat).data
    )

@api_view(['POST'])
def chat_init(request):
    """Initialize chat for a project"""
    project_id = request.data.get('project_id')
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    
    if not project_id or not user_id:
        return ApiResponse(error="project_id and user_id are required", status=422)
        
    project = get_object_or_404(Projects, uuid=project_id)
    user = Users.objects.filter(id=user_id).first()
    
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    # create chat logic
    chat = Chats.objects.create(
        uuid=str(uuid_lib.uuid4()),
        participants=[user.id, project.user_id],
        created_at=timezone.now()
    )
    
    return ApiResponse(chat=ChatSerializer(chat).data)

@api_view(['POST'])
def chat_init_public(request):
    """Initialize a public chat with a recipient"""
    recipient_id = request.data.get('recipient_id')
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    
    if not user_id or not recipient_id:
        return ApiResponse(error="user_id and recipient_id are required", status=422)
        
    user = Users.objects.filter(id=user_id).first()
    recipient = Users.objects.filter(id=recipient_id).first()
    
    if not user or not recipient:
        return ApiResponse(error="User or Recipient not found", status=404)
        
    chat = Chats.objects.create(
        uuid=str(uuid_lib.uuid4()),
        participants=[user.id, recipient.id],
        created_at=timezone.now()
    )
    
    return ApiResponse(chat=ChatSerializer(chat).data)

@api_view(['GET'])
def chat_get_received_messages(request):
    """Get all received messages for user"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    messages = ChatMessages.objects.filter(recipient_id=user_id).order_by('-created_at')
    
    return ApiResponse(
        messages=ChatMessageSerializer(messages, many=True).data,
        total=messages.count()
    )

@api_view(['POST'])
def chat_update_message(request, id):
    """Update message status or content"""
    message = get_object_or_404(ChatMessages, id=id)
    # logic to update
    return ApiResponse(updated_message=ChatMessageSerializer(message).data)

# ============================================================================
# FAVOURITE ENDPOINTS
# ============================================================================

@api_view(['GET'])
def favourite_index(request):
    """List favourites for user"""
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    favourites = UserFavourites.objects.filter(user_id=user_id)
    
    return ApiResponse(
        favourites=UserFavouriteSerializer(favourites, many=True).data,
        total=favourites.count()
    )

@api_view(['POST'])
def favourite_store(request):
    """Add or remove favourite"""
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    editor_uuid = request.data.get('editor')
    status = request.data.get('status') # true to add, false to remove
    
    if not user_id or not editor_uuid:
        return ApiResponse(error="user_id and editor are required", status=422)
        
    user = Users.objects.filter(id=user_id).first()
    editor = Users.objects.filter(uuid=editor_uuid).first()
    
    if not user or not editor:
        return ApiResponse(error="User or Editor not found", status=404)
    
    if status is True or status == 'true':
        favourite, created = UserFavourites.objects.get_or_create(
            user=user,
            favourite_user=editor
        )
        message = "Added to favourites"
    else:
        UserFavourites.objects.filter(user=user, favourite_user=editor).delete()
        message = "Removed from favourites"
        
    return ApiResponse(message=message)

# ============================================================================
# PROFILE VISIT ENDPOINTS
# ============================================================================

@api_view(['POST'])
def profile_visit_store(request):
    """Store profile visit"""
    user_id = request.headers.get('X-User-ID') or request.data.get('user_id')
    editor_id = request.data.get('editor_id') 
    
    if not user_id or not editor_id:
        return ApiResponse(error="user_id and editor_id are required", status=422)
        
    user = Users.objects.filter(id=user_id).first()
    # editor_id might be UUID or ID, check both
    editor = Users.objects.filter(uuid=editor_id).first() or Users.objects.filter(id=editor_id).first()
    
    if not user or not editor:
        return ApiResponse(error="User or Editor not found", status=404)
        
    ProfileVisits.objects.create(
        user=user,
        editor=editor,
        user_id=user_id,
        editor_id=editor_id,
        created_at=timezone.now()
    )
    
    return ApiResponse(message="Profile visit recorded")

# ============================================================================
# ADMIN MANAGEMENT ENDPOINTS
# ============================================================================

@api_view(['GET'])
def admin_list_editors(request):
    """List all editors for admin"""
    # TODO: check_permission('admin_access')
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 20))
    
    editors = Users.objects.filter(account_type='editor', deleted_at__isnull=True)
    total = editors.count()
    
    start = (page - 1) * per_page
    end = start + per_page
    editors_page = editors[start:end]
    
    return ApiResponse(
        status='success',
        message='Editors loaded successfully',
        editors=AdminUserSerializer(editors_page, many=True).data,
        total=total,
        page=page
    )

@api_view(['GET'])
def admin_get_editor(request, id):
    """Get editor details for admin"""
    # TODO: check_permission('admin_access')
    editor = Users.objects.filter(id=id, account_type='editor').first()
    if not editor:
        editor = Users.objects.filter(uuid=id, account_type='editor').first()
        
    if not editor:
        return ApiResponse(error="Editor not found", status=404)
        
    return ApiResponse(
        status='success',
        message='Editor loaded successfully',
        editor=AdminUserSerializer(editor).data
    )

@api_view(['GET'])
def admin_list_creators(request):
    """List all creators (customers) for admin"""
    # TODO: check_permission('admin_access')
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 20))
    
    creators = Users.objects.filter(account_type='user', deleted_at__isnull=True)
    total = creators.count()
    
    start = (page - 1) * per_page
    end = start + per_page
    creators_page = creators[start:end]
    
    return ApiResponse(
        status='success',
        message='Creators loaded successfully',
        creators=AdminUserSerializer(creators_page, many=True).data,
        total=total,
        page=page
    )

@api_view(['GET'])
def admin_get_creator(request, id):
    """Get creator details for admin"""
    # TODO: check_permission('admin_access')
    creator = Users.objects.filter(id=id, account_type='user').first()
    if not creator:
        creator = Users.objects.filter(uuid=id, account_type='user').first()
        
    if not creator:
        return ApiResponse(error="Creator not found", status=404)
        
    return ApiResponse(
        status='success',
        message='Creator loaded successfully',
        user=AdminUserSerializer(creator).data
    )

@api_view(['GET'])
def admin_list_projects(request):
    """List all projects for admin"""
    # TODO: check_permission('admin_access')
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 20))
    
    projects = Projects.objects.all()
    total = projects.count()
    
    start = (page - 1) * per_page
    end = start + per_page
    projects_page = projects[start:end]
    
    return ApiResponse(
        status='success',
        message='Projects loaded successfully',
        projects=AdminProjectSerializer(projects_page, many=True).data,
        total=total,
        page=page
    )

@api_view(['GET'])
def admin_get_project(request, id):
    """Get project details for admin"""
    # TODO: check_permission('admin_access')
    project = Projects.objects.filter(id=id).first()
    if not project:
        project = Projects.objects.filter(uuid=id).first()
        
    if not project:
        return ApiResponse(error="Project not found", status=404)
        
    return ApiResponse(
        status='success',
        message='Project loaded successfully',
        project=AdminProjectSerializer(project).data
    )

@api_view(['DELETE'])
def admin_delete_account(request, email):
    """Delete a user account by email"""
    # TODO: check_permission('admin_access')
    user = Users.objects.filter(email=email).first()
    if not user:
        return ApiResponse(error="User not found", status=404)
        
    user.deleted_at = timezone.now()
    user.active = 0
    user.save()
    
    return ApiResponse(
        status='success',
        message='Deleted the account'
    )

@api_view(['POST'])
def admin_email_user(request):
    """Email a user (Placeholder)"""
    # TODO: check_permission('admin_access')
    user_id = request.data.get('user_id')
    return ApiResponse(
        status='success',
        message=f'Emailed {user_id}'
    )

# ============================================================================
# FILE MANAGEMENT ENDPOINTS
# ============================================================================

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import FileResponse, HttpResponse

@api_view(['POST'])
def file_store(request):
    """Store a file for authenticated user"""
    user = get_authenticated_user(request)
    if not user:
        return ApiResponse(error="Unauthorized", status=401)
        
    if 'photo' not in request.FILES:
        return ApiResponse(error="File is required", status=400)
        
    uploaded_file = request.FILES['photo']
    file_name = f"{timezone.now().timestamp()}_{uploaded_file.name}"
    
    # Save to storage
    path = default_storage.save(f"users/{user.id}/{file_name}", ContentFile(uploaded_file.read()))
    
    file_record = Files.objects.create(
        uuid=str(uuid_lib.uuid4()),
        user=user,
        name=path,
        description=uploaded_file.name,
        reference_name='users',
        reference_id=str(user.id),
        public=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    return ApiResponse(
        status='success',
        message='File created successfully',
        file=FilesSerializer(file_record).data
    )

@api_view(['POST'])
def file_upload(request):
    """General file upload to storage"""
    if 'file' not in request.FILES:
        return ApiResponse(error="File is required", status=400)
        
    uploaded_file = request.FILES['file']
    file_name = f"{timezone.now().timestamp()}_{uploaded_file.name}"
    
    # For now, save to local storage (Google Cloud Storage placeholder)
    path = default_storage.save(f"uploads/{file_name}", ContentFile(uploaded_file.read()))
    url = default_storage.url(path)
    
    return ApiResponse(url=url)

@api_view(['POST'])
def file_upload_multiple(request):
    """Multiple files upload to storage"""
    if 'files' not in request.FILES:
        return ApiResponse(error="Files are required", status=400)
        
    files = request.FILES.getlist('files')
    uploaded_files = []
    
    for f in files:
        file_name = f"{timezone.now().timestamp()}_{uuid_lib.uuid4()}_{f.name}"
        path = default_storage.save(f"uploads/{file_name}", ContentFile(f.read()))
        uploaded_files.append({
            'url': default_storage.url(path),
            'format': os.path.splitext(f.name)[1][1:],
            'original_name': f.name,
            'size': f.size
        })
        
    return ApiResponse(
        success=True,
        uploaded_files=uploaded_files,
        total_uploaded=len(uploaded_files),
        total_files=len(files)
    )

@api_view(['GET'])
def file_get_signed_url(request, filename):
    """Get a signed URL (Placeholder for GCS)"""
    url = default_storage.url(filename)
    return ApiResponse(url=url)

@api_view(['GET'])
def file_serve(request, id):
    """Serve file content"""
    file_record = Files.objects.filter(uuid=id).first()
    if not file_record:
        return ApiResponse(error="File not found", status=404)
        
    if not file_record.public and not get_authenticated_user(request):
        return ApiResponse(error="Unauthorized", status=401)
        
    path = os.path.join(settings.MEDIA_ROOT, file_record.name)
    if not os.path.exists(path):
        return ApiResponse(error="File not found on disk", status=404)
        
    return FileResponse(open(path, 'rb'))

@api_view(['GET'])
def file_download(request, id):
    """Download file"""
    file_record = Files.objects.filter(uuid=id).first()
    if not file_record:
        return ApiResponse(error="File not found", status=404)
        
    path = os.path.join(settings.MEDIA_ROOT, file_record.name)
    if not os.path.exists(path):
        return ApiResponse(error="File not found on disk", status=404)
        
    response = FileResponse(open(path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_record.name)}"'
    return response


# Updated by Clawbot

# --- Taxonomy CRUD Endpoints ---

@api_view(['POST'])
def skill_store(request):
    data = request.data
    Skills.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Skills.objects.filter(active=1)
    return ApiResponse(skills=SkillSerializer(items, many=True).data)

@api_view(['POST'])
def skill_update(request):
    data = request.data
    item_id = data.get('id')
    Skills.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Skills.objects.filter(active=1)
    return ApiResponse(skills=SkillSerializer(items, many=True).data)

@api_view(['GET'])
def skill_destroy(request, id):
    Skills.objects.filter(id=id).delete()
    items = Skills.objects.filter(active=1)
    return ApiResponse(skills=SkillSerializer(items, many=True).data)

@api_view(['GET'])
def skill_show(request, id):
    item = Skills.objects.filter(id=id).first()
    return ApiResponse(skill=SkillSerializer(item).data if item else None)

@api_view(['POST'])
def job_types_store(request):
    data = request.data
    JobTypes.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = JobTypes.objects.filter(active=1)
    return ApiResponse(jobtypes=JobTypeSerializer(items, many=True).data)

@api_view(['POST'])
def job_types_update(request):
    data = request.data
    item_id = data.get('id')
    JobTypes.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = JobTypes.objects.filter(active=1)
    return ApiResponse(jobtypes=JobTypeSerializer(items, many=True).data)

@api_view(['GET'])
def job_types_destroy(request, id):
    JobTypes.objects.filter(id=id).delete()
    items = JobTypes.objects.filter(active=1)
    return ApiResponse(jobtypes=JobTypeSerializer(items, many=True).data)

@api_view(['GET'])
def job_types_show(request, id):
    item = JobTypes.objects.filter(id=id).first()
    return ApiResponse(job_types=JobTypeSerializer(item).data if item else None)

@api_view(['POST'])
def equipment_store(request):
    data = request.data
    Equipment.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Equipment.objects.filter(active=1)
    return ApiResponse(equipments=EquipmentSerializer(items, many=True).data)

@api_view(['POST'])
def equipment_update(request):
    data = request.data
    item_id = data.get('id')
    Equipment.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Equipment.objects.filter(active=1)
    return ApiResponse(equipments=EquipmentSerializer(items, many=True).data)

@api_view(['GET'])
def equipment_destroy(request, id):
    Equipment.objects.filter(id=id).delete()
    items = Equipment.objects.filter(active=1)
    return ApiResponse(equipments=EquipmentSerializer(items, many=True).data)

@api_view(['GET'])
def equipment_show(request, id):
    item = Equipment.objects.filter(id=id).first()
    return ApiResponse(equipment=EquipmentSerializer(item).data if item else None)

@api_view(['POST'])
def software_store(request):
    data = request.data
    Software.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Software.objects.filter(active=1)
    return ApiResponse(softwares=SoftwareSerializer(items, many=True).data)

@api_view(['POST'])
def software_update(request):
    data = request.data
    item_id = data.get('id')
    Software.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Software.objects.filter(active=1)
    return ApiResponse(softwares=SoftwareSerializer(items, many=True).data)

@api_view(['GET'])
def software_destroy(request, id):
    Software.objects.filter(id=id).delete()
    items = Software.objects.filter(active=1)
    return ApiResponse(softwares=SoftwareSerializer(items, many=True).data)

@api_view(['GET'])
def software_show(request, id):
    item = Software.objects.filter(id=id).first()
    return ApiResponse(software=SoftwareSerializer(item).data if item else None)

@api_view(['POST'])
def platform_store(request):
    data = request.data
    Platforms.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Platforms.objects.filter(active=1)
    return ApiResponse(platforms=PlatformSerializer(items, many=True).data)

@api_view(['POST'])
def platform_update(request):
    data = request.data
    item_id = data.get('id')
    Platforms.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Platforms.objects.filter(active=1)
    return ApiResponse(platforms=PlatformSerializer(items, many=True).data)

@api_view(['GET'])
def platform_destroy(request, id):
    Platforms.objects.filter(id=id).delete()
    items = Platforms.objects.filter(active=1)
    return ApiResponse(platforms=PlatformSerializer(items, many=True).data)

@api_view(['GET'])
def platform_show(request, id):
    item = Platforms.objects.filter(id=id).first()
    return ApiResponse(platform=PlatformSerializer(item).data if item else None)

@api_view(['POST'])
def content_vertical_store(request):
    data = request.data
    ContentVerticals.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = ContentVerticals.objects.filter(active=1)
    return ApiResponse(contentverticals=ContentVerticalSerializer(items, many=True).data)

@api_view(['POST'])
def content_vertical_update(request):
    data = request.data
    item_id = data.get('id')
    ContentVerticals.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = ContentVerticals.objects.filter(active=1)
    return ApiResponse(contentverticals=ContentVerticalSerializer(items, many=True).data)

@api_view(['GET'])
def content_vertical_destroy(request, id):
    ContentVerticals.objects.filter(id=id).delete()
    items = ContentVerticals.objects.filter(active=1)
    return ApiResponse(contentverticals=ContentVerticalSerializer(items, many=True).data)

@api_view(['GET'])
def content_vertical_show(request, id):
    item = ContentVerticals.objects.filter(id=id).first()
    return ApiResponse(content_vertical=ContentVerticalSerializer(item).data if item else None)

@api_view(['POST'])
def creative_style_store(request):
    data = request.data
    CreativeStyles.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = CreativeStyles.objects.filter(active=1)
    return ApiResponse(creativestyles=CreativeStyleSerializer(items, many=True).data)

@api_view(['POST'])
def creative_style_update(request):
    data = request.data
    item_id = data.get('id')
    CreativeStyles.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = CreativeStyles.objects.filter(active=1)
    return ApiResponse(creativestyles=CreativeStyleSerializer(items, many=True).data)

@api_view(['GET'])
def creative_style_destroy(request, id):
    CreativeStyles.objects.filter(id=id).delete()
    items = CreativeStyles.objects.filter(active=1)
    return ApiResponse(creativestyles=CreativeStyleSerializer(items, many=True).data)

@api_view(['GET'])
def creative_style_show(request, id):
    item = CreativeStyles.objects.filter(id=id).first()
    return ApiResponse(creative_style=CreativeStyleSerializer(item).data if item else None)

@api_view(['POST'])
def content_form_store(request):
    data = request.data
    ContentForms.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = ContentForms.objects.filter(active=1)
    return ApiResponse(content_forms=ContentFormSerializer(items, many=True).data)

@api_view(['POST'])
def content_form_update(request):
    data = request.data
    item_id = data.get('id')
    ContentForms.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = ContentForms.objects.filter(active=1)
    return ApiResponse(content_forms=ContentFormSerializer(items, many=True).data)

@api_view(['GET'])
def content_form_destroy(request, id):
    ContentForms.objects.filter(id=id).delete()
    items = ContentForms.objects.filter(active=1)
    return ApiResponse(content_forms=ContentFormSerializer(items, many=True).data)

@api_view(['GET'])
def content_form_show(request, id):
    item = ContentForms.objects.filter(id=id).first()
    return ApiResponse(content_form=ContentFormSerializer(item).data if item else None)

@api_view(['POST'])
def project_type_store(request):
    data = request.data
    ProjectTypes.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = ProjectTypes.objects.filter(active=1)
    return ApiResponse(project_types=ProjectTypeSerializer(items, many=True).data)

@api_view(['POST'])
def project_type_update(request):
    data = request.data
    item_id = data.get('id')
    ProjectTypes.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = ProjectTypes.objects.filter(active=1)
    return ApiResponse(project_types=ProjectTypeSerializer(items, many=True).data)

@api_view(['GET'])
def project_type_destroy(request, id):
    ProjectTypes.objects.filter(id=id).delete()
    items = ProjectTypes.objects.filter(active=1)
    return ApiResponse(project_types=ProjectTypeSerializer(items, many=True).data)

@api_view(['GET'])
def project_type_show(request, id):
    item = ProjectTypes.objects.filter(id=id).first()
    return ApiResponse(project_type=ProjectTypeSerializer(item).data if item else None)

@api_view(['POST'])
def reason_store(request):
    data = request.data
    Reasons.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        tags=data.get('tags'),
        active=data.get('active', 1)
    )
    items = Reasons.objects.filter(active=1)
    return ApiResponse(reasons=ReasonSerializer(items, many=True).data)

@api_view(['POST'])
def reason_update(request):
    data = request.data
    item_id = data.get('id')
    Reasons.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        tags=data.get('tags'),
        active=data.get('active', 1)
    )
    items = Reasons.objects.filter(active=1)
    return ApiResponse(reasons=ReasonSerializer(items, many=True).data)

@api_view(['GET'])
def reason_destroy(request, id):
    Reasons.objects.filter(id=id).delete()
    items = Reasons.objects.filter(active=1)
    return ApiResponse(reasons=ReasonSerializer(items, many=True).data)

@api_view(['GET'])
def reason_show(request, id):
    item = Reasons.objects.filter(id=id).first()
    return ApiResponse(reason=ReasonSerializer(item).data if item else None)

@api_view(['POST'])
def referral_store(request):
    data = request.data
    Referrals.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Referrals.objects.filter(active=1)
    return ApiResponse(referrals=ReferralSerializer(items, many=True).data)

@api_view(['POST'])
def referral_update(request):
    data = request.data
    item_id = data.get('id')
    Referrals.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = Referrals.objects.filter(active=1)
    return ApiResponse(referrals=ReferralSerializer(items, many=True).data)

@api_view(['GET'])
def referral_destroy(request, id):
    Referrals.objects.filter(id=id).delete()
    items = Referrals.objects.filter(active=1)
    return ApiResponse(referrals=ReferralSerializer(items, many=True).data)

@api_view(['GET'])
def referral_show(request, id):
    item = Referrals.objects.filter(id=id).first()
    return ApiResponse(referral=ReferralSerializer(item).data if item else None)

# --- Core User Management CRUD Endpoints ---

@api_view(['GET'])
def role_index(request):
    items = Roles.objects.filter(active=1)
    return ApiResponse(roles=RoleSerializer(items, many=True).data)

@api_view(['POST'])
def role_store(request):
    data = request.data
    Roles.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        code=data.get('code'),
        active=data.get('active', 1)
    )
    items = Roles.objects.filter(active=1)
    return ApiResponse(roles=RoleSerializer(items, many=True).data)

@api_view(['POST'])
def role_update(request):
    data = request.data
    item_id = data.get('id')
    Roles.objects.filter(id=item_id).update(
        name=data.get('name'),
        code=data.get('code'),
        active=data.get('active', 1)
    )
    items = Roles.objects.filter(active=1)
    return ApiResponse(roles=RoleSerializer(items, many=True).data)

@api_view(['GET'])
def role_destroy(request, id):
    Roles.objects.filter(id=id).delete()
    items = Roles.objects.filter(active=1)
    return ApiResponse(roles=RoleSerializer(items, many=True).data)

@api_view(['GET'])
def role_show(request, id):
    item = Roles.objects.filter(id=id).first()
    return ApiResponse(role=RoleSerializer(item).data if item else None)

@api_view(['GET'])
def permission_index(request):
    items = Permissions.objects.filter(active=1)
    return ApiResponse(permissions=PermissionSerializer(items, many=True).data)

@api_view(['POST'])
def permission_store(request):
    data = request.data
    Permissions.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        active=data.get('active', 1)
    )
    items = Permissions.objects.filter(active=1)
    return ApiResponse(permissions=PermissionSerializer(items, many=True).data)

@api_view(['POST'])
def permission_update(request):
    data = request.data
    item_id = data.get('id')
    Permissions.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        active=data.get('active', 1)
    )
    items = Permissions.objects.filter(active=1)
    return ApiResponse(permissions=PermissionSerializer(items, many=True).data)

@api_view(['GET'])
def permission_destroy(request, id):
    Permissions.objects.filter(id=id).delete()
    items = Permissions.objects.filter(active=1)
    return ApiResponse(permissions=PermissionSerializer(items, many=True).data)

@api_view(['GET'])
def permission_show(request, id):
    item = Permissions.objects.filter(id=id).first()
    return ApiResponse(permission=PermissionSerializer(item).data if item else None)

@api_view(['GET'])
def menu_index(request):
    items = Menus.objects.filter(active=1)
    return ApiResponse(menus=MenuSerializer(items, many=True).data)

@api_view(['POST'])
def menu_store(request):
    data = request.data
    Menus.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        link=data.get('link'),
        icon=data.get('icon'),
        priority=data.get('priority', 0),
        active=data.get('active', 1)
    )
    items = Menus.objects.filter(active=1)
    return ApiResponse(menus=MenuSerializer(items, many=True).data)

@api_view(['POST'])
def menu_update(request):
    data = request.data
    item_id = data.get('id')
    Menus.objects.filter(id=item_id).update(
        name=data.get('name'),
        link=data.get('link'),
        icon=data.get('icon'),
        priority=data.get('priority', 0),
        active=data.get('active', 1)
    )
    items = Menus.objects.filter(active=1)
    return ApiResponse(menus=MenuSerializer(items, many=True).data)

@api_view(['GET'])
def menu_destroy(request, id):
    Menus.objects.filter(id=id).delete()
    items = Menus.objects.filter(active=1)
    return ApiResponse(menus=MenuSerializer(items, many=True).data)

@api_view(['GET'])
def menu_show(request, id):
    item = Menus.objects.filter(id=id).first()
    return ApiResponse(menu=MenuSerializer(item).data if item else None)


# --- User & Dashboard Management Endpoints ---

@api_view(['GET'])
def dashboard_index(request):
    # Dummy stats for dashboard
    users_count = Users.objects.filter(active=1).count()
    projects_count = Projects.objects.exclude(status='deleted').count()
    return ApiResponse(dashboard={
        "total_users": users_count,
        "total_projects": projects_count,
        "message": "Dashboard data fetched successfully."
    })

@api_view(['GET'])
def user_index(request):
    search = request.query_params.get('search', '')
    users = Users.objects.filter()
    if search:
        users = users.filter(name__icontains=search) | users.filter(email__icontains=search)
    return ApiResponse(users=UserSerializer(users[:50], many=True).data)

@api_view(['GET'])
def user_list(request):
    users = Users.objects.filter(active=1).order_by('-created_at')[:50]
    return ApiResponse(users=UserSerializer(users, many=True).data)

@api_view(['GET'])
def user_create(request):
    # Returns data needed to render a creation form (e.g., roles)
    roles = Roles.objects.filter(active=1)
    return ApiResponse(roles=RoleSerializer(roles, many=True).data)

@api_view(['POST'])
def user_store(request):
    data = request.data
    import uuid
    from django.contrib.auth.hashers import make_password
    plain_password = data.get('password', 'password')
    user = Users.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        email=data.get('email'),
        password=make_password(plain_password),
        active=data.get('active', 1)
    )
    return ApiResponse(user=UserSerializer(user).data)

@api_view(['GET'])
def user_destroy(request, id):
    user = Users.objects.filter(id=id).first()
    if user:
        user.delete()
    return ApiResponse(message="User deleted successfully")

@api_view(['GET'])
def user_show(request, id):
    user = Users.objects.filter(id=id).first()
    return ApiResponse(user=UserSerializer(user).data if user else None)

@api_view(['GET'])
def user_edit(request, id):
    user = Users.objects.filter(id=id).first()
    roles = Roles.objects.filter(active=1)
    return ApiResponse(
        user=UserSerializer(user).data if user else None,
        roles=RoleSerializer(roles, many=True).data
    )

@api_view(['PATCH'])
def user_update_patch(request, id):
    data = request.data
    user = Users.objects.filter(id=id).first()
    if user:
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'active' in data:
            user.active = data['active']
        user.save()
    return ApiResponse(user=UserSerializer(user).data if user else None)

@api_view(['POST'])
def user_photo(request):
    # This expects a photo in request.FILES, similar to profile_photo
    user_id = request.data.get('user_id')
    user = Users.objects.filter(id=user_id).first()
    if user:
        if 'photo' in request.FILES:
            # mock saving photo
            user.photo = 'uploaded_file.png'
            user.save()
    return ApiResponse(user=UserSerializer(user).data if user else None)

@api_view(['GET', 'POST'])
def profile_edit(request):
    user_id = request.headers.get('X-User-ID') or request.query_params.get('user_id')
    user = Users.objects.filter(id=user_id).first()
    return ApiResponse(user=UserSerializer(user).data if user else None)

@api_view(['POST'])
def profile_photo(request):
    return user_photo(request) # Reuse logic

@api_view(['POST'])
def profile_password(request):
    user_id = request.data.get('user_id')
    user = Users.objects.filter(id=user_id).first()
    if user:
        from django.contrib.auth.hashers import make_password
        user.password = make_password(request.data.get('password'))
        user.save()
    return ApiResponse(message="Password updated successfully")

@api_view(['GET'])
def setting_system(request):
    return ApiResponse(message="System Settings")

@api_view(['GET'])
def setting_api(request):
    return ApiResponse(message="API Settings")

@api_view(['GET'])
def setting_app(request):
    return ApiResponse(message="App Settings")

# --- Complex Controllers & Endpoints ---

@api_view(['GET'])
def editor_list(request):
    editors = Users.objects.filter(account_type='editor', active=1)
    return ApiResponse(editors=UserSerializer(editors, many=True).data)

@api_view(['GET'])
def editor_create(request):
    return ApiResponse(message="Load Editor Creation Form Data")

@api_view(['POST'])
def editor_store(request):
    data = request.data
    import uuid
    from django.contrib.auth.hashers import make_password
    plain_password = data.get('password', 'password')
    user = Users.objects.create(
        uuid=str(uuid.uuid4()),
        name=data.get('name'),
        email=data.get('email'),
        password=make_password(plain_password),
        account_type='editor',
        active=data.get('active', 1)
    )
    return ApiResponse(editor=UserSerializer(user).data)

@api_view(['GET'])
def editor_destroy(request, id):
    user = Users.objects.filter(id=id, account_type='editor').first()
    if user:
        user.delete()
    return ApiResponse(message="Editor deleted successfully")

@api_view(['GET'])
def editor_show(request, id):
    user = Users.objects.filter(id=id, account_type='editor').first()
    return ApiResponse(editor=UserSerializer(user).data if user else None)

@api_view(['GET'])
def editor_edit(request, id):
    user = Users.objects.filter(id=id, account_type='editor').first()
    return ApiResponse(editor=UserSerializer(user).data if user else None)

@api_view(['PATCH'])
def editor_update(request, id):
    data = request.data
    user = Users.objects.filter(id=id, account_type='editor').first()
    if user:
        if 'name' in data: user.name = data['name']
        if 'email' in data: user.email = data['email']
        if 'active' in data: user.active = data['active']
        user.save()
    return ApiResponse(editor=UserSerializer(user).data if user else None)

@api_view(['POST'])
def editor_verification(request, id):
    return ApiResponse(message="Verification handled")

@api_view(['GET'])
def editor_activation(request, id, status):
    user = Users.objects.filter(id=id, account_type='editor').first()
    if user:
        user.active = 1 if status == 'active' else 0
        user.save()
    return ApiResponse(message="Activation handled")

@api_view(['GET'])
def editor_invite(request, id):
    return ApiResponse(message="Invite handled")

@api_view(['POST'])
def editor_project(request, id):
    return ApiResponse(message="Editor Project added")

@api_view(['GET'])
def editor_delete_project(request, id, project):
    return ApiResponse(message="Editor Project deleted")

@api_view(['POST'])
def editor_creator(request, id):
    return ApiResponse(message="Editor Creator handled")

@api_view(['GET'])
def editor_delete_creator(request, id, creator):
    return ApiResponse(message="Editor Creator deleted")

@api_view(['POST'])
def editor_send_verification_email(request, uuid):
    return ApiResponse(message="Email sent")

@api_view(['PATCH'])
def editor_update_verification_note(request, uuid):
    return ApiResponse(message="Verification note updated")

@api_view(['PATCH'])
def editor_approve_verification(request, uuid):
    return ApiResponse(message="Verification approved")

@api_view(['POST'])
def editor_delete_verification_note(request, uuid):
    return ApiResponse(message="Verification note deleted")

@api_view(['GET'])
def editor_get_verification_issues(request, uuid):
    return ApiResponse(issues=[])

# Project Missing
@api_view(['GET'])
def project_create_view(request):
    return ApiResponse(message="Load project creation form")

@api_view(['POST'])
def project_history(request, id):
    return ApiResponse(message="Project History")

@api_view(['POST'])
def project_review(request, id):
    return ApiResponse(message="Project Review")

@api_view(['POST'])
def project_feedback(request, id):
    return ApiResponse(message="Project Feedback")

@api_view(['GET'])
def project_destroy(request, id):
    proj = Projects.objects.filter(id=id).first()
    if proj: proj.delete()
    return ApiResponse(message="Project deleted")

@api_view(['GET'])
def project_edit(request, id):
    proj = Projects.objects.filter(id=id).first()
    return ApiResponse(project=ProjectSerializer(proj).data if proj else None)

# Project Applications
@api_view(['GET'])
def project_application_show_view(request, id):
    app = ProjectApplications.objects.filter(id=id).first()
    return ApiResponse(application=ProjectApplicationSerializer(app).data if app else None)

# Questionnaire Responses
@api_view(['GET'])
def questionnaire_response_index(request):
    return ApiResponse(responses=[])

@api_view(['GET'])
def questionnaire_response_show(request, id):
    return ApiResponse(response={})

@api_view(['GET'])
def questionnaire_response_approve(request, id):
    return ApiResponse(message="Approved")

@api_view(['GET'])
def questionnaire_response_reject(request, id):
    return ApiResponse(message="Rejected")

# Matching Settings
@api_view(['GET'])
def matching_setting_index(request):
    return ApiResponse(settings=[])

@api_view(['POST'])
def matching_setting_store(request):
    return ApiResponse(message="Setting stored")

@api_view(['POST'])
def matching_setting_update(request):
    return ApiResponse(message="Setting updated")

@api_view(['GET'])
def matching_setting_destroy(request, id):
    return ApiResponse(message="Setting destroyed")

# Chat
@api_view(['GET'])
def chat_show(request, id):
    chat = Chats.objects.filter(id=id).first()
    return ApiResponse(chat=ChatSerializer(chat).data if chat else None)

# Email Notification
@api_view(['GET'])
def email_notification_index(request):
    return ApiResponse(notifications=[])

@api_view(['GET'])
def email_notification_create(request):
    return ApiResponse(message="Email notification form")

@api_view(['POST'])
def email_notification_store(request):
    return ApiResponse(message="Email notification stored")

@api_view(['GET'])
def email_notification_edit(request, id):
    return ApiResponse(message="Email notification edit form")

@api_view(['PATCH'])
def email_notification_update(request, id):
    return ApiResponse(message="Email notification updated")

@api_view(['GET'])
def email_notification_destroy(request, id):
    return ApiResponse(message="Email notification deleted")

@api_view(['GET'])
def email_notification_show(request, id):
    return ApiResponse(notification={})

# --- Webhooks & Utilities ---

@api_view(['GET'])
def test_supervisor(request):
    return ApiResponse(message="Supervisor is running!")

@api_view(['POST'])
def sendgrid_webhook(request):
    # Depending on payload, we might process bouncing, drops, etc.
    data = request.data
    # For now, just accept
    return ApiResponse(message="Sendgrid webhook received")
