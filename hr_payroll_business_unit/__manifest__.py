# -*- coding: utf-8 -*-
# Inspired from OCA Operating Units

{
    'name': "TMICT - HR Payroll Business Unit",
    'summary': """
        HR Payroll Unit within a company.""",
    'description': "",
    'author': "TMICT",
    'website': "http://www.tmict.com",
    'category': 'TMICT',
    'version': '15.0.1.0.0',
    'depends': [
        'hr_payroll',
    ],
    'external_dependencies' : {},
    'data': [
        'views/hr_payslip_run_views.xml',
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
