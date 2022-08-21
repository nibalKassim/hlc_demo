# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    
    _inherit = 'res.users'
   
    @api.model
    def business_unit_default_get(self, user_id=False):
        if not user_id:
            user_id = self._uid
        user = self.env['res.users'].browse(user_id)
        return user.default_business_unit_id

    @api.model
    def _default_business_unit(self):
        return self.business_unit_default_get()
    
    @api.model
    def _default_business_units(self):
        return self._default_business_unit()

    business_unit_ids = fields.One2many(
        comodel_name="business.unit",
        compute="_compute_business_unit_ids",
        inverse="_inverse_business_unit_ids",
    )
    assigned_business_unit_ids = fields.Many2many(
        comodel_name='business.unit',
        relation='business_unit_users_rel',
        column1='user_id',
        column2='bu_id',
        string='Business Units',
        default=lambda self: self._default_business_units()
    )
    default_business_unit_id = fields.Many2one(
        comodel_name='business.unit',
        string='Default Business Unit',
        default=lambda self: self._default_business_unit()
    )

    @api.depends("groups_id", "assigned_business_unit_ids")
    def _compute_business_unit_ids(self):
        for user in self:
            if user.has_group("business_unit.group_manager_business_unit"):
                dom = []
                if self.env.context.get("allowed_company_ids"):
                    dom = [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "in", self.env.context["allowed_company_ids"]),
                    ]
                else:
                    dom = []
                user.business_unit_ids = self.env["business.unit"].sudo().search(dom)
            else:
                user.business_unit_ids = user.assigned_business_unit_ids

    def _inverse_business_unit_ids(self):
        for user in self:
            user.assigned_business_unit_ids = user.business_unit_ids
