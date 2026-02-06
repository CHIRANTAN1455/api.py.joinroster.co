# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
