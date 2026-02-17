# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import sys


class ChatMessages(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    chat = models.ForeignKey('Chats', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    recipient_id = models.BigIntegerField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_messages'


class Chats(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    participants = models.JSONField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chats'


class Cities(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    state = models.ForeignKey('States', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    wiki_data_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class ContentForms(models.Model):
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
        db_table = 'content_forms'


class ContentTopics(models.Model):
    name = models.CharField(max_length=500)
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    youtube_topic_id = models.CharField(max_length=255, blank=True, null=True)
    subtopics = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_topics'


class ContentVerticals(models.Model):
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
        db_table = 'content_verticals'


class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=255)
    numeric_code = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=255)
    phone_code = models.CharField(max_length=255)
    capital = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255)
    currency_name = models.CharField(max_length=255)
    currency_symbol = models.CharField(max_length=255)
    tld = models.CharField(max_length=255)
    native = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    subregion = models.CharField(max_length=255, blank=True, null=True)
    timezones = models.JSONField()
    translations = models.JSONField()
    latitude = models.DecimalField(max_digits=8, decimal_places=2)
    longitude = models.DecimalField(max_digits=8, decimal_places=2)
    emoji = models.CharField(max_length=255)
    emojiu = models.CharField(db_column='emojiU', max_length=255)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class CreativeStyles(models.Model):
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
        db_table = 'creative_styles'


class CreatorGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    username = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    links = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    banner = models.CharField(max_length=500, blank=True, null=True)
    logo = models.CharField(max_length=500, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    followers_type = models.CharField(max_length=100, blank=True, null=True)
    similar_creators = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator_groups'


class CreatorSocialIdentityChecks(models.Model):
    id = models.BigAutoField(primary_key=True)
    creator = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    vouch_request = models.ForeignKey('CreatorVouchRequests', models.DO_NOTHING, blank=True, null=True)
    youtube_channel_id = models.CharField(max_length=255, blank=True, null=True)
    verification_status = models.CharField(max_length=10)
    verified_at = models.DateTimeField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator_social_identity_checks'


class CreatorVerificationTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    vouch_request = models.ForeignKey('CreatorVouchRequests', models.DO_NOTHING)
    token = models.CharField(unique=True, max_length=255)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator_verification_tokens'


class CreatorVouchAttemptLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    vouch_request = models.ForeignKey('CreatorVouchRequests', models.DO_NOTHING)
    attempt_type = models.CharField(max_length=13)
    attempt_status = models.CharField(max_length=6)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator_vouch_attempt_logs'


class CreatorVouchOutcomes(models.Model):
    id = models.BigAutoField(primary_key=True)
    vouch_request = models.ForeignKey('CreatorVouchRequests', models.DO_NOTHING)
    outcome = models.CharField(max_length=21)
    reason = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator_vouch_outcomes'


class CreatorVouchRequests(models.Model):
    id = models.BigAutoField(primary_key=True)
    supplier = models.ForeignKey('Users', models.DO_NOTHING)
    creator = models.ForeignKey('Users', models.DO_NOTHING, related_name='creatorvouchrequests_creator_set', blank=True, null=True)
    exp_creator = models.ForeignKey('UserCreators', models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=12)
    attempts_count = models.IntegerField()
    last_attempt_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator_vouch_requests'



class Customers(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    payment_type = models.ForeignKey('PaymentTypes', models.DO_NOTHING)
    payment_status = models.ForeignKey('PaymentStatuses', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    payment_cycle = models.CharField(max_length=50, blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'



class EditorShortlists(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    editor = models.ForeignKey('Users', models.DO_NOTHING)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    matching = models.ForeignKey('Matchings', models.DO_NOTHING, blank=True, null=True)
    match = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='editorshortlists_user_set', blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    rejected = models.IntegerField(blank=True, null=True)
    rejection_email_template = models.CharField(max_length=5000, blank=True, null=True)
    project_application = models.ForeignKey('ProjectApplications', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editor_shortlists'




class Equipment(models.Model):
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
        db_table = 'equipment'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Files(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    meta = models.TextField(blank=True, null=True)
    reference_name = models.CharField(max_length=255)
    reference_id = models.CharField(max_length=255)
    public = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class HackathonApplicantAssignments(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    project_application = models.ForeignKey('ProjectApplications', models.DO_NOTHING)
    assignment_url = models.TextField()
    assignment_filename = models.CharField(max_length=255, blank=True, null=True)
    file_format = models.CharField(max_length=50, blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hackathon_applicant_assignments'


class InterestFormSurvey(models.Model):
    id = models.BigAutoField(primary_key=True)
    survey_id = models.PositiveBigIntegerField()
    survey_title = models.CharField(max_length=255, blank=True, null=True)
    survey_status = models.CharField(max_length=50, blank=True, null=True)
    survey_url_slug = models.CharField(max_length=255, blank=True, null=True)
    survey_created_at = models.DateTimeField(blank=True, null=True)
    feature_id = models.PositiveBigIntegerField(blank=True, null=True)
    feature_name = models.CharField(max_length=255, blank=True, null=True)
    feature_description = models.TextField(blank=True, null=True)
    feature_image_url = models.CharField(max_length=500, blank=True, null=True)
    feature_display_order = models.IntegerField(blank=True, null=True)
    response_id = models.PositiveBigIntegerField(blank=True, null=True)
    response_timestamp = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    additional_feedback = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    rating_id = models.PositiveBigIntegerField(blank=True, null=True)
    rating_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interest_form_survey'


class JobTypeSkills(models.Model):
    job_type = models.ForeignKey('JobTypes', models.DO_NOTHING)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_type_skills'
        unique_together = (('job_type', 'skill'),)


class JobTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    hide_from_customers = models.IntegerField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_types'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=255)
    payload = models.TextField()
    attempts = models.PositiveIntegerField()
    reserved_at = models.PositiveIntegerField(blank=True, null=True)
    available_at = models.PositiveIntegerField()
    created_at = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'jobs'


class Locations(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    city = models.CharField(max_length=255)
    city_ascii = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=255)
    admin_name = models.CharField(max_length=255, blank=True, null=True)
    capital = models.CharField(max_length=255, blank=True, null=True)
    population = models.CharField(max_length=255, blank=True, null=True)
    lat = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class Logs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    action = models.CharField(max_length=255)
    data = models.JSONField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class MatchingContentVerticals(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    content_vertical = models.ForeignKey(ContentVerticals, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_content_verticals'
        unique_together = (('matching', 'content_vertical'),)


class MatchingCreativeStyles(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    creative_style = models.ForeignKey(CreativeStyles, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_creative_styles'
        unique_together = (('matching', 'creative_style'),)


class MatchingEditors(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    editor = models.ForeignKey('Users', models.DO_NOTHING)
    match = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'matching_editors'


class MatchingJobTypes(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    job_type = models.ForeignKey(JobTypes, models.DO_NOTHING)
    starting_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pricing_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_job_types'
        unique_together = (('matching', 'job_type'),)


class MatchingPlatforms(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    platform = models.ForeignKey('Platforms', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_platforms'
        unique_together = (('matching', 'platform'),)


class MatchingSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    element = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_settings'


class MatchingSkills(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_skills'
        unique_together = (('matching', 'skill'),)


class MatchingSoftware(models.Model):
    matching = models.ForeignKey('Matchings', models.DO_NOTHING)
    software = models.ForeignKey('Software', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_software'
        unique_together = (('matching', 'software'),)


class Matchings(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    average_turnaround_time = models.IntegerField(blank=True, null=True)
    interested_in = models.JSONField(blank=True, null=True)
    token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    project_id = models.PositiveBigIntegerField(blank=True, null=True)
    flow = models.CharField(max_length=255, blank=True, null=True)
    utc_offset = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    min_budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matchings'


class Menus(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    priority = models.IntegerField()
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menus'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Otps(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    code = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otps'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class PaymentStatuses(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=36)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'payment_statuses'


class PaymentTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=36)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'payment_types'


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class Platforms(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    hide_from_customers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'platforms'


class ProfileVisits(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    editor = models.ForeignKey('Users', models.DO_NOTHING, related_name='profilevisits_editor_set')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

class Skills(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    hide_from_customers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'

class Reasons(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tags = models.JSONField(blank=True, null=True)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reasons'

class Referrals(models.Model):
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
        db_table = 'referrals'

class UserSocials(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    platform = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    external_user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_socials'
        unique_together = (('user', 'platform'),)

class UserPayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    gateway = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    external_user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_payments'

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    photo = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone_verified_at = models.DateTimeField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    yt_verified = models.IntegerField()
    activated_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)
    fun_fact = models.CharField(max_length=3000, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=255, blank=True, null=True)
    utc_offset = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    open_for_work = models.IntegerField(blank=True, null=True)
    resume = models.CharField(max_length=1000, blank=True, null=True)
    resume_updated_at = models.DateTimeField(blank=True, null=True)
    new_onboarding = models.SmallIntegerField(blank=True, null=True)
    worked_with_creators = models.SmallIntegerField(blank=True, null=True)
    via_affiliate = models.SmallIntegerField(blank=True, null=True)
    referral_discount_amount = models.SmallIntegerField(blank=True, null=True)
    referral_discount_type = models.CharField(max_length=50, blank=True, null=True)
    import_via_linkedin = models.SmallIntegerField(blank=True, null=True)
    referral_discount_interval = models.SmallIntegerField(blank=True, null=True)
    import_via_resume = models.SmallIntegerField(blank=True, null=True)
    sign_up_path = models.CharField(max_length=15, blank=True, null=True)
    discount_code = models.CharField(max_length=255, blank=True, null=True)
    special_referrer_source = models.CharField(max_length=50, blank=True, null=True)
    activated_by = models.BigIntegerField(blank=True, null=True)
    completion_status = models.CharField(max_length=10, blank=True, null=True)
    policy_accepted = models.IntegerField(blank=True, null=True, db_comment='Whether the user has accepted the policy')
    policy_accepted_at = models.DateTimeField(blank=True, null=True, db_comment='When the user accepted the policy')

    class Meta:
        managed = False
        db_table = 'users'
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
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ProjectTypes(models.Model):
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
        db_table = 'project_types'

class UserSkills(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_skills'
        unique_together = (('user', 'skill'),)


class UserContentVerticals(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    content_vertical = models.ForeignKey('ContentVerticals', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_content_verticals'
        unique_together = (('user', 'content_vertical'),)


class UserPlatforms(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    platform = models.ForeignKey('Platforms', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_platforms'
        unique_together = (('user', 'platform'),)

class UserPricing(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    average_turnaround_time = models.CharField(max_length=255, blank=True, null=True)
    interested_in = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_pricings'

class UserSoftware(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    software = models.ForeignKey('Software', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_software'
        unique_together = (('user', 'software'),)

class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'

class UserRoles(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    role = models.ForeignKey('Roles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_roles'
        unique_together = (('user', 'role'),)

class UserLanguage(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_languages'

class UserSocialProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField('Users', models.DO_NOTHING)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    other_link = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    followers = models.BigIntegerField(blank=True, null=True)
    follower_type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_social_profiles'

class UserJobTypePricing(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    job_type = models.ForeignKey('JobTypes', models.DO_NOTHING)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pricing_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_job_type_pricings'

class UserSocialProfileContentTopics(models.Model):
    user_social_profile = models.ForeignKey('UserSocialProfile', models.DO_NOTHING)
    content_topic = models.ForeignKey('ContentTopics', models.DO_NOTHING)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_social_profile_content_topics'
        unique_together = (('user_social_profile', 'content_topic'),)

class UserEquipments(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    equipment = models.ForeignKey('Equipment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_equipments'
        unique_together = (('user', 'equipment'),)

class UserCreativeStyles(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    creative_style = models.ForeignKey('CreativeStyles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_creative_styles'
        unique_together = (('user', 'creative_style'),)

class UserJobTypes(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    job_type = models.ForeignKey('JobTypes', models.DO_NOTHING)
    primary_job = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'user_job_types'
        unique_together = (('user', 'job_type'),)

class QuestionTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    validation_rules = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question_types'


class ProjectScreeningQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    project = models.ForeignKey(Projects, models.DO_NOTHING)
    question_type = models.ForeignKey(QuestionTypes, models.DO_NOTHING)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    placeholder = models.TextField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True)
    is_required = models.IntegerField()
    sort_order = models.IntegerField()
    active = models.IntegerField()
    validation_rules = models.JSONField(blank=True, null=True)
    custom_tips = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_screening_questions'


class ProjectApplicationNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    project_application = models.ForeignKey('ProjectApplications', models.DO_NOTHING)
    text = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_application_notes'


class ProjectScreeningAnswers(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    project_screening_question = models.ForeignKey(ProjectScreeningQuestions, models.DO_NOTHING)
    project_application = models.ForeignKey('ProjectApplications', models.DO_NOTHING)
    answer_text = models.TextField(blank=True, null=True)
    answer_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_screening_answers'
        unique_together = (('project_screening_question', 'project_application'),)


class CustomScreeningQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Projects, models.DO_NOTHING)
    project_uuid = models.CharField(max_length=36, blank=True, null=True)
    applicant_uuid = models.CharField(max_length=36, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    is_required = models.IntegerField()
    question_type = models.CharField(max_length=30)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custom_screening_questions'

class UserVerificationLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    link = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    attachment = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    approved = models.SmallIntegerField(blank=True, null=True)
    approved_by = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_verification_links'
        unique_together = (('user', 'link', 'deleted_at'),)


class UserFavourites(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='userfavourites_user_set')
    favourite_user = models.ForeignKey('Users', models.DO_NOTHING, related_name='userfavourites_favourite_user_set')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_favourites'

class Setting(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    element = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = 'test' in sys.argv
        db_table = 'settings'


class EditorInvitations(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True, db_column='referrer_id')
    referrer_project = models.ForeignKey('UserProjects', models.DO_NOTHING, blank=True, null=True, db_column='referrer_project_id')
    referrer_creator = models.ForeignKey('UserCreators', models.DO_NOTHING, blank=True, null=True, db_column='referrer_creator_id')
    password_reset_link = models.CharField(max_length=500, blank=True, null=True)
    job_type = models.ForeignKey('JobTypes', models.DO_NOTHING, blank=True, null=True, db_column='job_type_id')
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editor_invitations'


class UserProjectContentTopics(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    user_project = models.ForeignKey('UserProjects', models.DO_NOTHING)
    content_topic = models.ForeignKey('ContentTopics', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_project_content_topics'


class UserCreatorContentTopics(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    user_creator = models.ForeignKey('UserCreators', models.DO_NOTHING)
    content_topic = models.ForeignKey('ContentTopics', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_creator_content_topics'


class EmailNotifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_notifications'


class EmailNotificationLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    email_notification = models.ForeignKey('EmailNotifications', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_notification_logs'


class ProjectJobTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    job_type = models.ForeignKey('JobTypes', models.DO_NOTHING)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pricing_type = models.CharField(max_length=255, blank=True, null=True)
    optional = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_job_types'


class UserVerifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    attachment = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_verifications'


class UserEmailUnsubscriptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    email_notification_id = models.BigIntegerField(blank=True, null=True) 
    notification_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_email_unsubscriptions'


class Transactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    status = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'transactions'


class ReferralCodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    code = models.CharField(max_length=255, blank=True, null=True)
    referrer_id = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_codes'
