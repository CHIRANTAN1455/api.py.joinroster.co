import re

views_addition = """
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
"""

with open('roster_api/views.py', 'r') as f:
    views_content = f.read()

if 'dashboard_index(request):' not in views_content:
    views_content += views_addition
    with open('roster_api/views.py', 'w') as f:
        f.write(views_content)

with open('roster_api/urls.py', 'r') as f:
    urls_content = f.read()

imports_to_add = """
from .views import (
    dashboard_index, user_index, user_list, user_create, user_store,
    user_destroy, user_show, user_edit, user_update_patch, user_photo,
    profile_edit, profile_photo, profile_password,
    setting_system, setting_api, setting_app
)
"""

urls_addition_block = """
    path('dashboard', dashboard_index, name='dashboard_index'),
    path('user', user_index, name='user_index_main'),
    path('user/list', user_list, name='user_list'),
    path('user/add', user_create, name='user_create_form'),
    path('user/store', user_store, name='user_store_new'),
    path('user/delete/<int:id>', user_destroy, name='user_destroy_id'),
    path('user/<int:id>', user_show, name='user_show_id'),
    path('user/<int:id>/edit', user_edit, name='user_edit_id'),
    path('user/<int:id>/patch', user_update_patch, name='user_update_patch_id'), # We mapped PATCH /user/{id} to this logic
    path('user/photo', user_photo, name='user_photo'),
    
    path('profile/edit', profile_edit, name='profile_edit'),
    path('profile/photo', profile_photo, name='profile_photo'),
    path('profile/password', profile_password, name='profile_password'),
    
    path('setting/system', setting_system, name='setting_system'),
    path('setting/api', setting_api, name='setting_api'),
    path('setting/app', setting_app, name='setting_app'),
"""

if 'dashboard_index' not in urls_content:
    urls_content = urls_content.replace('from . import views # Keep this for views.test_api', imports_to_add + '\nfrom . import views # Keep this for views.test_api')
    
    # We should add PATCH for user: Laravel `Route::patch('/user/{id}', 'update')->name('user.update');`
    # Let's map it via Django route
    urls_content = re.sub(r'\]\n*$', urls_addition_block + "\n]\n", urls_content)

    with open('roster_api/urls.py', 'w') as f:
        f.write(urls_content)

print("Added Dashboard, User, Profile, Setting CRUDs")
