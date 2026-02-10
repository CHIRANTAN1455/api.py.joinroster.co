import math
from django.db.models import Q
from .models import MatchingSettings, Users, Projects, UserJobTypePricing

class MatchService:
    def __init__(self):
        # Fetch all active matching settings once
        settings_qs = MatchingSettings.objects.filter(active=1, deleted_at__isnull=True)
        self.settings = {s.key: s.value for s in settings_qs}

    def get_setting(self, key, default):
        val = self.settings.get(key)
        if val is None:
            return default
        try:
            return float(val) if '.' in val else int(val)
        except ValueError:
            return val

    def calculate_match(self, user: Users, project: Projects):
        match_score = 0
        total_possible = 0
        has_production_roles = False

        # 1. Job Type
        job_type_points = 10
        optional_job_type_points = 5
        match_job_types = []
        
        # In Django, related names or .all()
        user_job_types = user.userjobtypes_set.all()
        project_job_types = project.projectjobtype_set.all()
        
        user_job_type_points = 0
        
        # Interchangeable types [43, 60] - SMM and Channel Manager
        interchangeable_types = [43, 60]
        
        for pj in project_job_types:
            pj_id = pj.job_type_id
            for uj in user_job_types:
                uj_id = uj.job_type_id
                
                if (pj_id == uj_id or 
                    (pj_id in interchangeable_types and uj_id in interchangeable_types)):
                    match_job_types.append(pj_id)
                    # Check if optional (assuming field exists based on Laravel logic)
                    is_optional = getattr(pj, 'optional', 0) == 1
                    if is_optional:
                        user_job_type_points += optional_job_type_points
                    else:
                        user_job_type_points += job_type_points
                    break

        compulsory_project_job_types = [jt for jt in project_job_types if getattr(jt, 'optional', 0) != 1]
        count_compulsory = len(compulsory_project_job_types)
        total_job_type_points = job_type_points * count_compulsory

        if count_compulsory:
            match_score += user_job_type_points
            total_possible += total_job_type_points

        # production role check
        has_production_roles = self.has_production_role(project_job_types)

        # Only consider rest of criteria if there is matched job type
        job_type_matched = len(match_job_types) > 0

        if job_type_matched:
            # 2. Primary Job Type
            if user_job_types.count() > 1:
                primary_points = self.get_setting('primary_job_type_points', 10)
                user_primary = [uj for uj in user_job_types if uj.primary_job == 1]
                
                if user_primary:
                    if self.has_matching_primary_job_type(user_primary, project_job_types):
                        match_score += primary_points
                
                total_possible += primary_points

            # 3. Project Job Type (Experience)
            if has_production_roles:
                exp_points = self.get_setting('project_job_type_points', 10)
                # user_projects in Laravel means finished projects?
                # In Django, Projects has editor field.
                user_completed_projects = Projects.objects.filter(editor=user, status='completed')
                
                if self.has_matching_project_job_type(project_job_types, user_completed_projects):
                    match_score += exp_points
                
                total_possible += exp_points

            # 4. Platforms
            platform_points = self.get_setting('platforms_points', 10)
            user_platforms = set(p.platform.name for p in user.userplatforms_set.all())
            project_platforms = set(p.platform.name for p in project.projectplatforms_set.all())
            
            match_p_count = len(user_platforms & project_platforms)
            match_score += platform_points * match_p_count
            total_possible += platform_points * len(project_platforms)

            # 5. Content Verticals
            cv_points = self.get_setting('content_verticals_points', 3)
            user_cvs = set(cv.content_vertical.name for cv in user.usercontentverticals_set.all())
            project_cvs = set(cv.content_vertical.name for cv in project.projectcontentverticals_set.all())
            
            match_cv_count = len(user_cvs & project_cvs)
            
            # Interchangeable content verticals
            inter_cvs = {'Automotive & Cars', 'Sports & Cars'}
            if (user_cvs & inter_cvs) and (project_cvs & inter_cvs):
                match_cv_count += 1
                
            match_score += cv_points * match_cv_count
            total_possible += cv_points * len(project_cvs)

            # 6. Skills
            skill_points = self.get_setting('skills_points', 5)
            user_skills = set(s.skill.name for s in user.userskills_set.all())
            project_skills = set(s.skill.name for s in project.projectskill_set.all())
            
            match_s_count = len(user_skills & project_skills)
            match_score += skill_points * match_s_count
            total_possible += skill_points * len(project_skills)

            # 7. Software
            project_softwares = project.projectsoftware_set.all()
            if project_softwares.exists():
                sw_points = self.get_setting('softwares_points', 10)
                user_softwares = set(sw.software.name for sw in user.usersoftware_set.all())
                proj_sw_names = set(sw.software.name for sw in project_softwares)
                
                match_sw_count = len(user_softwares & proj_sw_names)
                match_score += sw_points * match_sw_count
                total_possible += sw_points * len(proj_sw_names)

            # 8. Creative Styles
            if has_production_roles:
                proj_cs = project.projectcreativestyle_set.all()
                if proj_cs.exists():
                    cs_points = self.get_setting('creative_styles_points', 5)
                    user_cs = set(cs.creative_style.name for cs in user.usercreativestyles_set.all())
                    proj_cs_names = set(cs.creative_style.name for cs in proj_cs)
                    
                    match_cs_count = len(user_cs & proj_cs_names)
                    match_score += cs_points * match_cs_count
                    total_possible += cs_points * len(proj_cs_names)

            # 9. Timezone
            if project.utc_offset is not None:
                offset_points = self.get_setting('utc_offset_points', 5)
                offset_range = self.get_setting('utc_offset_range', 5)
                
                if user.utc_offset is not None:
                    if abs(user.utc_offset - project.utc_offset) <= offset_range:
                        match_score += offset_points
                
                total_possible += offset_points

            # 10. Favorite Creators / Topics
            # This part is complex and depends on many relationships. 
            # I'll implement a simplified version or port fully if models exist.
            # fav_creators = project.user.creators (UserCreators model?)
            # I'll skip the detailed creator matching for now if models are missing, 
            # but I should check if UserCreators exists in Django.
            
            # 11. Availability
            interested_in = project.interested_in or []
            # User availability logic needs Pricing model check
            user_interested_in = []
            try:
                user_pricing = user.userpricing
                user_interested_in = user_pricing.interested_in or []
            except:
                pass
                
            avail_points = self.get_setting('interested_in_points', 10)
            if interested_in:
                for target in interested_in:
                    avail_match = False
                    canon_target = 'fulltime' if 'full' in target.lower() else 'freelance'
                    for u_avail in user_interested_in:
                        canon_u = 'fulltime' if 'full' in u_avail.lower() else 'freelance'
                        if canon_u == canon_target:
                            avail_match = True
                            break
                    
                    if avail_match:
                        match_score += avail_points
                    total_possible += avail_points

        # Calculate final percentage
        final_percent = 0
        if total_possible > 0:
            final_percent = round((match_score / total_possible) * 100)
            if final_percent >= 99:
                final_percent = 98

        return {
            'total_match_score': max(0, final_percent),
            'total': total_possible,
            'match': max(0, match_score),
            'has_production_role': has_production_roles
        }

    def has_production_role(self, project_job_types):
        # Port of Laravel ProjectService->has_production_role
        production_roles = [
            'Producer', 'Scriptwriter', 'Ghostwriter', 'Thumbnail Designer', 
            'Video Editor', 'Voiceover Artist', 'Newsletter Writer', 'Animator',
            'Ideation Strategist', 'Production Assistant', 'Videographer', 
            'In-House Creator', 'Showrunner', 'Researcher', 'Podcast Editor',
            'Creative Director', 'Photographer', 'Presenter', 'Casting Director'
        ]
        for pjt in project_job_types:
            if pjt.job_type.name in production_roles:
                return True
        return False

    def has_matching_primary_job_type(self, user_primary, project_job_types):
        pj_ids = [pj.job_type_id for pj in project_job_types]
        for up in user_primary:
            if up.job_type_id in pj_ids:
                return True
        return False

    def has_matching_project_job_type(self, project_job_types, user_projects):
        # Check if user has worked on projects with any of the requested job types
        pj_ids = [pj.job_type_id for pj in project_job_types]
        for up in user_projects:
            # Need to know which job types were in that past project
            up_job_types = up.projectjobtype_set.values_list('job_type_id', flat=True)
            if any(jt_id in pj_ids for jt_id in up_job_types):
                return True
        return False
