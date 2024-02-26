# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHVisiteMedicalLine(models.Model):
    _name = 'rh.visite.medical.line'


    employee_id = fields.Many2one('hr.employee')
    visite_medical_id = fields.Many2one('rh.visite.medicale')
    date_visite_medicale = fields.Date()






