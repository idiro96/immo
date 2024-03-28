# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHCongeDroit(models.Model):
    _name = 'rh.conge_droit_month'

    id_conge_droit = fields.Many2one(comodel_name='rh.congedroit')
    month = fields.Char()

    @api.model
    def my_function(self):
        (print('testaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))










