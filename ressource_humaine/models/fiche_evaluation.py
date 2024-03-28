# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class RHFicheEvaluation(models.Model):
    _name = 'rh.fiche.evaluation'

    date_evaluation = fields.Date(required=True, store=True)
    employee_id = fields.Many2one('hr.employee', required=True, store=True)
    grade_id = fields.Many2one('rh.grade', compute='_onchange_employee_id', store=True)
    job_id = fields.Many2one('hr.job', compute='_onchange_employee_id', store=True)
    echelon_id = fields.Many2one('rh.echelon', compute='_onchange_employee_id', store=True)
    date_grade = fields.Date()
    note = fields.Integer()
    observation = fields.Char()
    fiche_evaluation_file = fields.Binary()
    exercice = fields.Integer(compute='_compute_exercice', store=True)

    # annee = exercice

    @api.model
    def create(self, vals):
        # recalculer la valeur de "exercice"
        if vals.get('date_evaluation'):
            date_str = vals['date_evaluation']
            exercice = datetime.strptime(date_str, '%Y-%m-%d').year
            # verifier l'existance de l'enregistrement
            evaluation = self.env['rh.fiche.evaluation'].search(
                [('employee_id', '=', vals['employee_id']), ('exercice', '=', exercice)])
            if evaluation:
                raise UserError("L employee choisit possède déja une notation pour cet exercice")
            else:
                evalutation = super(RHFicheEvaluation, self).create(vals)
                return evalutation
        else:
            raise UserError("Entrer la date d'evaluation")

    @api.depends('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            rec.grade_id = rec.employee_id.grade_id
            rec.job_id = rec.employee_id.job_id
            rec.echelon_id = rec.employee_id.echelon_id

    @api.depends('date_evaluation')
    def _compute_exercice(self):
        for rec in self:
            print('teste')
            if rec.date_evaluation:
                date_str = rec.date_evaluation
                rec.exercice = datetime.strptime(date_str, '%Y-%m-%d').year
                evaluation = self.env['rh.fiche.evaluation'].search(
                    [('employee_id', '=', rec.employee_id.id), ('exercice', '=', rec.exercice)])
                if evaluation:
                    raise UserError("L employee choisit possède déja une notation pour cet exercice")

