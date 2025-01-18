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
            # FOR EVERY DATA TERRITORY CREATE ONE PROGRESS TERRITORY
            prog_id = territory_progress.create(
                {
                    "name": territory.name,
                    "territory_id": territory.id,
                    "lap_id": self.id,
                    "state": "pending",
                }
            )
            # CREATE LINE STREET
            if prog_id:
                progress_line = self.env["territory.progress.line"]
                for street in territory.street_lines:
                    progress_line.create(
                        {
                            "name": street.name,
                            "progress_id": prog_id.id,
                            "sidewalk": street.sidewalk,
                            "between_streets": street.between_streets,
                            "num_houses": street.num_houses,
                        }
                    )
        self.state = "progress"


class TerritoryProgress(models.Model):
    _name = "territory.progress"
    _description = "Territories Progress"

    name = fields.Char()
    notes = fields.Text()
    territory_id = fields.Many2one("preaching.territory")
    group_id = fields.Many2one(related="territory_id.group_id")
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
    responsible = fields.Char()

    def mark_done(self):
        if self.responsible:
            for line in self.street_lines:
                line.write({"done": 1})
            self.write({"state": "done", "date_end": date.today()})
        else:
            raise UserError(_("You need to define the responsible first"))

    # def write(self, vals):
    #     res = super(TerritoryProgress, self).write(vals)
    #     total_lines = len(self.street_lines)
    #     done_lines = len(self.street_lines.filtered(lambda l: l.done))
    #     if not done_lines == total_lines:
    #         self.state = "partially"
    #     return res


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
