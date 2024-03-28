# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHCritere(models.Model):
    _name = 'rh.critere'

    code_critere = fields.Char()
    description_critere = fields.Date()



