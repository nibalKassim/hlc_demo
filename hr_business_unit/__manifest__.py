# -*- coding: utf-8 -*-
# Inspired from OCA Operating Units

{
    'name': "TMICT - HR Business Unit",
    'summary': """
        HR Business Unit within a company.""",
    'description': "",
    'author': "Shahzad Ali",
    'website': "http://www.tmict.com",
    'category': 'TMICT',
    'version': '15.0.1.0.0',
    'depends': [
        'hr',
        'hr_contract',
        'business_unit',
    ],
    'external_dependencies' : {},
    'data': [
        'security/hr_security.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
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
