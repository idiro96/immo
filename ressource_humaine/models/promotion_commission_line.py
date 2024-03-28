# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHPromotionCommissionLine(models.Model):
    _name = 'rh.promotion.commission.line'


    employee_id = fields.Many2one('hr.employee')
    promotion_id = fields.Many2one('rh.promotion')
    department_id = fields.Char()
    job_id = fields.Char()
    # date_commission= fields.Date()
