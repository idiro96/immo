# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RHChoisirCommission(models.TransientModel):
    _name = 'choisir.commission'


    employee_id_lines = fields.One2many('hr.employee', 'visite_medical_detaille_id', string="Visite Medical Lines", default=lambda self: self._default_employees())



    def valider_commission(self):
        record = self.env['rh.sanction'].browse(self._context['active_id'])
        for line in self.employee_id_lines:
            if line.selection_employe == True:
                commission_line = self.env['rh.commission.line'].create({
                'employee_id': line.id,
                'department_id': line.department_id.name,
                'job_id': line.job_id.name,
                'sanction_id':record.id,
                })


    @api.model
    def _default_employees(self):
        records = self.env['hr.employee'].search([])
        for rec in records:
            rec.selection_employe = False
        return records







