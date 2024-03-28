# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHSectionSuperieure(models.Model):
    _name = 'rh.section.superieure'
    _rec_name = 'intitule'

    intitule = fields.Char()
    description = fields.Char()

    categorie_superieure_id = fields.Many2one('rh.categorie.superieure')



