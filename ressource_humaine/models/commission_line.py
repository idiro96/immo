# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHcommissionLine(models.Model):
    _name = 'rh.commission.line'

    employee_id = fields.Many2one('hr.employee')
    sanction_id = fields.Many2one('rh.sanction')
    department_id = fields.Char()
    job_id = fields.Char()
    # date_commission= fields.Date()
