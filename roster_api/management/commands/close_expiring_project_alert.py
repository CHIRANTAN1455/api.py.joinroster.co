from django.core.management.base import BaseCommand
from roster_api.models import (
    Users, Projects, EmailNotifications, EmailNotificationLogs, Customers
)
from django.utils import timezone
from django.db.models import Q
import logging
from datetime import timedelta
import uuid

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Close expiring job'

    def handle(self, *args, **options):
        now = timezone.now()
        start_date = timezone.make_aware(datetime(2025, 5, 25))

        # Fetch projects
        projects = Projects.objects.filter(
            status='open',
            deleted_at__isnull=True,
            created_at__gte=start_date
        ).exclude(hackathon=1).filter(user__account_type='user')

        for project in projects:
            expiry_date = project.created_at + timedelta(days=30) # addMonth approx
            # Diff in days
            # PHP: $expiry_date->diffInDays($now, false). If expiry > now (future), diff is negative?
            # PHP diffInDays(date, absolute=true by default). false means signed.
            # $expiry->diffInDays($now, false) means ($now - $expiry) in days.
            # If Expiry is Future, Now - Expiry is Negative.
            # Example: Expiry in 7 days. Now - Expiry = -7.
            
            diff = (now - expiry_date).days
            # Python timedelta days property is slightly different, it floors.
            # Let's use total_seconds
            diff_days = (now - expiry_date).total_seconds() / (24 * 3600)
            
            # Use integer days for comparison to match PHP rough logic
            days_until_expiry = int(diff_days)

            self.stdout.write(f'Days until expired: {days_until_expiry}')
            user = project.user

            if -7 <= days_until_expiry <= -3:
                # 7 days before
                self.send_notification(user, project, 'd7', abs(days_until_expiry), f'Expiring Job 1 Week Before-Project_{project.uuid}')
            
            elif -1 <= days_until_expiry < 0:
                # 1 day before
                self.send_notification(user, project, 'd1', None, f'Expiring Job 1 Day Before-Project_{project.uuid}')
            
            elif days_until_expiry == 0: # This might be tricky with float logic, using int(diff_days) might result in 0 for range (-1, 1). 
                # PHP diffInDays strips time components usually or uses threshold.
                # If now > expiry (positive).
                # Let's assume 0 means "today".
                self.send_notification(user, project, 'd0', None, f'Expiring Job Same Day-Project_{project.uuid}')

            elif days_until_expiry >= 1:
                # Expire the job
                project.status = 'closed'
                project.to_send_rejection_email = 1
                project.sent_rejection_email = 0
                project.closed_at = now
                project.updated_at = now
                project.save()

                # Downgrade customer
                try:
                    customer = Customers.objects.filter(user=user).first()
                    if customer:
                        if customer.expired_at is None:
                            logger.error(f"expired_at is NULL for customer ID {customer.id}")
                            # Send alert email logic here
                        elif customer.payment_type_id == 2 or (customer.payment_type_id > 2 and customer.expired_at < now):
                            customer.payment_type_id = 1
                            customer.payment_status_id = 1
                            customer.save()
                except Exception as e:
                    logger.error(f"Error updating customer: {e}")

                # Notification
                self.send_notification(user, project, 'd+1', None, f'Expired Job-Project_{project.uuid}')

    def send_notification(self, user, project, type_code, days_count, name_prefix):
        code_suffix = f"-project_{project.uuid}"
        full_code = f"expiring_job_{type_code}{code_suffix}"
        
        notification = EmailNotifications.objects.filter(code=full_code).first()
        if not notification:
            notification = EmailNotifications.objects.create(
                uuid=str(uuid.uuid4()),
                name=name_prefix,
                code=full_code,
                active=1,
                tags=['notification'],
                subject=name_prefix,
                content='</>',
                created_at=timezone.now()
            )

        log = EmailNotificationLogs.objects.filter(
            user=user,
            email_notification=notification
        ).first()

        if not log:
            # Send Email (Placeholder)
            self.stdout.write(f"Emailing: {user.email} for {type_code}")
            
            EmailNotificationLogs.objects.create(
                email_notification=notification,
                user=user,
                created_at=timezone.now()
            )
