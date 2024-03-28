# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class RHFicheEvaluation(models.Model):
    _name = 'rh.fiche.evaluation'

    date_evaluation = fields.Date()
    employee_id = fields.Many2one('hr.employee')
    grade_id = fields.Many2one('rh.grade',compute='_onchange_employee_id', store=True)
    job_id = fields.Many2one('hr.job',compute='_onchange_employee_id', store=True)
    echelon_id = fields.Many2one('rh.echelon',compute='_onchange_employee_id', store=True)
    date_grade = fields.Date()
    note = fields.Integer()
    observation = fields.Char()
    fiche_evaluation_file = fields.Binary()
    exercice = fields.Integer()


    @api.model
    def create(self, vals):
        evaluation = self.env['rh.fiche.evaluation'].search([('employee_id', '=', vals['employee_id']),('exercice', '=', vals['exercice'])])
        print(evaluation)
        if evaluation:
            raise UserError("L employee choisit possède déja une notation pour cet exercice")
        evalutation = super(RHFicheEvaluation, self).create(vals)
        return evalutation

    # @api.constrains('employee_id','exercice')
    # def _check_contract_overlap(self):
    #     for evaluation in self:
    #         overlapping_evaluation = self.search([
    #             ('employee_id', '=', evaluation.employee_id.id),
    #             ('exercice', '=', evaluation.exercice),
    #         ])
    #         if overlapping_evaluation:
    #             raise UserError("L employee choisit possède déja une notation pour cet exercice")


    @api.depends('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            rec.grade_id = rec.employee_id.grade_id
            rec.job_id = rec.employee_id.job_id
            rec.echelon_id = rec.employee_id.echelon_id


    @api.onchange('date_evaluation')
    def _onchange_date_evaluation(self):
        for rec in self:
            print('teste')
            if rec.date_evaluation:
                rec.exercice = datetime.strptime(rec.date_evaluation, '%Y-%m-%d').year

