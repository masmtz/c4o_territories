# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime


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

    name = fields.Char("")
    week = fields.Integer()
    territory_progress_ids = fields.One2many(
        "preaching.assignment.territory", "assignment_id"
    )


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
