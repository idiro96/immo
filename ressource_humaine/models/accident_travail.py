# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAccidentTravail(models.Model):
    _name = 'rh.accident.travail'
    _rec_name = 'employee_id'


    date_accident_travail = fields.Date()
    description_accident_travail = fields.Text()
    num_pv_accident_travail = fields.Integer()
    employee_id = fields.Many2one('hr.employee')
    accident_travail_file_lines = fields.One2many('rh.file', 'accident_travail_id')






