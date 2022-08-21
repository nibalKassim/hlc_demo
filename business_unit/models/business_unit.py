from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessUnit(models.Model):
    
    _name = 'business.unit'
    _description = 'Business Unit'
    
    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        translate=True
        )
    code = fields.Char(
        string='Code',
        size=5,
        required=True,
        copy=False
        )
    active = fields.Boolean(
        default=True
        )
    initialized = fields.Boolean(
        string='Initialized',
        default=False
        )
    parent_id = fields.Many2one(
        comodel_name='business.unit', 
        string='Parent Unit', 
        index=True
        )
    child_ids = fields.One2many(
        comodel_name='business.unit', 
        inverse_name='parent_id', 
        string='Child Units'
        )
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
        domain="[('is_company','=',True)]"
        )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        )

    default_user_ids = fields.One2many(
        comodel_name='res.users',
        inverse_name='default_business_unit_id',
        string='Default Users'
        )   
    user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='business_unit_users_rel',
        column1='bu_id',
        column2='user_id',
        string='Allowed Users',
        )

    #Report Related
    is_bu_report = fields.Boolean(
        string='Business Unit Report',
        help='Business unit custom report template.',
        default=False,
        )
    is_bu_header = fields.Boolean(
        string='Custom Header',
        help='Use custom report header and override the default one.',
        default=False,
        ) 
    report_header = fields.Html(
        string='Header'
        )
    report_tagline = fields.Text(
        string='Report Tagline', 
        help="Appears by default on the top right corner of your printed documents (report header).",
        translate=True
        )
    report_footer = fields.Text(
        string='Report Footer',
        translate=True,
        help="Footer text displayed at the bottom of all reports."
        )


    sale_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string='Sale Sequence',
        copy=False
        )
#    crm_team_ids = fields.One2many(
#        comodel_name='crm.team',
#        inverse_name='business_unit_id',
#        string='Sale Teams'
#        ) 
#     journal_ids = fields.One2many(
#         comodel_name='account.journal',
#         inverse_name='business_unit_id',
#         string='Journals'
#         )   
            
     
    _sql_constraints = [
        ('code_company_uniq', 'unique (code,company_id)',
         'The code of the business unit must '
         'be unique per company!'),
        ('name_company_uniq', 'unique (name,company_id)',
         'The name of the business unit must '
         'be unique per company!')
    ]

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive Business Units.'))
            
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=80):
        # Make a search with default criteria
        names1 = super(models.Model, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # Make the other search
        names2 = []
        if name:
            domain = [('code', '=ilike', name + '%')]
            names2 = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]
    
    @api.model
    def create(self, values):
        bu = super(BusinessUnit, self).create(values)
        bu.user_ids += self.env.user
        self.clear_caches()
        return bu

    def write(self, vals):
        self.clear_caches()
        return super(BusinessUnit, self).write(vals)
