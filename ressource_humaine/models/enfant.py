# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHEnfant(models.Model):
    _name = 'rh.enfant'
    _rec_name = 'employee_id'


    nom_enfant = fields.Char()
    prenom_enfant = fields.Char()
    date_naissance_enfant = fields.Date()
    scolarite = fields.Boolean(default=False)
    enfant_file_lines = fields.One2many('rh.file', 'enfant_id')
    employee_id = fields.Many2one('hr.employee')