# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError




class RHAbsenceFormation(models.TransientModel):
    _name = 'absence.formation'

    date_absence = fields.Date()
    employee_name = fields.Char()
    # employee_name = fields.Char(default=lambda self: self._default_employees())

    @api.constrains('date_absence')
    def _check_date_absence_within_interval(self):
        for wizard in self:
            if wizard.date_absence:
                formation_line = self.env['rh.formation.line'].browse(self._context.get('active_id'))
                start_date = formation_line.date_debut_formation_line
                end_date = formation_line.date_fin_formation_line
                if not (start_date <= wizard.date_absence <= end_date):
                    raise ValidationError(_("La date d''absence doit étre dans l'interval de la formation"))

    def absence_formation(self):
        record = self.env['rh.formation.line'].browse(self._context['active_id'])
        for line in record:
            absence_formation = self.env['rh.absence.formation'].create({
                    'employee_id': line.employee_id.id,
                    'formation_line_id': line.id,
                    'formation_id': line.formation_id.id,
                    'date_absence': self.date_absence
                })

    # @api.one
    # def _default_employees(self):
    #
    #     record = self.env['rh.formation.line'].browse(self._context['active_id'])
    #     print(record)
    #     for rec in record:
    #         print(rec.employee_id.name)
    #         self.employee_name = rec.employee_id.name
    #     return self.employee_name