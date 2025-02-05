# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class PreachingAssignment(models.Model):
    _name = "preaching.assignment"
    _description = "Preaching Assignment"

    def _compute_message(self):
        self.assignment_warning = ""
        self.overdue = False
        if not self.territory_progress_ids and self.assigment_type == "in_person":
            self.assignment_warning = _(
                "There are no territories assigned for these day. Ask your system administrator."
            )
        if self.date < datetime.now():
            self.overdue = True
            # self.assignment_warning = _("This assignment has expired.")

    name = fields.Char()
    user_id = fields.Many2one("res.users", string="Responsible", tracking=True)
    date = fields.Datetime(string="Date assignment", tracking=True)
    assigment_type = fields.Selection(
        [("in_person", "In Person"), ("zoom", "Zoom")],
    )
    assignment_warning = fields.Char(compute="_compute_message")
    notes = fields.Text()
    # territory_progress_ids = fields.One2many("territory.progress", "assignment_id")
    territory_progress_ids = fields.One2many(
        "preaching.assignment.territory", "assignment_id"
    )
    overdue = fields.Boolean(compute="_compute_message")

    @api.model
    def create(self, vals):
        user_id = self.env["res.users"].browse(vals["user_id"])
        vals["name"] = user_id.name
        return super(PreachingAssignment, self).create(vals)

    def write(self, vals):
        user_id = user_id = self.user_id
        if "user_id" in vals:
            user_id = self.env["res.users"].browse(vals["user_id"])

        vals["name"] = user_id.name
        return super(PreachingAssignment, self).write(vals)


class TerritoryWeekAssignment(models.Model):
    _name = "territory.week.assignment"
    _description = "Territory Week Assignment"

    @api.depends("date_start")
    def _compute_week_number(self):
        week_no = 0
        if self.date_start:
            if self.date_start.weekday() == 0:
                week_no = self.date_start.isocalendar()[1]
                self.week = week_no
                self.date_end = self.date_start + timedelta(days=6)
            else:
                raise UserError("The date must be Monday")

    name = fields.Char("")
    date_start = fields.Date()
    date_end = fields.Date()
    week = fields.Integer(compute="_compute_week_number", store=True)
    territory_progress_ids = fields.One2many(
        "preaching.assignment.territory", "assignment_id"
    )

    @api.model
    def create(self, vals):
        vals["name"] = _(
            "Week %s (From %s To %s)"
            % (
                self.week,
                datetime.strptime(str(self.date_start), "%Y-%M-%d").strftime(
                    "%d-%m-%Y"
                ),
                self.date_end,
            )
        )
        return super(TerritoryWeekAssignment, self).create(vals)

    def write(self, vals):
        vals["name"] = _(
            "Week %s (From %s To %s)"
            % (
                self.week,
                datetime.strptime(str(self.date_start), "%Y-%M-%d").strftime(
                    "%d-%m-%Y"
                ),
                self.date_end,
            )
        )
        return super(TerritoryWeekAssignment, self).write(vals)


class PreachingAssignmentTerritory(models.Model):
    _name = "preaching.assignment.territory"
    _description = "Preaching Assignment Territories"

    name = fields.Char()
    sequence = fields.Integer()
    territory_id = fields.Many2one("territory.progress")
    territory_state = fields.Selection(related="territory_id.state")
    assignment_id = fields.Many2one("preaching.assignment")

    @api.model
    def create(self, vals):
        territory_id = self.env["territory.progress"].browse(vals["territory_id"])
        vals["name"] = territory_id.name
        return super(PreachingAssignmentTerritory, self).create(vals)

    def write(self, vals):
        territory_id_id = user_id = self.territory_id
        if "territory_id" in vals:
            territory_id = self.env["territory.progress"].browse(vals["territory_id"])

        vals["name"] = territory_id.name
        return super(PreachingAssignmentTerritory, self).write(vals)
