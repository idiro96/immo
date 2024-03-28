# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHConjoint(models.Model):
    _name = 'rh.conjoint'
    _rec_name = 'employee_id'


    nom_conjoint = fields.Char()
    prenom_conjoint = fields.Char()
    date_naissance_conjoint = fields.Date()
    lieu_naissance_conjoint = fields.Char()
    date_mariage = fields.Date()
    femme_foyer = fields.Boolean(default=False)
    conjoint_file_lines = fields.One2many('rh.file', 'conjoint_id')
    employee_id = fields.Many2one('hr.employee')


