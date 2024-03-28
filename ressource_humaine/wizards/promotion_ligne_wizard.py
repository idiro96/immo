# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHPromotionLine(models.TransientModel):
    _name = 'rh.promotion.line.wizard'

    date_promotion = fields.Date()
    promotion_id = fields.Many2one('hr.promotion')
    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    job_id = fields.Many2one('hr.job')
    code_type_fonction = fields.Char(related='employee_id.nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)


    grade_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    duree = fields.Integer()




