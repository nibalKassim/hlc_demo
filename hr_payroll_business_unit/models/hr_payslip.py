# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging

from collections import defaultdict
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, Command, fields, models, _
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, date_utils, convert_file, html2plaintext
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    business_unit_id = fields.Many2one(
        comodel_name='business.unit',
        string='Business Unit',
        ondelete='cascade',
        default=lambda self: self.payslip_run_id.business_unit_id
    )

    def write(self, vals):
        vals['business_unit_id'] = self.payslip_run_id.business_unit_id
        super(HrPayslip, self).write(vals)
