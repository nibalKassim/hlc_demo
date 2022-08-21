# -*- coding: utf-8 -*-
# Inspired from OCA Operating Units

{
    'name': "TMICT - Business Unit",
    'summary': """
        Business Unit within a company.""",
    'description': "",
    'author': "Shahzad Ali",
    'website': "http://www.tmict.com",
    'category': 'TMICT',
    'version': '15.0.1.0.0',
    'depends': [
        'base'
    ],
    'external_dependencies' : {},
    'data': [
        'security/business_unit_security.xml',
        'security/ir.model.access.csv',
        'data/business_unit_data.xml',
        # 'wizard/business_unit_initialize_view.xml',
        'views/business_unit_view.xml',
        'views/res_users_view.xml',
        'views/report_templates.xml',
    ],
    'demo': [],
    'application':False,
    'installable': True,
    'auto_install': False,
    'uninstall_hook': '',
    'pre_init_hook': '',
    'post_init_hook': '',
    'active':True,
}
