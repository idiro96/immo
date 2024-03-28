# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHNiveauHierarchiqueCheBureau(models.Model):
    _name = 'rh.niveau.hierarchique.chef.bureau'
    _rec_name = 'intitule'

    intitule = fields.Char()
    bonification_indiciaire = fields.Integer()





