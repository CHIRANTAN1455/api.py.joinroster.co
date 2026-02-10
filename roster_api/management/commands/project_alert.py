from django.core.management.base import BaseCommand
from django.utils import timezone
from roster_api.models import Projects, Users, EmailNotifications, EmailNotificationLogs
from roster_api.match_service import MatchService

class Command(BaseCommand):
    help = 'Send alerts for open projects to editors (Port of project:alert)'

    def handle(self, *args, **options):
        now = timezone.now()
        match_service = MatchService()
        
        # 1. Get Project Alert notification template
        try:
            alert_template = EmailNotifications.objects.get(code='project-alert', active=1)
        except EmailNotifications.DoesNotExist:
            self.stdout.write(self.style.ERROR("Notification template 'project-alert' not found."))
            return

        # 2. Get Open projects
        open_projects = Projects.objects.filter(status='open', published=1)
        self.stdout.write(f"Analyzing {open_projects.count()} open projects.")

        # 3. Get Active Editors
        editors = Users.objects.filter(account_type='editor', active=1)
        
        for project in open_projects:
            self.stdout.write(f"Checking matching editors for project: {project.title} (ID: {project.id})")
            
            for editor in editors:
                # 4. Check if already notified for THIS project
                already_notified = EmailNotificationLogs.objects.filter(
                    user=editor,
                    project_id=project.id,
                    email_notification=alert_template
                ).exists()
                
                if already_notified:
                    continue
                
                # 5. Calculate Match
                match_data = match_service.calculate_match(editor, project)
                score = match_data['total_match_score']
                
                # Threshold from Laravel is often >= 40% or 50%
                if score >= 50:
                    self.stdout.write(self.style.SUCCESS(
                        f"MATCH! Editor {editor.email} matches Project {project.id} with {score}%"
                    ))
                    
                    # 6. Send Email (Placeholder)
                    # send_project_alert_email(editor, project, score)
                    
                    # 7. Log Notification
                    EmailNotificationLogs.objects.create(
                        user=editor,
                        project_id=project.id,
                        email_notification=alert_template,
                        created_at=now,
                        updated_at=now
                    )
                    
                    self.stdout.write(f"Logged alert for {editor.email}")

        self.stdout.write(self.style.SUCCESS("Project alerts processing complete."))
