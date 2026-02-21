import os

MODELS = [
    # (model_name, plural_name (for return key), serializer_name, prefix)
    ("Skills", "skills", "SkillSerializer", "skill"),
    ("JobTypes", "jobtypes", "JobTypeSerializer", "job_types"),
    ("Equipment", "equipments", "EquipmentSerializer", "equipment"),
    ("Software", "softwares", "SoftwareSerializer", "software"),
    ("Platforms", "platforms", "PlatformSerializer", "platform"),
    ("ContentVerticals", "contentverticals", "ContentVerticalSerializer", "content_vertical"),
    ("CreativeStyles", "creativestyles", "CreativeStyleSerializer", "creative_style"),
    ("ContentForms", "content_forms", "ContentFormSerializer", "content_form"),
    ("ProjectTypes", "project_types", "ProjectTypeSerializer", "project_type"),
    ("Reasons", "reasons", "ReasonSerializer", "reason"),
    ("Referrals", "referrals", "ReferralSerializer", "referral"),
]

TEMPLATE = """
@api_view(['POST'])
def {prefix}_store(request):
    data = request.data
    {model_name}.objects.create(
        uuid=str(uuid_lib.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = {model_name}.objects.filter(active=1)
    return ApiResponse({plural_name}={serializer_name}(items, many=True).data)

@api_view(['POST'])
def {prefix}_update(request):
    data = request.data
    item_id = data.get('id')
    {model_name}.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        icon=data.get('icon'),
        active=data.get('active', 1)
    )
    items = {model_name}.objects.filter(active=1)
    return ApiResponse({plural_name}={serializer_name}(items, many=True).data)

@api_view(['GET'])
def {prefix}_destroy(request, id):
    {model_name}.objects.filter(id=id).delete()
    items = {model_name}.objects.filter(active=1)
    return ApiResponse({plural_name}={serializer_name}(items, many=True).data)

@api_view(['GET'])
def {prefix}_show(request, id):
    item = {model_name}.objects.filter(id=id).first()
    return ApiResponse({prefix}={serializer_name}(item).data if item else None)
"""

REASON_TEMPLATE = """
@api_view(['POST'])
def {prefix}_store(request):
    data = request.data
    {model_name}.objects.create(
        uuid=str(uuid_lib.uuid4()),
        name=data.get('name'),
        description=data.get('description', ''),
        tags=data.get('tags'),
        active=data.get('active', 1)
    )
    items = {model_name}.objects.filter(active=1)
    return ApiResponse({plural_name}={serializer_name}(items, many=True).data)

@api_view(['POST'])
def {prefix}_update(request):
    data = request.data
    item_id = data.get('id')
    {model_name}.objects.filter(id=item_id).update(
        name=data.get('name'),
        description=data.get('description', ''),
        tags=data.get('tags'),
        active=data.get('active', 1)
    )
    items = {model_name}.objects.filter(active=1)
    return ApiResponse({plural_name}={serializer_name}(items, many=True).data)

@api_view(['GET'])
def {prefix}_destroy(request, id):
    {model_name}.objects.filter(id=id).delete()
    items = {model_name}.objects.filter(active=1)
    return ApiResponse({plural_name}={serializer_name}(items, many=True).data)

@api_view(['GET'])
def {prefix}_show(request, id):
    item = {model_name}.objects.filter(id=id).first()
    return ApiResponse({prefix}={serializer_name}(item).data if item else None)
"""

URL_TEMPLATE = """
    path('{url_prefix}/add', {prefix}_store, name='{prefix}_store'),
    path('{url_prefix}/update', {prefix}_update, name='{prefix}_update'),
    path('{url_prefix}/delete/<int:id>', {prefix}_destroy, name='{prefix}_destroy'),
    path('{url_prefix}/<int:id>', {prefix}_show, name='{prefix}_show'),
"""

URL_PREFIXES = {
    "skill": "skill",
    "job_types": "job-type",
    "equipment": "equipment",
    "software": "software",
    "platform": "platform",
    "content_vertical": "content-vertical",
    "creative_style": "creative-style",
    "content_form": "content-form",
    "project_type": "project-type",
    "reason": "reason",
    "referral": "referral"
}

views_code = ""
urls_code = ""

for model, plural, serial, prefix in MODELS:
    if model == "Reasons":
        views_code += REASON_TEMPLATE.format(model_name=model, plural_name=plural, serializer_name=serial, prefix=prefix)
    else:
        views_code += TEMPLATE.format(model_name=model, plural_name=plural, serializer_name=serial, prefix=prefix)
    
    url_pfx = URL_PREFIXES[prefix]
    urls_code += URL_TEMPLATE.format(url_prefix=url_pfx, prefix=prefix)

with open('taxonomy_crud_views.py', 'w') as f:
    f.write(views_code)

with open('taxonomy_crud_urls.py', 'w') as f:
    f.write(urls_code)
