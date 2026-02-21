import re
import uuid

# 1. Update serializers.py
with open('roster_api/serializers.py', 'r') as f:
    serializers_content = f.read()

new_serializers = """
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'

"""
# Find a place to inject these, right after RoleSerializer or at the end
if 'class PermissionSerializer' not in serializers_content:
    # Just append at the end
    serializers_content += new_serializers
    with open('roster_api/serializers.py', 'w') as f:
        f.write(serializers_content)

# 2. Generate Views
views_addition = """
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

"""

with open('roster_api/views.py', 'r') as f:
    views_content = f.read()

# Make sure we don't append multiple times
if 'menu_index(request):' not in views_content:
    # Need to add PermissionSerializer and MenuSerializer imports in views.py
    views_content = views_content.replace(
        'RoleSerializer,',
        'RoleSerializer,\n    PermissionSerializer,\n    MenuSerializer,'
    )
    # The models might already be imported, but check
    if 'Roles,' not in views_content:
        # It's there, we just replace
        pass
        
    views_content += views_addition
    with open('roster_api/views.py', 'w') as f:
        f.write(views_content)

# 3. Update urls.py
with open('roster_api/urls.py', 'r') as f:
    urls_content = f.read()

imports_to_add = """
from .views import (
    role_index, role_store, role_update, role_destroy, role_show,
    permission_index, permission_store, permission_update, permission_destroy, permission_show,
    menu_index, menu_store, menu_update, menu_destroy, menu_show
)
"""

urls_addition_block = """
    # --- Core User Management Endpoints ---
    path('role', role_index, name='role_index'),
    path('role/add', role_store, name='role_store'),
    path('role/update', role_update, name='role_update'),
    path('role/delete/<int:id>', role_destroy, name='role_destroy'),
    path('role/<int:id>', role_show, name='role_show'),

    path('permission', permission_index, name='permission_index'),
    path('permission/add', permission_store, name='permission_store'),
    path('permission/update', permission_update, name='permission_update'),
    path('permission/delete/<int:id>', permission_destroy, name='permission_destroy'),
    path('permission/<int:id>', permission_show, name='permission_show'),

    path('menu', menu_index, name='menu_index'),
    path('menu/add', menu_store, name='menu_store'),
    path('menu/update', menu_update, name='menu_update'),
    path('menu/delete/<int:id>', menu_destroy, name='menu_destroy'),
    path('menu/<int:id>', menu_show, name='menu_show'),
"""

if 'role_index' not in urls_content:
    urls_content = urls_content.replace('from . import views # Keep this for views.test_api', imports_to_add + '\nfrom . import views # Keep this for views.test_api')
    urls_content = re.sub(r'\]\n*$', urls_addition_block + "\n]\n", urls_content)

    with open('roster_api/urls.py', 'w') as f:
        f.write(urls_content)

print("Added Core User CRUD Endpoints")
