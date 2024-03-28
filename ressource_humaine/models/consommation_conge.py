# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHConsommationConge(models.Model):
    _name = 'rh.consommation.conge'

    date_debut_conge = fields.Date()
    date_fin_conge = fields.Date()
    date_fin_prevue = fields.Date()






