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
    territory_progress_ids = fields.One2many("territory.progress", "lap_id")

    def start_lap(self):
        territory_ids = self.env["preaching.territory"].search([(1, "=", 1)])
        territory_progress = self.env["territory.progress"]
        for territory in territory_ids:
            street_lines = []
            for street in territory.street_lines:
                street_values = {
                    "name": street.name,
                    "sidewalk": street.sidewalk,
                    "between_streets": street.between_streets,
                    "num_houses": street.between_streets,
                }
                street_lines.append(street_values)
            territory_progress.create(
                {
                    "name": territory.name,
                    "territory_id": territory.id,
                    "lap_id": self.id,
                    "state": "pending",
                    "street_lines": [(6, 0, street_lines)],
                }
            )


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
    street_lines = fields.One2many("territory.progress.line", "progress_id")
    progress_warning = fields.Char()


class TerritoryProgressLine(models.Model):
    _name = "territory.progress.line"
    _description = "Territory Progress Streets"

    name = fields.Char()
    progress_id = fields.Many2one("territory.progress")
    sidewalk = fields.Selection(
        [("n", "North"), ("s", "South"), ("e", "East"), ("w", "West")]
    )
    between_streets = fields.Char()
    num_houses = fields.Integer()
    done = fields.Boolean(default=False)
    notes = fields.Text()
