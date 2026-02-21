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
    customer_register, customer_get_by_user, customer_upgrade, customer_generate_subscription_link,
    customer_stop_email_webhook, customer_update_expiry_from_stripe,
    chat_index, chat_get, chat_message, chat_create_custom_message,
    chat_init, chat_init_public, chat_get_received_messages, chat_update_message,
    favourite_index, favourite_store, profile_visit_store,
    matching_get_by_project_id, matching_public_create, matching_get_by_token,
    matching_create_from_favorite_creators, matching_admin_update,
    content_forms_index, project_types_index, project_types_user_index, reasons_index, referrals_index,
    settings_index, settings_store, settings_update, settings_destroy
)

from .views import (
    skill_store, skill_update, skill_destroy, skill_show,
    job_types_store, job_types_update, job_types_destroy, job_types_show,
    equipment_store, equipment_update, equipment_destroy, equipment_show,
    software_store, software_update, software_destroy, software_show,
    platform_store, platform_update, platform_destroy, platform_show,
    content_vertical_store, content_vertical_update, content_vertical_destroy, content_vertical_show,
    creative_style_store, creative_style_update, creative_style_destroy, creative_style_show,
    content_form_store, content_form_update, content_form_destroy, content_form_show,
    project_type_store, project_type_update, project_type_destroy, project_type_show,
    reason_store, reason_update, reason_destroy, reason_show,
    referral_store, referral_update, referral_destroy, referral_show
)


from .views import (
    role_index, role_store, role_update, role_destroy, role_show,
    permission_index, permission_store, permission_update, permission_destroy, permission_show,
    menu_index, menu_store, menu_update, menu_destroy, menu_show
)


from .views import (
    dashboard_index, user_index, user_list, user_create, user_store,
    user_destroy, user_show, user_edit, user_update_patch, user_photo,
    profile_edit, profile_photo, profile_password,
    setting_system, setting_api, setting_app
)


from .views import (
    editor_list, editor_create, editor_store, editor_destroy, editor_show, editor_edit,
    editor_update, editor_verification, editor_activation, editor_invite, editor_project,
    editor_delete_project, editor_creator, editor_delete_creator, editor_send_verification_email,
    editor_update_verification_note, editor_approve_verification, editor_delete_verification_note,
    editor_get_verification_issues,
    project_create_view, project_history, project_review, project_feedback, project_destroy, project_edit,
    project_application_show_view,
    questionnaire_response_index, questionnaire_response_show, questionnaire_response_approve, questionnaire_response_reject,
    matching_setting_index, matching_setting_store, matching_setting_update, matching_setting_destroy,
    chat_show,
    email_notification_index, email_notification_create, email_notification_store, email_notification_edit,
    email_notification_update, email_notification_destroy, email_notification_show
)


