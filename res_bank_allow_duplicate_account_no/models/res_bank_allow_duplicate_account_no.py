# -*- coding: utf-8 -*-

import re

from collections.abc import Iterable

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError

import werkzeug.urls


class ResPartnerBank(models.Model):
    _name = 'res.partner.bank'

    def _auto_init(self, cr, context=None):
        self._sql_constraints = [
            ('unique_number', 'unique(sanitized_acc_number, bank_id, company_id)', 'Account Number must be unique')
        ]
          super(ResPartnerBank, self)._auto_init(cr, context)
