from roster_api.models import EmailNotifications, EmailNotificationLogs, Users, Settings
from django.utils import timezone
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def profile_missing_fields_day1():
    return {
        'photo': {
            'title': 'Missing photo',
            'description': 'Upload a HD photo of yourself so creators can see who they\'re getting in touch with.',
            'slug': 'bio'
        },
        'job_types': {
            'title': 'Missing job types',
            'description': 'Select roles that you are most experienced with.',
            'slug': 'job_types'
        },
        'creators': {
            'title': 'Missing experience',
            'description': 'What brands or creators have you worked with? This is one of the most important sections every creator looks at.',
            'slug': 'creators'
        },
        'projects': {
            'title': 'Missing projects',
            'description': "Include at least 1 project you've worked on for each creator or brand you mentioned to showcase your experience.",
            'slug': 'creators'
        },
        'skills': {
            'title': 'Missing skills',
            'description': 'List relevant skills to your job types and showcase your expertise.',
            'slug': 'skills'
        },
        'platforms': {
            'title': 'Missing platforms',
            'description': 'What social media platforms do you specialize in?',
            'slug': 'platforms'
        },
        'content_verticals': {
            'title': 'Missing content verticals',
            'description': 'What content niches do you specialize in?',
            'slug': 'content-verticals'
        },
        'pricing': {
            'title': 'Missing rates',
            'description': 'Provide your rates to help creators understand how they can best work with you.',
            'slug': 'project-and-pricing'
        },
        'availability': {
            'title': 'Missing availability',
            'description': 'Are you looking for full-time or freelance opportunities?',
            'slug': 'project-and-pricing'
        }
    }

def profile_missing_fields_day3():
    return {
        'photo': {
            'title': 'Add a photo',
            'description': 'Got a cool photo of yourself you can upload? Creators want to know who they\'re chatting with.',
            'slug': 'bio'
        },
        'job_types': {
            'title': 'Add job types',
            'description': 'Select roles that you are offering service for',
            'slug': 'job_types'
        },
        'creators': {
            'title': 'Add what creators or companies you\'ve worked with',
            'description': 'Yes, this is the place to name drop!',
            'slug': 'creators'
        },
        'projects': {
            'title': 'Add a project',
            'description': 'You can showcase a video or project that you’ve worked on during your time at the company here! The visuals help creators grasp your creative style.',
            'slug': 'creators'
        },
        'skills': {
            'title': 'Add skills',
            'description': 'List relevant skills to your job types and showcase your expertise.',
            'slug': 'skills'
        },
        'platforms': {
            'title': 'Add platforms',
            'description': 'What social media platforms do you specialize in?',
            'slug': 'platforms'
        },
        'content_verticals': {
            'title': 'Missing content verticals',
            'description': 'Stand out by sharing your expertise! What content niches do you like to work on?',
            'slug': 'content-verticals'
        },
        'pricing': {
            'title': 'Add your rates',
            'description': 'You should be compensated for your work! Help creators understand your rates by adding them to your profile.',
            'slug': 'project-and-pricing'
        },
        'availability': {
            'title': 'Add your availability',
            'description': 'Indicate whether your\'e open to full-time or freelance opportunities here.',
            'slug': 'project-and-pricing'
        }
    }

def profile_missing_fields_day7():
    return {
        'photo': {
            'title': 'Upload a pic',
            'description': 'Every user is required to have a profile photo!',
            'slug': 'bio'
        },
        'job_types': {
            'title': 'Add job types',
            'description': 'Select roles that you are you are most experienced with.',
            'slug': 'job_types'
        },
        'creators': {
            'title': 'Past creators or clients',
            'description': 'This is going to catch a creator\'s eye right off the bat.',
            'slug': 'creators'
        },
        'projects': {
            'title': 'Add at least 1 past project for each creator',
            'description': 'This is one of the most important sections creators look at!',
            'slug': 'creators'
        },
        'skills': {
            'title': 'Add skills',
            'description': 'List relevant skills to your job types and showcase your expertise.',
            'slug': 'skills'
        },
        'platforms': {
            'title': 'Add platforms',
            'description': 'What social media platforms do you specialize in?',
            'slug': 'platforms'
        },
        'content_verticals': {
            'title': 'Missing content verticals',
            'description': 'What type of content or industry do you want to specialize in? List them to help creators find you.',
            'slug': 'content-verticals'
        },
        'pricing': {
            'title': 'Add your rates for each job type',
            'description': 'Help creators understand your pricing — add your rates for all the job types you specialize in.',
            'slug': 'project-and-pricing'
        },
        'availability': {
            'title': 'Add your availability',
            'description': 'Are you looking for full-time or freelance opportunities, or both?',
            'slug': 'project-and-pricing'
        },
    }

