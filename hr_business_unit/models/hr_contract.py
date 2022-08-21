# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    business_unit_id = fields.Many2one(
        comodel_name='business.unit',
        string='Business Unit',
        ondelete='cascade',        
        default=lambda self: self.env['res.users'].business_unit_default_get()
    )

    @api.constrains('business_unit_id', 'company_id')
    def _check_company_business_unit(self):
        for team in self:
            if (team.company_id and team.business_unit_id and
                    team.company_id != team.business_unit_id.company_id):
                raise UserError(_('Configuration error, '
                                  'The Company in the Sales Team and in the '
                                  'Business Unit must be the same.'))
