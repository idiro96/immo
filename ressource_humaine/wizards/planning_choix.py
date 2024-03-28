# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RHChoisirPlanning(models.TransientModel):
    _name = 'choisir.planning'


    employee_id_lines = fields.One2many('hr.employee', 'planning_choix_id', string="Planning Choix Lines", default=lambda self: self._default_employees())


    def valider_planning(self):
        record = self.env['rh.planning'].browse(self._context['active_id'])
        for line in self.employee_id_lines:
            if line.selection_employe == True:
                print(line.id)
                planning_line = self.env['rh.planning.line'].create({
                    'planning_survellance_id': record.id,
                    'employee_id': line.id,
                    'emphy_id': line.emphy_id.id,
                })


    @api.model
    def _default_employees(self):
        records = self.env['hr.employee'].search([])
        for rec in records:
            rec.selection_employe = False
        return records
