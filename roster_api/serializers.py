from rest_framework import serializers
from .models import (
    Skills, ContentVerticals, Platforms, Software, Equipment, 
    CreativeStyles, JobTypes, Countries, States, Cities, Locations, Users,
    UserProjects, UserCreators, UserSkills, UserContentVerticals, UserPlatforms,
    UserPricing, ProjectTypes, UserLanguage, UserSocialProfile,
    UserJobTypePricing, UserJobTypes, UserEquipments, UserCreativeStyles,
    Roles, UserRoles, Customers, PaymentTypes, PaymentStatuses,
    ContentForms, Reasons, Referrals, Otps, PersonalAccessTokens,
    UserSocials, UserPayments, ContentTopics, UserSoftware, ProjectApplications,
    ProjectApplicationNotes, ProjectScreeningAnswers, ProjectScreeningQuestions,
    CustomScreeningQuestions, QuestionTypes, UserVerificationLinks,
    Projects, Matchings, MatchingEditors, MatchingSkills, MatchingPlatforms,
    MatchingSoftware, MatchingContentVerticals, MatchingCreativeStyles,
    MatchingJobTypes, Chats, ChatMessages, UserFavourites, ProfileVisits,
    Setting, Files, Permissions, Menus, ReferralCodes, UserTodos,
    ProjectMilestones, ProjectReferences, ProjectHistories,
    ProjectFeedbackUsers, ProjectFeedbackEditors, Transactions
)


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'uuid', 'name', 'email', 'account_type', 'active', 'created_at']

class AdminProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class ContentVerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentVerticals
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platforms
        fields = '__all__'

class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class CreativeStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreativeStyles
        fields = '__all__'

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTypes
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjects
        fields = '__all__'

class UserCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreators
        fields = '__all__'

class UserContentVerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContentVerticals
        fields = '__all__'

class UserPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlatforms
        fields = '__all__'

class UserPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPricing
        fields = '__all__'

class UserSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSoftware
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'

class UserLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguage
        fields = '__all__'

class UserSocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialProfile
        fields = '__all__'

class UserJobTypePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobTypePricing
        fields = '__all__'

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkills
        fields = '__all__'

class UserEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEquipments
        fields = '__all__'

class UserCreativeStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreativeStyles
        fields = '__all__'

class UserJobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobTypes
        fields = '__all__'

class ContentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentForms
        fields = '__all__'

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTypes
        fields = '__all__'

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reasons
        fields = '__all__'

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referrals
        fields = '__all__'

class UserSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocials
        fields = '__all__'

class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayments
        fields = '__all__'

class ContentTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTopics
        fields = '__all__'

class ProjectApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectApplications
        fields = '__all__'

class ProjectApplicationNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectApplicationNotes
        fields = '__all__'

class ProjectScreeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScreeningQuestions
        fields = '__all__'

class ProjectScreeningAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScreeningAnswers
        fields = '__all__'

class CustomScreeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomScreeningQuestions
        fields = '__all__'

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTypes
        fields = '__all__'

class UserVerificationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerificationLinks
        fields = '__all__'


class ProjectMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMilestones
        fields = '__all__'


class ProjectReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReferences
        fields = '__all__'


class ProjectHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectHistories
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    editor = serializers.SerializerMethodField()
    milestones = ProjectMilestoneSerializer(many=True, read_only=True)
    content_forms = ContentFormSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    previous_references = serializers.SerializerMethodField()
    inspiration_references = serializers.SerializerMethodField()
    history = ProjectHistorySerializer(many=True, read_only=True)
    budget_text = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.uuid,
            'photo': user.photo,
            'name': user.name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'fun_fact': user.fun_fact,
            'job_title': user.job_title,
        }

    def get_editor(self, obj):
        editor = obj.editor
        if not editor:
            return []
        return {
            'id': editor.uuid,
            'photo': editor.photo,
            'name': editor.name,
            'first_name': editor.first_name,
            'last_name': editor.last_name,
            'username': editor.username,
            'fun_fact': editor.fun_fact,
            'job_title': editor.job_title,
            'address': editor.address,
        }

    def get_previous_references(self, obj):
        return ProjectReferenceSerializer(obj.references.filter(type='previous'), many=True).data

    def get_inspiration_references(self, obj):
        return ProjectReferenceSerializer(obj.references.filter(type='inspiration'), many=True).data

    def get_budget_text(self, obj):
        if obj.budget:
            return f"${obj.budget:,.2f}"
        return None


class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matchings
        fields = '__all__'


class MatchingEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingEditors
        fields = '__all__'


class MatchingSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingSkills
        fields = '__all__'


class MatchingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingPlatforms
        fields = '__all__'


class MatchingSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingSoftware
        fields = '__all__'


class MatchingContentVerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingContentVerticals
        fields = '__all__'


class MatchingCreativeStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingCreativeStyles
        fields = '__all__'


class MatchingJobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingJobTypes
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = '__all__'


class UserFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavourites
        fields = '__all__'


class ProfileVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileVisits
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTypes
        fields = '__all__'


class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatuses
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'


class UserTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTodos
        fields = '__all__'


class ReferralCodeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'first_name', 'last_name', 'created_at', 'account_type', 'activated_at', 'username']


class ReferralCodeSerializer(serializers.ModelSerializer):
    user = ReferralCodeUserSerializer(read_only=True)
    referral_discount_amount = serializers.IntegerField(source='referrer.referral_discount_amount', read_only=True)
    referral_discount_type = serializers.CharField(source='referrer.referral_discount_type', read_only=True)
    referral_discount_interval = serializers.IntegerField(source='referrer.referral_discount_interval', read_only=True)
    discount_code = serializers.CharField(source='referrer.discount_code', read_only=True)
    referrer_id = serializers.CharField(source='referrer.uuid', read_only=True)

    class Meta:
        model = ReferralCodes
        fields = [
            'id', 'uuid', 'code', 'user', 'credit_for_referrer', 'credit_for_referred_user',
            'created_at', 'referrer_id', 'referral_discount_amount',
            'referral_discount_type', 'referral_discount_interval', 'discount_code'
        ]


class ProjectFeedbackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFeedbackUsers
        fields = '__all__'


class ProjectFeedbackEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFeedbackEditors
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
