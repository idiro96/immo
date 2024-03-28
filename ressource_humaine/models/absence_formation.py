# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAbsenceFormation(models.Model):
    _name = 'rh.absence.formation'
    _rec_name = 'employee_id'


    formation_line_id = fields.Many2one('rh.formation.line')
    formation_id = fields.Many2one('rh.formation')
    employee_id = fields.Many2one('hr.employee')
    date_absence = fields.Date()