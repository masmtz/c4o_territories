# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime


class PreachingTerritory(models.Model):
    _name = "preaching.territory"
    _description = "Preaching Territories"

    name = fields.Char()
    description = fields.Text()
    street_lines = fields.One2many("territory.street", "territory_id", copy=True)
    image = fields.Binary()
    num_houses = fields.Integer()


class TerritoryStreet(models.Model):
    _name = "territory.street"
    _description = "Territory Streets"

    name = fields.Char()
    territory_id = fields.Many2one("preaching.territory")
    sidewalk = fields.Selection(
        [("n", "North"), ("s", "South"), ("e", "East"), ("w", "West")]
    )
    n_street = fields.Char()
    s_street = fields.Char()
    e_street = fields.Char()
    w_street = fields.Char()
    between_streets = fields.Char(compute="compute_between_streets")
    num_houses = fields.Integer()
    notes = fields.Text()

    @api.depends("n_street", "s_street", "w_street", "e_street")
    def compute_between_streets(self):
        str_bstreets = ""
        if self.w_street and self.e_street:
            str_bstreets = _("Between " + self.w_street + " and " + self.e_street)

        if self.n_street and self.s_street:
            str_bstreets = _("Between " + self.n_street + " and " + self.s_street)
        self.between_streets = str_bstreets


class TerritoryConfigParamenter(models.Model):
    _name = "territory.config.parameter"

    name = fields.Char()
    daily_time = fields.Float()  # Tiempo diario
