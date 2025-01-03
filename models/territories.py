# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime


class PreachingTerritory(models.Model):
    _name = "preaching.territory"
    _description = "Preaching Territories"

    name = fields.Char()
    description = fields.Text()
    street_lines = fields.One2many()
    image = fields.Binary()
    num_houses = fields.Integer()


class TerritoryStreet(models.Model):
    _name = "territory.street"
    _description = "Territory Streets"

    name = fields.Char()
    sidewalk = fields.Selection(
        [("n", "North"), ("s", "South"), ("e", "East"), ("w", "West")]
    )
    n_street = fields.Char(default="N/A")
    s_street = fields.Char(default="N/A")
    e_street = fields.Char(default="N/A")
    w_street = fields.Char(default="N/A")
    num_houses = fields.Integer()
    notes = fields.Text()


class TerritoryConfigParamenter(models.Model):
    _name = "territory.config.parameter"

    name = fields.Char()
    daily_time = fields.Float()  # Tiempo diario
