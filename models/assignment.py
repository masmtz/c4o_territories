# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime


class PreachingAssignment(models.Model):
    _name = "preaching.assignment"
    _description = "Preaching Assignment"

    name = fields.Char()
    user_id = fields.Many2one("res.users", string="Responsible", tracking=True)
    date = fields.Date(string="Date assignment", tracking=True)
