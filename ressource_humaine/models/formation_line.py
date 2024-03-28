# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError




class RHFormationLine(models.Model):
    _name = 'rh.formation.line'


    employee_id = fields.Many2one('hr.employee')
    formation_id = fields.Many2one('rh.formation')
    date_debut_formation_line = fields.Date()
    date_fin_formation_line = fields.Date()
    # nbr_jour_assiste = fields.Integer()
    groupe = fields.Selection(
        [('groupe1', 'Groupe 1'), ('groupe2', 'Groupe 2'), ('groupe3', 'Groupe 3'), ('groupe4', 'Groupe 4'),
         ('groupe5', 'Groupe 5')])


    def formation_absence(self):
        context = {
            'default_employee_name': self.employee_id.name,
        }

        return {
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name': 'Formation absence',
        'view_mode': 'form',
        'res_model': 'absence.formation',
        'context': context,
        }









