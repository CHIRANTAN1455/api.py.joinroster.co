import re

views_addition = """
# --- Webhooks & Utilities ---

@api_view(['GET'])
def test_supervisor(request):
    return ApiResponse(message="Supervisor is running!")

@api_view(['POST'])
def sendgrid_webhook(request):
    # Depending on payload, we might process bouncing, drops, etc.
    data = request.data
    # For now, just accept
    return ApiResponse(message="Sendgrid webhook received")
"""

with open('roster_api/views.py', 'r') as f:
    views_content = f.read()

if 'test_supervisor(request):' not in views_content:
    views_content += views_addition
    with open('roster_api/views.py', 'w') as f:
        f.write(views_content)

with open('roster_api/urls.py', 'r') as f:
    urls_content = f.read()

imports_to_add = """
from .views import (
    test_supervisor, sendgrid_webhook
)
"""

urls_addition_block = """
    # Webhooks & Utilities
    path('test-supervisor', test_supervisor, name='test_supervisor'),
    path('webhooks/sendgrid', sendgrid_webhook, name='sendgrid_webhook'),
"""

if 'test_supervisor' not in urls_content:
    urls_content = urls_content.replace('from . import views # Keep this for views.test_api', imports_to_add + '\nfrom . import views # Keep this for views.test_api')
    urls_content = re.sub(r'\]\n*$', urls_addition_block + "\n]\n", urls_content)

    with open('roster_api/urls.py', 'w') as f:
        f.write(urls_content)

print("Added Webhooks & Utilities")