from .views import (
    test_supervisor, sendgrid_webhook
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
    path('data/country', country_create, name='country_create'),
    path('data/state', state_create, name='state_create'),
    path('data/city', city_create, name='city_create'),
    path('data/location', location_create, name='location_create'),
    path('data/editor', editor_create, name='editor_create'),
    path('data/editor/invite', invite, name='invite'),
    path('settings', settings_index, name='settings_index'),
    path('settings/add', settings_store, name='settings_store'),
    path('settings/update', settings_update, name='settings_update'),
    path('settings/<id>/delete', settings_destroy, name='settings_destroy'),

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
    path('projecttypes/<username>', project_types_user_index, name='project_types_index_user'),
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
    path('auth/social', views.auth_social, name='auth_social'),
    path('auth/linkedin', views.auth_linkedin, name='auth_linkedin'),
    path('auth/chat', views.auth_chat, name='auth_chat'),
    path('auth/broadcasting', views.auth_broadcasting, name='auth_broadcasting'),
    
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
    path('editor', editor_index, name='editor_index'),
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
    path('customer/register', customer_register, name='customer_register'),
    path('customer/me', customer_get_by_user, name='customer_get_by_user'),
    path('customer/upgrade', customer_upgrade, name='customer_upgrade'),
    path('customer/subscription-link', customer_generate_subscription_link, name='customer_generate_subscription_link'),
    path('customer/email-stop-webhook', customer_stop_email_webhook, name='customer_stop_email_webhook'),
    path('customer/stripe-expiry-update', customer_update_expiry_from_stripe, name='customer_update_expiry_from_stripe'),

    # Chat Endpoints
    path('chat', chat_index, name='chat_index'),
    path('chat/<uuid>', chat_get, name='chat_get'),
    path('chat/<uuid>/message', chat_message, name='chat_message'),
    path('chat/custom-message', chat_create_custom_message, name='chat_create_custom_message'),
    path('chat/init', chat_init, name='chat_init'),
    path('chat/init-public', chat_init_public, name='chat_init_public'),
    path('chat/received-messages', chat_get_received_messages, name='chat_get_received_messages'),
    path('chat/message/<id>/update', chat_update_message, name='chat_update_message'),

    # Favourite Endpoints
    path('favourite', favourite_index, name='favourite_index'),
    path('favourite/store', favourite_store, name='favourite_store'),

    # Profile Visit Endpoints
    path('profile-visit/store', profile_visit_store, name='profile_visit_store'),

    # Additional Matching Endpoints
    path('matching/project/<project_uuid>', matching_get_by_project_id, name='matching_get_by_project_id'),
    path('matching/public-create', matching_public_create, name='matching_public_create'),
    path('matching/token/<token>', matching_get_by_token, name='matching_get_by_token'),
    path('matching/create-from-favourites', matching_create_from_favorite_creators, name='matching_create_from_favorite_creators'),
    path('matching/admin/<id>/update', matching_admin_update, name='matching_admin_update'),

    # Admin Management Endpoints
    path('admin/editors', views.admin_list_editors, name='admin_list_editors'),
    path('admin/editors/<id>', views.admin_get_editor, name='admin_get_editor'),
    path('admin/creators', views.admin_list_creators, name='admin_list_creators'),
    path('admin/creators/<id>', views.admin_get_creator, name='admin_get_creator'),
    path('admin/projects', views.admin_list_projects, name='admin_list_projects'),
    path('admin/projects/<id>', views.admin_get_project, name='admin_get_project'),
    path('admin/delete-account/<email>', views.admin_delete_account, name='admin_delete_account'),
    path('admin/email-user', views.admin_email_user, name='admin_email_user'),

    # File Management Endpoints
    path('file/store', views.file_store, name='file_store'),
    path('file/upload', views.file_upload, name='file_upload'),
    path('file/upload-multiple', views.file_upload_multiple, name='file_upload_multiple'),
    path('file/signed-url/<filename>', views.file_get_signed_url, name='file_get_signed_url'),
    path('file/serve/<id>', views.file_serve, name='file_serve'),
    path('file/download/<id>', views.file_download, name='file_download'),

    # --- Taxonomy CRUD Endpoints ---

    path('skill/add', skill_store, name='skill_store'),
    path('skill/update', skill_update, name='skill_update'),
    path('skill/delete/<int:id>', skill_destroy, name='skill_destroy'),
    path('skill/<int:id>', skill_show, name='skill_show'),

    path('job-type/add', job_types_store, name='job_types_store'),
    path('job-type/update', job_types_update, name='job_types_update'),
    path('job-type/delete/<int:id>', job_types_destroy, name='job_types_destroy'),
    path('job-type/<int:id>', job_types_show, name='job_types_show'),

    path('equipment/add', equipment_store, name='equipment_store'),
    path('equipment/update', equipment_update, name='equipment_update'),
    path('equipment/delete/<int:id>', equipment_destroy, name='equipment_destroy'),
    path('equipment/<int:id>', equipment_show, name='equipment_show'),

    path('software/add', software_store, name='software_store'),
    path('software/update', software_update, name='software_update'),
    path('software/delete/<int:id>', software_destroy, name='software_destroy'),
    path('software/<int:id>', software_show, name='software_show'),

    path('platform/add', platform_store, name='platform_store'),
    path('platform/update', platform_update, name='platform_update'),
    path('platform/delete/<int:id>', platform_destroy, name='platform_destroy'),
    path('platform/<int:id>', platform_show, name='platform_show'),

    path('content-vertical/add', content_vertical_store, name='content_vertical_store'),
    path('content-vertical/update', content_vertical_update, name='content_vertical_update'),
    path('content-vertical/delete/<int:id>', content_vertical_destroy, name='content_vertical_destroy'),
    path('content-vertical/<int:id>', content_vertical_show, name='content_vertical_show'),

    path('creative-style/add', creative_style_store, name='creative_style_store'),
    path('creative-style/update', creative_style_update, name='creative_style_update'),
    path('creative-style/delete/<int:id>', creative_style_destroy, name='creative_style_destroy'),
    path('creative-style/<int:id>', creative_style_show, name='creative_style_show'),

    path('content-form/add', content_form_store, name='content_form_store'),
    path('content-form/update', content_form_update, name='content_form_update'),
    path('content-form/delete/<int:id>', content_form_destroy, name='content_form_destroy'),
    path('content-form/<int:id>', content_form_show, name='content_form_show'),

    path('project-type/add', project_type_store, name='project_type_store'),
    path('project-type/update', project_type_update, name='project_type_update'),
    path('project-type/delete/<int:id>', project_type_destroy, name='project_type_destroy'),
    path('project-type/<int:id>', project_type_show, name='project_type_show'),

    path('reason/add', reason_store, name='reason_store'),
    path('reason/update', reason_update, name='reason_update'),
    path('reason/delete/<int:id>', reason_destroy, name='reason_destroy'),
    path('reason/<int:id>', reason_show, name='reason_show'),

    path('referral/add', referral_store, name='referral_store'),
    path('referral/update', referral_update, name='referral_update'),
    path('referral/delete/<int:id>', referral_destroy, name='referral_destroy'),
    path('referral/<int:id>', referral_show, name='referral_show'),


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


    # Editor Controller Detailed
    path('editor/list', editor_list, name='editor_list'),
    path('editor/add', editor_create, name='editor_create_form'),
    path('editor/store', editor_store, name='editor_store_new'),
    path('editor/delete/<int:id>', editor_destroy, name='editor_destroy_id'),
    path('editor/<int:id>', editor_show, name='editor_show_id'),
    path('editor/<int:id>/edit', editor_edit, name='editor_edit_id'),
    path('editor/<int:id>/patch', editor_update, name='editor_update_patch'),
    path('editor/<int:id>/verification', editor_verification, name='editor_verification'),
    path('editor/<int:id>/activation/<status>', editor_activation, name='editor_activation'),
    path('editor/<int:id>/invite', editor_invite, name='editor_invite'),
    path('editor/<int:id>/project', editor_project, name='editor_project'),
    path('editor/<int:id>/project/delete/<int:project>', editor_delete_project, name='editor_delete_project'),
    path('editor/<int:id>/creator', editor_creator, name='editor_creator'),
    path('editor/<int:id>/creator/delete/<int:creator>', editor_delete_creator, name='editor_delete_creator'),
    path('editor/<uuid>/verification/send-email', editor_send_verification_email, name='editor_send_verification_email'),
    path('editor/verification/<uuid>/note', editor_update_verification_note, name='editor_update_verification_note'),
    path('editor/verification/<uuid>/approve', editor_approve_verification, name='editor_approve_verification'),
    path('editor/verification/<uuid>/note/delete', editor_delete_verification_note, name='editor_delete_verification_note'),
    path('editor/<uuid>/verification-issues', editor_get_verification_issues, name='editor_get_verification_issues'),

    # Project Extensions
    path('project/add', project_create_view, name='project_add_form'),
    path('project/history/<int:id>', project_history, name='project_history_id'),
    path('project/review/<int:id>', project_review, name='project_review_id'),
    path('project/feedback/<int:id>', project_feedback, name='project_feedback_id'),
    path('project/delete/<int:id>', project_destroy, name='project_destroy_id'),
    path('project/<int:id>/edit', project_edit, name='project_edit_id'),

    # Project Application Extensions
    path('project-application/<int:id>', project_application_show_view, name='project_application_show_view'),

    # Questionnaire Responses
    path('questionnaire-response', questionnaire_response_index, name='questionnaire_response_index'),
    path('questionnaire-response/<int:id>', questionnaire_response_show, name='questionnaire_response_show'),
    path('questionnaire-response/approve/<int:id>', questionnaire_response_approve, name='questionnaire_response_approve'),
    path('questionnaire-response/reject/<int:id>', questionnaire_response_reject, name='questionnaire_response_reject'),

    # Matching Settings
    path('matching/setting', matching_setting_index, name='matching_setting_index'),
    path('matching/setting/add', matching_setting_store, name='matching_setting_store'),
    path('matching/setting/update', matching_setting_update, name='matching_setting_update'),
    path('matching/setting/delete/<int:id>', matching_setting_destroy, name='matching_setting_destroy'),

    # Chat Extensions
    path('chat/<int:id>', chat_show, name='chat_show_id'),

    # Email Notifications
    path('email-notification', email_notification_index, name='email_notification_index'),
    path('email-notification/add', email_notification_create, name='email_notification_create'),
    path('email-notification/store', email_notification_store, name='email_notification_store'),
    path('email-notification/<int:id>/edit', email_notification_edit, name='email_notification_edit'),
    path('email-notification/<int:id>', email_notification_update, name='email_notification_update'),
    path('email-notification/delete/<int:id>', email_notification_destroy, name='email_notification_destroy'),
    path('email-notification/show/<int:id>', email_notification_show, name='email_notification_show'),


    # Webhooks & Utilities
    path('test-supervisor', test_supervisor, name='test_supervisor'),
    path('webhooks/sendgrid', sendgrid_webhook, name='sendgrid_webhook'),

]
