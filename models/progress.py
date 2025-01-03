# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime


class TerritoryLap(models.Model):
    _name = "territory.lap"
    _description = "Territory Laps"

    name = fields.Char()
    date_start = fields.Date()
    date_end = fields.Date()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("progress", "In Progress"),
            ("pause", "In Pause"),
            ("done", "Done"),
        ]
    )
    lap_warning = fields.Char()


class TerritoryProgress(models.Model):
    _name = "territory.progress"
    _description = "Territories Progress"

    name = fields.Char()
    notes = fields.Text()
    territory_id = fields.Many2one("preaching.territory")
    lap_id = fields.Many2one("territory.lap")
    state = fields.Selection(
        [
            ("pending", "To Work"),
            ("partially", "Partially Worked"),
            ("done", "Completed"),
        ]
    )
    date_start = fields.Date()
    date_end = fields.Date()
    meeting_point = fields.Char()
    street_lines = fields.Many2one("")
    progress_warning = fields.Char()


class TerritoryProgressLine(models.Model):
    _name = "territory.progress.line"
    _description = "Territory Progress Streets"

    name = fields.Char()
    sidewalk = fields.Selection(
        [("n", "North"), ("s", "South"), ("e", "East"), ("w", "West")]
    )
    between_strets = fields.Char()
    num_houses = fields.Integer()
    notes = fields.Text()
