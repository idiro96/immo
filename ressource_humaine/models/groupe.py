# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHGroupe(models.Model):
    _name = 'rh.groupe'
    _rec_name = 'name'

    name = fields.Char()
    description = fields.Char()
    grade_lines = fields.One2many('rh.grade', inverse_name='grade_id')
    grille_id = fields.Many2one('rh.grille')
    categorie_lines = fields.One2many('rh.categorie', inverse_name='groupe_id')



