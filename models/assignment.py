# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime


class PreachingAssignment(models.Model):
    _name = "preaching.assignment"
    _description = "Preaching Assignment"

    name = fields.Char()
    user_id = fields.Many2one("res.users", string="Responsible", tracking=True)
    date = fields.Datetime(string="Date assignment", tracking=True)
    assigment_type = fields.Selection(
        [("in_person", "In Person"), ("zoom", "Zoom")],
    )
    assignment_warning = fields.Char()
    notes = fields.Text()

    @api.model
    def create(self, vals):
        vals["name"] = vals["user_id"]
        return super(PreachingAssignment, self).create(vals)
