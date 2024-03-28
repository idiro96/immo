# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHCategorieSuperieure(models.Model):
    _name = 'rh.categorie.superieure'
    _rec_name = 'intitule'

    intitule = fields.Char()
    description = fields.Char()


