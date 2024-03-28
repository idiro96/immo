# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHNiveauHierarchique(models.Model):
    _name = 'rh.niveau.hierarchique'
    _rec_name = 'intitule'

    intitule = fields.Char()
    bonification_indiciaire = fields.Integer()

    section_superieure_id = fields.Many2one('rh.section.superieure')



