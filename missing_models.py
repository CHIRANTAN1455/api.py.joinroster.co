# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class States(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    country = models.ForeignKey('Countries', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'states'


class UserCreators(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    link = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=2000, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    followers = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    role_summary = models.CharField(max_length=2000, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    contract_type = models.JSONField(blank=True, null=True)
    till_present = models.SmallIntegerField(blank=True, null=True)
    creator_group = models.ForeignKey('CreatorGroups', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_creators'
        unique_together = (('user', 'link'),)


class Projects(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    editor = models.ForeignKey('Users', models.DO_NOTHING, related_name='projects_editor_set', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    budget_per = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    revisions = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    flow = models.CharField(max_length=255, blank=True, null=True)
    match_token = models.CharField(max_length=255, blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    utc_offset = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    published = models.IntegerField()
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    working_location = models.CharField(max_length=255, blank=True, null=True)
    interested_in = models.JSONField(blank=True, null=True)
    notify_editors = models.IntegerField(blank=True, null=True)
    custom_title = models.CharField(max_length=500, blank=True, null=True)
    min_budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    open_to_negotiate = models.SmallIntegerField(blank=True, null=True)
    banner_image = models.CharField(max_length=1000, blank=True, null=True)
    logo = models.CharField(max_length=1000, blank=True, null=True)
    hackathon = models.IntegerField(blank=True, null=True)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    assignment_url = models.CharField(max_length=1000, blank=True, null=True)
    assignment_type = models.CharField(max_length=50, blank=True, null=True)
    requirements = models.CharField(max_length=2000, blank=True, null=True)
    faqs = models.JSONField(blank=True, null=True)
    prizes = models.JSONField(blank=True, null=True)
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=500, blank=True, null=True)
    required_languages = models.JSONField(blank=True, null=True)
    currency = models.CharField(max_length=15, blank=True, null=True)
    accept_toc = models.SmallIntegerField(blank=True, null=True)
    hire_source = models.CharField(max_length=100, blank=True, null=True)
    hired_editor_ids = models.JSONField(blank=True, null=True)
    interviewed_editor_ids = models.JSONField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    offer_date = models.DateTimeField(blank=True, null=True)
    sent_rejection_email = models.SmallIntegerField(blank=True, null=True)
    to_send_rejection_email = models.SmallIntegerField(blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    feedback = models.CharField(max_length=1000, blank=True, null=True)
    custom_rejection_message = models.CharField(max_length=1000, blank=True, null=True)
    upload_constraints = models.JSONField(blank=True, null=True)
    toc_doc_id = models.CharField(max_length=255, blank=True, null=True)
    require_toc = models.SmallIntegerField(blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class UserProjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    project_type = models.ForeignKey('ProjectTypes', models.DO_NOTHING)
    link = models.CharField(max_length=255)
    icon = models.CharField(max_length=2000, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    views = models.CharField(max_length=255, blank=True, null=True)
    likes = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    job_type_id = models.PositiveBigIntegerField(blank=True, null=True)
    role_description = models.CharField(max_length=500, blank=True, null=True)
    followers = models.CharField(max_length=255, blank=True, null=True)
    individual_project = models.IntegerField(blank=True, null=True)
    user_creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_projects'
        unique_together = (('user', 'link'),)


class ProjectApplications(models.Model):
    note = models.CharField(max_length=2000, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    best_project_role = models.CharField(max_length=1000, blank=True, null=True)
    match_percent = models.IntegerField(blank=True, null=True)
    job_type_match_percent = models.IntegerField(blank=True, null=True)
    platform_match_percent = models.IntegerField(blank=True, null=True)
    content_vertical_match_percent = models.IntegerField(blank=True, null=True)
    skill_match_percent = models.IntegerField(blank=True, null=True)
    software_match_percent = models.IntegerField(blank=True, null=True)
    creative_style_match_percent = models.IntegerField(blank=True, null=True)
    uuid = models.CharField(max_length=36)
    project = models.ForeignKey(Projects, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255)
    budget_match_percent = models.IntegerField(blank=True, null=True)
    active = models.IntegerField()
    id = models.BigAutoField(primary_key=True)
    timezone_match_percent = models.IntegerField(blank=True, null=True)
    location_city_match_percent = models.IntegerField(blank=True, null=True)
    common_creator_match_percent = models.IntegerField(blank=True, null=True)
    common_category_match_percent = models.IntegerField(blank=True, null=True)
    availability_match_percent = models.IntegerField(blank=True, null=True)
    utm_source = models.CharField(max_length=255, blank=True, null=True)
    utm_medium = models.CharField(max_length=255, blank=True, null=True)
    utm_campaign = models.CharField(max_length=255, blank=True, null=True)
    relocate = models.IntegerField(blank=True, null=True)
    assignment_url = models.CharField(max_length=1000, blank=True, null=True)
    assignment_filename = models.CharField(max_length=500, blank=True, null=True)
    place = models.SmallIntegerField(blank=True, null=True)
    cover_letter_score = models.SmallIntegerField(blank=True, null=True)
    cover_letter_remarks = models.CharField(max_length=1000, blank=True, null=True)
    weighted_match_score = models.SmallIntegerField(blank=True, null=True)
    accept_toc = models.SmallIntegerField(blank=True, null=True)
    accept_toc_time = models.DateTimeField(blank=True, null=True)
    legal_name = models.CharField(max_length=200, blank=True, null=True)
    slack_notification_sent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_applications'


class Software(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'software'
