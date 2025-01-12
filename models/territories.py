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
    group_id = fields.Many2one("territory.group")


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
        for rec in self:
            # str_bstreets = ""
            str_street_1 = ""
            str_street_2 = ""
            if rec.w_street and rec.e_street:
                str_street_1 = rec.e_street
                str_street_2 = rec.w_street
                # str_bstreets = _(
                #     "Between %(w_street)s and %(e_street)s",
                #     w_street=rec.e_street,
                #     e_street=rec.w_street,
                # )

            if rec.n_street and rec.s_street:
                str_street_1 = rec.n_street
                str_street_2 = rec.s_street
                # str_bstreets = _(
                #     "Between %(n_street)s and %(n_street)s",
                #     w_street=rec.n_street,
                #     e_street=rec.s_street,
                # )
            # rec.between_streets = str_bstreets
            rec.between_streets =  = _(
                    "Between %(street_1)s and %(street_2)s",
                    street_1=str_street_1,
                    street_2=str_street_2,
                )


class TerritoryGroup(models.Model):
    _name = "territory.group"
    _description = "Territories Groups"

    name = fields.Char()


class TerritoryConfigParamenter(models.Model):
    _name = "territory.config.parameter"

    name = fields.Char()
    daily_time = fields.Float()  # Tiempo diario
