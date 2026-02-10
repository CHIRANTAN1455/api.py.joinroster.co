from django.urls import path
from .views import (
    skills_index, content_verticals_index, platforms_index, softwares_index,
    equipments_index, creative_styles_index, job_types_index,
    country_create, state_create, city_create, location_create,
    editor_create, invite,
    profile_get, profile_update, profile_pricing, profile_skills,
    profile_jobtypes, profile_contentverticals, profile_contentverticals_new,
    profile_platforms, profile_softwares, profile_equipments,
    profile_creativestyles, profile_social,
    location_index, location_get,
    user_project_index, user_project_public_index, user_project_add,
    user_project_update, user_project_delete, user_project_info,
    project_index, project_public_index, project_get, project_store,
    project_update, project_status_update,
    matching_index, matching_get, matching_store, matching_update, matching_editor_update,
    editor_index, editor_get, editor_projects, editor_creators, editor_reviews,
    project_application_index, project_application_get, project_application_store,
    project_application_update, project_application_create_note,
    project_application_delete_note, project_application_send_rejection_email,
    project_screening_question_index, project_screening_question_store,
    project_screening_question_show, project_screening_question_update,
    project_screening_question_destroy,
    customer_get_by_user, customer_upgrade, customer_generate_subscription_link,
    customer_stop_email_webhook, customer_update_expiry_from_stripe
)
from . import views # Keep this for views.test_api

