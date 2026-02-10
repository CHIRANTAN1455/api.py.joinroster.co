from django.core.management.base import BaseCommand
from django.utils import timezone
from roster_api.models import Customers, PaymentStatuses

class Command(BaseCommand):
    help = 'Update expired customers (Port of customers:update-expired)'

    def handle(self, *args, **options):
        now = timezone.now()
        
        try:
            free_status = PaymentStatuses.objects.get(name='free', active=1)
        except PaymentStatuses.DoesNotExist:
            self.stdout.write(self.style.ERROR("Free status 'free' not found in payment_statuses."))
            return

        # Fetch recurring and one-time customers whose expired_at has passed
        expired_customers = Customers.objects.filter(
            expired_at__lte=now
        ).exclude(payment_status=free_status)
        
        count = expired_customers.count()
        self.stdout.write(f"Found {count} expired customers.")
        
        for customer in expired_customers:
            try:
                old_status = customer.payment_status.name
                customer.payment_status = free_status
                customer.updated_at = now
                customer.save()
                
                msg = f"Customer {customer.user.email} (ID: {customer.id}) downgraded from {old_status} to free."
                self.stdout.write(self.style.SUCCESS(msg))
                
                # Note: Laravel sends Slack alerts here. 
                # We can implement a Slack utility later if needed.
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error updating customer {customer.id}: {str(e)}"))
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} customers."))
        else:
            self.stdout.write("No customers to process.")
