
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RHVisiteMedicalDetaille(models.TransientModel):
    _name = 'visite.medical.detaille'


    employee_id_lines = fields.One2many('hr.employee', 'visite_medical_detaille_id', string="Visite Medical Lines", default=lambda self: self._default_employees())

    date_visite_medicale = fields.Date()


    def detaille_viste_medical(self):
        record = self.env['rh.visite.medicale'].browse(self._context['active_id'])
        for line in self.employee_id_lines:
            if line.selection_employe == True:
                visite_medical = self.env['rh.visite.medical.line'].create({
                'employee_id': line.id,
                'visite_medical_id':record.id,
                'date_visite_medicale': self.date_visite_medicale,
                })


    @api.model
    def _default_employees(self):
        records = self.env['hr.employee'].search([])
        for rec in records:
            rec.selection_employe = False
        return records



