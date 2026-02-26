
@api_view(['POST'])
def skill_store(request):
    data = request.data
    Skills.objects.create(
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
        uuid=str(uuid_lib.uuid4()),
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
