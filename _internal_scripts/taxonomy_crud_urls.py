
    path('skill/add', skill_store, name='skill_store'),
    path('skill/update', skill_update, name='skill_update'),
    path('skill/delete/<int:id>', skill_destroy, name='skill_destroy'),
    path('skill/<int:id>', skill_show, name='skill_show'),

    path('job-type/add', job_types_store, name='job_types_store'),
    path('job-type/update', job_types_update, name='job_types_update'),
    path('job-type/delete/<int:id>', job_types_destroy, name='job_types_destroy'),
    path('job-type/<int:id>', job_types_show, name='job_types_show'),

    path('equipment/add', equipment_store, name='equipment_store'),
    path('equipment/update', equipment_update, name='equipment_update'),
    path('equipment/delete/<int:id>', equipment_destroy, name='equipment_destroy'),
    path('equipment/<int:id>', equipment_show, name='equipment_show'),

    path('software/add', software_store, name='software_store'),
    path('software/update', software_update, name='software_update'),
    path('software/delete/<int:id>', software_destroy, name='software_destroy'),
    path('software/<int:id>', software_show, name='software_show'),

    path('platform/add', platform_store, name='platform_store'),
    path('platform/update', platform_update, name='platform_update'),
    path('platform/delete/<int:id>', platform_destroy, name='platform_destroy'),
    path('platform/<int:id>', platform_show, name='platform_show'),

    path('content-vertical/add', content_vertical_store, name='content_vertical_store'),
    path('content-vertical/update', content_vertical_update, name='content_vertical_update'),
    path('content-vertical/delete/<int:id>', content_vertical_destroy, name='content_vertical_destroy'),
    path('content-vertical/<int:id>', content_vertical_show, name='content_vertical_show'),

    path('creative-style/add', creative_style_store, name='creative_style_store'),
    path('creative-style/update', creative_style_update, name='creative_style_update'),
    path('creative-style/delete/<int:id>', creative_style_destroy, name='creative_style_destroy'),
    path('creative-style/<int:id>', creative_style_show, name='creative_style_show'),

    path('content-form/add', content_form_store, name='content_form_store'),
    path('content-form/update', content_form_update, name='content_form_update'),
    path('content-form/delete/<int:id>', content_form_destroy, name='content_form_destroy'),
    path('content-form/<int:id>', content_form_show, name='content_form_show'),

    path('project-type/add', project_type_store, name='project_type_store'),
    path('project-type/update', project_type_update, name='project_type_update'),
    path('project-type/delete/<int:id>', project_type_destroy, name='project_type_destroy'),
    path('project-type/<int:id>', project_type_show, name='project_type_show'),

    path('reason/add', reason_store, name='reason_store'),
    path('reason/update', reason_update, name='reason_update'),
    path('reason/delete/<int:id>', reason_destroy, name='reason_destroy'),
    path('reason/<int:id>', reason_show, name='reason_show'),

    path('referral/add', referral_store, name='referral_store'),
    path('referral/update', referral_update, name='referral_update'),
    path('referral/delete/<int:id>', referral_destroy, name='referral_destroy'),
    path('referral/<int:id>', referral_show, name='referral_show'),
