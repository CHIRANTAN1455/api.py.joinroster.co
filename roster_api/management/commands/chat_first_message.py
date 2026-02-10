from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from roster_api.models import ChatMessages, Users, EmailNotifications, EmailNotificationLogs

class Command(BaseCommand):
    help = 'Send reminder for unreplied first messages (Port of chat:first-message)'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int)

    def handle(self, *args, **options):
        days = options['days']
        now = timezone.now()
        target_date = now - timedelta(days=days)
        
        # We look for messages sent roughly 'days' ago.
        # To be precise, we can look for messages sent between (days) and (days-1) ago if run daily, 
        # or just check if they are older than 'days' and haven't been notified yet.
        
        # 1. Get template
        try:
            template = EmailNotifications.objects.get(code='chat-reminder', active=1)
        except EmailNotifications.DoesNotExist:
            self.stdout.write(self.style.ERROR("Template 'chat-reminder' not found."))
            return

        # 2. Find messages sent around target_date (e.g., within a 1-hour window to avoid duplicates if run hourly)
        # Or better: find messages >= days old, unreplied, and no notification log yet.
        
        potential_messages = ChatMessages.objects.filter(
            created_at__lte=target_date,
            is_read=0 # Usually unread implies unreplied too, but let's check properly
        ).order_by('created_at')

        processed_chats = set()

        for msg in potential_messages:
            if msg.chat_id in processed_chats:
                continue
            
            # 3. Verify it's the first message
            is_first = not ChatMessages.objects.filter(
                chat=msg.chat, 
                created_at__lt=msg.created_at
            ).exists()
            
            if is_first:
                # 4. Check for ANY reply from recipient
                has_reply = ChatMessages.objects.filter(
                    chat=msg.chat,
                    user_id=msg.recipient_id, # Recipient of first message replied?
                    created_at__gt=msg.created_at
                ).exists()
                
                if not has_reply:
                    # 5. Check notification log to avoid multiple reminders for same msg
                    # We can use project_id=msg.id or similar if using project_id field as generic ID
                    # or just rely on the fact that we only remind once.
                    recipient = Users.objects.filter(id=msg.recipient_id).first()
                    if not recipient:
                        continue
                        
                    already_notified = EmailNotificationLogs.objects.filter(
                        user=recipient,
                        email_notification=template,
                        # We use created_at comparison or a custom identifier if available
                    ).filter(created_at__gt=msg.created_at).exists()
                    
                    if not already_notified:
                        self.stdout.write(self.style.SUCCESS(
                            f"REPLY REMINDER: Chat {msg.chat.id}, Recipient: {recipient.email}, Days: {days}"
                        ))
                        
                        # 6. Log notification
                        EmailNotificationLogs.objects.create(
                            user=recipient,
                            email_notification=template,
                            created_at=now,
                            updated_at=now
                        )
            
            processed_chats.add(msg.chat_id)

        self.stdout.write(self.style.SUCCESS(f"Finished processing chat reminders for {days} days."))
