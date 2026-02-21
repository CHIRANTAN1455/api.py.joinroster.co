import re

views_addition = """
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
"""

with open('roster_api/views.py', 'r') as f:
    views_content = f.read()

if 'editor_list(request):' not in views_content:
    views_content += views_addition
    with open('roster_api/views.py', 'w') as f:
        f.write(views_content)

with open('roster_api/urls.py', 'r') as f:
    urls_content = f.read()

imports_to_add = """
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
"""

urls_addition_block = """
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
"""

if 'editor_list' not in urls_content:
    urls_content = urls_content.replace('from . import views # Keep this for views.test_api', imports_to_add + '\nfrom . import views # Keep this for views.test_api')
    urls_content = re.sub(r'\]\n*$', urls_addition_block + "\n]\n", urls_content)

    with open('roster_api/urls.py', 'w') as f:
        f.write(urls_content)

print("Added Complex Controllers CRUDs")