class ProfileHelper:
    def calculate_profile_completion(self, user):
        missing_fields = []
        production_roles = [
            'Producer', 'Scriptwriter', 'Ghostwriter', 'Thumbnail Designer', 
            'Video Editor', 'Voiceover Artist', 'Newsletter Writer', 'Animator',
            'Ideation Strategist', 'Production Assistant', 'Videographer', 
            'In-House Creator', 'Showrunner', 'Researcher', 'Podcast Editor',
            'Creative Director', 'Photographer', 'Presenter', 'Casting Director',
            'Localization & Distribution'
        ]

        has_production_role = False
        user_job_types = user.userjobtypes_set.all()
        for uj in user_job_types:
            if uj.job_type.name in production_roles:
                has_production_role = True
                break

        total_fields_production = 9
        total_fields_non_production = 8
        completed_fields = 0

        # Check photo
        if user.photo and '/avatar.jpg' not in user.photo:
            completed_fields += 1
        else:
            missing_fields.append('photo')

        # Check job types
        if user_job_types.exists():
            completed_fields += 1
        else:
            missing_fields.append('job_types')

        # Check creators
        user_creators = user.usercreators_set.all()
        if user_creators.exists():
            completed_fields += 1
        else:
            missing_fields.append('creators')

        # Check projects for production roles
        if has_production_role:
            # Check if user has at least 1 project per creator?
            # Laravel: $user->has_min_1_project_per_creator()
            # Assuming simplified logic: check if user has projects
            if user.projects_set.filter(status='completed').exists(): # approximation
                completed_fields += 1
            else:
                missing_fields.append('projects')

        # Check skills
        if user.userskills_set.exists():
            completed_fields += 1
        else:
            missing_fields.append('skills')

        # Check platforms
        if user.userplatforms_set.exists():
            completed_fields += 1
        else:
            missing_fields.append('platforms')

        # Check content verticals
        if user.usercontentverticals_set.exists():
            completed_fields += 1
        else:
            missing_fields.append('content_verticals')

        # Pricing and Availability
        # UserPricing is OneToOne usually?
        try:
            user_pricing = user.userpricing
            # Check job type pricings
            job_type_pricing_complete = True
            ujtp = user.userjobtypepricing_set.all()
            if ujtp.exists():
                for pricing in ujtp:
                    if not pricing.starting_price:
                        job_type_pricing_complete = False
                        break
            else:
                job_type_pricing_complete = False  # Or true if no job types? But we checked job types above
            
            if job_type_pricing_complete:
                completed_fields += 1
            else:
                missing_fields.append('pricing')

            # Check availability (interested_in)
            if user_pricing.interested_in and len(user_pricing.interested_in) > 0:
                completed_fields += 1
            else:
                missing_fields.append('availability')

        except Exception:
            missing_fields.append('pricing')
            missing_fields.append('availability')

        total_fields = total_fields_production if has_production_role else total_fields_non_production
        
        completion_percentage = round((completed_fields / total_fields) * 100)
        
        return {
            'complete_percent': completion_percentage,
            'missing_fields': missing_fields
        }

    def trigger_base_alert(self, user, missing_fields, send_email_callback):
        setting = Settings.objects.filter(key='web_app_url').first()
        base_url = setting.value if setting else 'https://app.joinroster.co'
        url = f"{base_url}/things-to-do?page=profile"

        d1_fields = profile_missing_fields_day1()
        d3_fields = profile_missing_fields_day3()
        d7_fields = profile_missing_fields_day7()

        # D1
        notif_d1 = EmailNotifications.objects.filter(code='incomplete-profile-d1').first()
        if not notif_d1:
            return # Should probably log error or create one
            
        first_notif_log = EmailNotificationLogs.objects.filter(
            user=user, 
            email_notification=notif_d1
        ).first()

        now = timezone.now()

        if not first_notif_log:
            mapped_fields = [d1_fields.get(f) for f in missing_fields if f in d1_fields]
            subject = f"{user.first_name}, 8 creators tried to view your profile but…" if user.first_name else '8 creators tried to view your profile but…'
            preview = 'Getting your profile shortlisted by creators'
            
            send_email_callback(user, url, 'incomplete-profile-d1', mapped_fields, subject, preview)
            
            EmailNotificationLogs.objects.create(
                email_notification=notif_d1,
                user=user,
                created_at=now
            )
        else:
            # Check D3
            days_since_d1 = (now - first_notif_log.created_at).days
            if days_since_d1 >= 2:
                notif_d3 = EmailNotifications.objects.filter(code='incomplete-profile-d3').first()
                second_notif_log = EmailNotificationLogs.objects.filter(
                    user=user,
                    email_notification=notif_d3
                ).first()

                if not second_notif_log:
                    mapped_fields = [d3_fields.get(f) for f in missing_fields if f in d3_fields]
                    subject = f"{user.first_name}, your profile is not visible to 230 creators." if user.first_name else 'Your profile is not visible to 230 creators.'
                    preview = 'Getting your profile shortlisted by creators [Action required]'

                    send_email_callback(user, url, 'incomplete-profile-d3', mapped_fields, subject, preview)

                    EmailNotificationLogs.objects.create(
                        email_notification=notif_d3,
                        user=user,
                        created_at=now
                    )
                else:
                    # Check D7
                    days_since_d3 = (now - second_notif_log.created_at).days
                    if days_since_d3 >= 4:
                        notif_d7 = EmailNotifications.objects.filter(code='incomplete-profile-d7').first()
                        third_notif_log = EmailNotificationLogs.objects.filter(
                            user=user,
                            email_notification=notif_d7
                        ).first()

                        if not third_notif_log:
                            mapped_fields = [d7_fields.get(f) for f in missing_fields if f in d7_fields]
                            subject = 'Complete your profile to get hired by top creators'
                            preview = 'Strengthen your profile to be discovered and ranked higher'

                            send_email_callback(user, url, 'incomplete-profile-d7', mapped_fields, subject, preview)

                            EmailNotificationLogs.objects.create(
                                email_notification=notif_d7,
                                user=user,
                                created_at=now
                            )
