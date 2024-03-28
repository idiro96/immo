# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHAvancementCommissionLine(models.Model):
    _name = 'rh.avancement.commission.line'


    employee_id = fields.Many2one('hr.employee')
    avancement_id = fields.Many2one('rh.avancement')
    department_id = fields.Char()
    job_id = fields.Char()
    # date_commission= fields.Date()
