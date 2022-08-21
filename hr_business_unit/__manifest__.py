# -*- coding: utf-8 -*-
# Inspired from OCA Operating Units

{
    'name': "TMICT - Sale Business Unit",
    'summary': """
        Sale Business Unit within a company.""",
    'description': "",
    'author': "Shahzad Ali",
    'website': "http://www.tmict.com",
    'category': 'TMICT',
    'version': '15.0.1.0.0',
    'depends': [
        'hr',
        'business_unit',
    ],
    'external_dependencies' : {},
    'data': [
        'security/sale_security.xml',
        # 'security/crm_team_security.xml',
        # 'views/crm_team_view.xml',
        'views/sale_views.xml',        
        'views/sale_report_view.xml',       
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
