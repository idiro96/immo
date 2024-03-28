# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHSpecialite(models.Model):
    _name = 'rh.specialite'

    code_specialite = fields.Char()
    intitule_specialite = fields.Char()