urlpatterns = [
    path('test', views.test_api),
    path('skills', skills_index),
    path('contentverticals', content_verticals_index),
    path('platforms', platforms_index),
    path('softwares', softwares_index),
    path('equipments', equipments_index),
    path('creativestyles', creative_styles_index, name='creative_styles_index'),
    path('jobtypes', job_types_index, name='job_types_index'),

    # DataController Endpoints
    path('country', country_create, name='country_create'),
    path('state', state_create, name='state_create'),
    path('city', city_create, name='city_create'),
    path('location', location_create, name='location_create'),
    path('editor', editor_create, name='editor_create'),
    path('invite', invite, name='invite'),

    # ProfileController Endpoints
    path('profile', profile_get, name='profile_get'),
    path('profile/update', profile_update, name='profile_update'),
    path('profile/pricing', profile_pricing, name='profile_pricing'),
    path('profile/skills', profile_skills, name='profile_skills'),
    path('profile/jobtypes', profile_jobtypes, name='profile_jobtypes'),
    path('profile/contentverticals', profile_contentverticals, name='profile_contentverticals'),
    path('profile/contentverticals/new', profile_contentverticals_new, name='profile_contentverticals_new'),
    path('profile/platforms', profile_platforms, name='profile_platforms'),
    path('profile/softwares', profile_softwares, name='profile_softwares'),
    path('profile/equipments', profile_equipments, name='profile_equipments'),
    path('profile/creativestyles', profile_creativestyles, name='profile_creativestyles'),
    path('profile/social', profile_social, name='profile_social'),
    path('profile/statistics', views.profile_statistics, name='profile_statistics'),
    path('profile/convert', views.profile_convert_as_creator, name='profile_convert_as_creator'),
    path('profile/refresh-token', views.profile_refresh_token, name='profile_refresh_token'),
    
    # Additional Index Endpoints
    path('contentforms', content_forms_index, name='content_forms_index'),
    path('projecttypes', project_types_index, name='project_types_index'),
    path('projecttypes/<username>', project_types_index, name='project_types_index_user'),
    path('reasons', reasons_index, name='reasons_index'),
    path('referrals', referrals_index, name='referrals_index'),
    
    # Location Endpoints
    path('location', location_index, name='location_index'),
    path('location/<int:id>', location_get, name='location_get'),
    
    # Authentication Endpoints
    path('auth/init', views.auth_init, name='auth_init'),
    path('auth/login', views.auth_login, name='auth_login'),
    path('auth/register', views.auth_register, name='auth_register'),
    path('auth/otp', views.auth_otp, name='auth_otp'),
    path('auth/verify', views.auth_verify, name='auth_verify'),
    path('auth/reset/otp', views.auth_reset_otp, name='auth_reset_otp'),
    path('auth/reset', views.auth_reset_password, name='auth_reset_password'),
    path('auth/password', views.auth_change_password, name='auth_change_password'),
    path('auth/logout', views.auth_logout, name='auth_logout'),
    
    # User Management Endpoints
    path('user/<uuid>', views.user_update, name='user_update'),
    path('user/<uuid>/timezone', views.user_update_timezone, name='user_update_timezone'),
    path('user/<uuid>/policy', views.user_update_policy, name='user_update_policy'),
    path('user/<uuid>/delete', views.user_delete, name='user_delete'),
    path('user/referral/<code>', views.user_by_referral_code, name='user_by_referral_code'),
    path('user/<uuid>/platforms', views.user_update_platforms, name='user_update_platforms'),
    path('user/<uuid>/jobtypes', views.user_update_jobtypes_pricing, name='user_update_jobtypes_pricing'),
    path('user/<uuid>/content-vertical', views.user_update_content_vertical, name='user_update_content_vertical'),
    path('user/<uuid>/unsubscribe', views.user_unsubscribe, name='user_unsubscribe'),
    path('user/<id>/revert-time', views.user_revert_update_time, name='user_revert_update_time'),
    path('user/<uuid>/post-slack', views.user_post_to_slack, name='user_post_to_slack'),
    
    # User Social Accounts Endpoints
    path('user/social', views.user_social_index, name='user_social_index'),
    path('user/social/create', views.user_social_create, name='user_social_create'),
    path('user/social/<uuid>', views.user_social_delete, name='user_social_delete'),
    path('user/social/content-topics', views.user_social_content_topics, name='user_social_content_topics'),
    
    # User Payment Methods Endpoints
    path('user/payment', views.user_payment_index, name='user_payment_index'),
    path('user/payment/create', views.user_payment_create, name='user_payment_create'),
    path('user/payment/<uuid>', views.user_payment_delete, name='user_payment_delete'),
    
    # User Creator Endpoints
    path('user/creator', views.user_creator_index, name='user_creator_index'),
    path('user/creator/unverified', views.user_creator_unverified, name='user_creator_unverified'),
    path('user/creator/search', views.user_creator_search, name='user_creator_search'),
    path('user/creator/add', views.user_creator_add, name='user_creator_add'),
    path('user/creator/<uuid>', views.user_creator_update, name='user_creator_update'),
    path('user/creator/<uuid>/delete', views.user_creator_delete, name='user_creator_delete'),
    path('user/creator/<uuid>/projects', views.user_creator_projects, name='user_creator_projects'),
    path('user/creator/content/topics', views.user_creator_get_content_topics, name='user_creator_get_content_topics'),
    path('user/creator/info', views.user_creator_get_info, name='user_creator_get_info'),
    path('user/creator/info/public', views.user_creator_get_public_info, name='user_creator_get_public_info'),
    path('user/creator/similar', views.user_creator_get_similar, name='user_creator_get_similar'),
    path('user/creator/invite/colleagues', views.user_creator_invite_colleagues, name='user_creator_invite_colleagues'),
    path('user/creator/username/<username>', views.user_creator_get_by_username, name='user_creator_get_by_username'),
    path('user/creator/group/create', views.user_creator_create_group, name='user_creator_create_group'),
    path('user/creator/search/public', views.user_creator_search_public, name='user_creator_search_public'),
    
    # Project Application Endpoints
    path('project/application', views.project_application_index, name='project_application_index'),
    path('project/application/<uuid>', views.project_application_get, name='project_application_get'),
    path('project/application/store', views.project_application_store, name='project_application_store'),
    path('project/application/<uuid>/update', views.project_application_update, name='project_application_update'),
    path('project/application/<uuid>/note', views.project_application_create_note, name='project_application_create_note'),
    path('project/application/note/<uuid>', views.project_application_delete_note, name='project_application_delete_note'),
    path('project/application/rejection/email', views.project_application_send_rejection_email, name='project_application_send_rejection_email'),
    
    # User Verification Link Endpoints
    path('user/verification/link', views.user_verification_link_index, name='user_verification_link_index'),
    path('user/verification/link/add', views.user_verification_link_add, name='user_verification_link_add'),
    path('user/verification/link/addMany', views.user_verification_link_add_many, name='user_verification_link_add_many'),
    path('user/verification/link/<uuid>/delete', views.user_verification_link_delete, name='user_verification_link_delete'),

    # User Project Endpoints
    path('userproject', user_project_index, name='user_project_index'),
    path('userproject/public', user_project_public_index, name='user_project_public_index'),
    path('userproject/add', user_project_add, name='user_project_add'),
    path('userproject/<uuid>/update', user_project_update, name='user_project_update'),
    path('userproject/<uuid>', user_project_delete, name='user_project_delete'),
    path('userproject/info', user_project_info, name='user_project_info'),

    # Project Endpoints
    path('project', project_index, name='project_index'),
    path('project/public', project_public_index, name='project_public_index'),
    path('project/store', project_store, name='project_store'),
    path('project/<uuid>', project_get, name='project_get'),
    path('project/<uuid>/update', project_update, name='project_update'),
    path('project/<uuid>/status', project_status_update, name='project_status_update'),

    # Matching Endpoints
    path('matching', matching_index, name='matching_index'),
    path('matching/<uuid>', matching_get, name='matching_get'),
    path('matching/store', matching_store, name='matching_store'),
    path('matching/<uuid>/update', matching_update, name='matching_update'),
    path('matching/editor/update', matching_editor_update, name='matching_editor_update'),

    # Editor Endpoints
    path('editors', editor_index, name='editor_index'),
    path('editor/<username>', editor_get, name='editor_get'),
    path('editor/<username>/projects', editor_projects, name='editor_projects'),
    path('editor/<username>/creators', editor_creators, name='editor_creators'),
    path('editor/<username>/reviews', editor_reviews, name='editor_reviews'),

    # Project Application Endpoints
    path('project/application', project_application_index, name='project_application_index'),
    path('project/application/<uuid>', project_application_get, name='project_application_get'),
    path('project/application/store', project_application_store, name='project_application_store'),
    path('project/application/<uuid>/update', project_application_update, name='project_application_update'),
    path('project/application/<uuid>/note', project_application_create_note, name='project_application_create_note'),
    path('project/application/note/<uuid>', project_application_delete_note, name='project_application_delete_note'),
    path('project/application/rejection/email', project_application_send_rejection_email, name='project_application_send_rejection_email'),

    # Project Screening Question Endpoints
    path('project/<project_uuid>/screening-questions', project_screening_question_index, name='project_screening_question_index'),
    path('project/<project_uuid>/screening-questions/store', project_screening_question_store, name='project_screening_question_store'),
    path('project/<project_uuid>/screening-questions/<question_uuid>', project_screening_question_show, name='project_screening_question_show'),
    path('project/<project_uuid>/screening-questions/<question_uuid>/update', project_screening_question_update, name='project_screening_question_update'),
    path('project/<project_uuid>/screening-questions/<question_uuid>/delete', project_screening_question_destroy, name='project_screening_question_destroy'),

    # Customer Endpoints
    path('customer/me', customer_get_by_user, name='customer_get_by_user'),
    path('customer/upgrade', customer_upgrade, name='customer_upgrade'),
    path('customer/subscription-link', customer_generate_subscription_link, name='customer_generate_subscription_link'),
    path('customer/email-stop-webhook', customer_stop_email_webhook, name='customer_stop_email_webhook'),
    path('customer/stripe-expiry-update', customer_update_expiry_from_stripe, name='customer_update_expiry_from_stripe'),
]
