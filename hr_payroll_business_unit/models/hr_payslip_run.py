# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    business_unit_id = fields.Many2one(
        comodel_name='business.unit',
        string='Business Unit',
        ondelete='cascade',        
        default=lambda self: self.env['res.users'].business_unit_default_get()
    )

