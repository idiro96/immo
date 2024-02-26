
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHTypeFonction(models.Model):
    _name = 'rh.type.fonction'
    _rec_name = "intitule_type_fonction"



    code_type_fonction = fields.Char()
    intitule_type_fonction = fields.Char()




