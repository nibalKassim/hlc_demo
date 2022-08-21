# -*- coding: utf-8 -*-

import re

from collections.abc import Iterable

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError

import werkzeug.urls


class ResPartnerBank(models.Model):
    _name = 'res.partner.bank'


