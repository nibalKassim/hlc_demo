# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import format_date


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    business_unit_id = fields.Many2one(
        comodel_name='business.unit',
        string='Business Unit',
        ondelete='cascade',
        default= lambda self: self._get_default_business_unit()
    )

    def _get_available_contracts_domain(self):
        res = super(HrPayslipEmployees, self)._get_available_contracts_domain()
        res.append(('business_unit_id', '=', self.business_unit_id.id))
        return res

    @api.model
    def _get_default_business_unit(self):
        bu = False
        active_id = self.env.context.get('active_id', False)
        if active_id and self.env.context.get('active_model',False) == 'hr.payslip.run':
            active_id = self.env['hr.payslip.run'].browse(active_id)
            bu = active_id.business_unit_id
        else:
            bu = self.env['res.users'].business_unit_default_get()
        return bu

    @api.depends('department_id', 'structure_id')
    def _compute_employee_ids(self):
        super(HrPayslipEmployees, self)._compute_employee_ids()
