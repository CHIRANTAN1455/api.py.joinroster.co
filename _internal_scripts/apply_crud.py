import re

with open('taxonomy_crud_views.py', 'r') as f:
    views_addition = f.read()

# Replace uuid_lib with just uuid as we might need to import it properly
views_addition = views_addition.replace('uuid_lib.uuid4()', 'uuid.uuid4()')

with open('roster_api/views.py', 'r') as f:
    views_content = f.read()

if 'import uuid' not in views_content:
    views_content = views_content.replace('import secrets', 'import secrets\nimport uuid\n')
else:
    # Ensure uuid is actually imported, uncomment it if needed
    views_content = views_content.replace('import uuid as uuid_lib # Removed', 'import uuid')

views_content += "\n# --- Taxonomy CRUD Endpoints ---\n" + views_addition

with open('roster_api/views.py', 'w') as f:
    f.write(views_content)

with open('taxonomy_crud_urls.py', 'r') as f:
    urls_addition = f.read()

with open('roster_api/urls.py', 'r') as f:
    urls_content = f.read()

# Add imports to urls.py
imports_to_add = """
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
"""
urls_content = urls_content.replace('from . import views # Keep this for views.test_api', imports_to_add + '\nfrom . import views # Keep this for views.test_api')

urls_addition_block = "\n    # --- Taxonomy CRUD Endpoints ---\n" + urls_addition + "\n]\n"
urls_content = re.sub(r'\]\n*$', urls_addition_block, urls_content)

with open('roster_api/urls.py', 'w') as f:
    f.write(urls_content)

print("Appended views and urls successfully.")
