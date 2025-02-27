# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class PreachingAssignment(models.Model):
    _name = "preaching.assignment"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]
    _description = "Preaching Assignment"

    @api.depends("date")
    def _compute_week_number(self):
        for rec in self:
            week_no = 0
            week_id = False
            if rec.date:
                week_no = rec.date.isocalendar()[1]
                week_id = self.env["territory.week.assignment"].search(
                    [("week", "=", week_no)], limit=1
                )
            rec.week_id = week_id

    def _compute_message(self):
        self.assignment_warning = ""
        self.overdue = False
        if not self.territory_progress_ids and self.assigment_type == "in_person":
            self.assignment_warning = _(
                "There are no territories assigned for these day. Please ask your system administrator."
            )
        if (self.date + timedelta(hours=2)) < datetime.now():
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
    overdue = fields.Boolean(compute="_compute_message")
    week_id = fields.Many2one(
        "territory.week.assignment", compute="_compute_week_number"
    )
    # territory_progress_ids = fields.One2many(
    #     "preaching.assignment.territory", "week_id"
    # )
    territory_progress_ids = fields.One2many(
        related="week_id.territory_progress_ids", tracking=True
    )

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

    def cron_send_email(self):
        for record in self:
            if record.date.date() == datetime.today() + timedelta(days=1):
                raise UserError("Entró")
                subject = "Recordatorio de asignación"
                body_html = (
                    "Estimado %s, \nUsted tiene una asignación (%s) para el día %s, para sacar el grupo de predicación."
                    % s(record.user_id.name, record.assigment_type, record.date)
                )
                email_to = record.user_id.email
                record.send_email(
                    subject, body_html, email_to, "s.mtz.casillas@gmail.com"
                )

    def send_email(
        self, subject, body_html, email_to, email_from="s.mtz.casillas@gmail.com"
    ):
        mail_message_obj = self.env["mail.mail"]
        email_vals = {
            "subject": subject,
            "body_html": body_html,
            "email_to": email_to,
            "email_from": email_from,
        }
        # Creamos el Correo
        mail_id = mail_message_obj.create(email_vals)
        # Mostramos la ventana para enviar correo
        mail_id.send(False, False)
        return True


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
                raise UserError(_("The date must be Monday"))

    name = fields.Char("")
    date_start = fields.Date()
    date_end = fields.Date()
    week = fields.Integer(compute="_compute_week_number", store=True)
    territory_progress_ids = fields.One2many(
        "preaching.assignment.territory", "week_id"
    )
    meeting_point = fields.Char(string="Meeting point")

    @api.model
    def create(self, vals):
        date_start = datetime.strptime(str(vals["date_start"]), "%Y-%M-%d").strftime(
            "%d-%m-%Y"
        )
        date_end = datetime.strptime(str(vals["date_end"]), "%Y-%M-%d").strftime(
            "%d-%m-%Y"
        )
        vals["name"] = _(
            "Week %s (%s)"
            % (
                vals["week"],
                date_start[-4:],
            )
        )
        return super(TerritoryWeekAssignment, self).create(vals)

    def write(self, vals):
        date_start = datetime.strptime(str(self.date_start), "%Y-%M-%d").strftime(
            "%d-%m-%Y"
        )
        date_end = datetime.strptime(str(self.date_end), "%Y-%M-%d").strftime(
            "%d-%m-%Y"
        )
        vals["name"] = _(
            "Week %s (%s)"
            % (
                self.week,
                date_start[-4:],
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
    # assignment_id = fields.Many2one("preaching.assignment")
    week_id = fields.Many2one("territory.week.assignment")

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

    def open_territory(self):
        self.ensure_one()
        return {
            "name": _("Territory"),
            "type": "ir.actions.act_window",
            "res_model": "territory.progress",
            "view_mode": "form",
            "res_id": self.territory_id.id,
            "domain": [("id", "=", self.territory_id.id)],
        }
