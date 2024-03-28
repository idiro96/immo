# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CompanyInherited(models.Model):
    _inherit = 'res.company'

    num_adh = fields.Char(string='N° Adhérent')
    raison_sociale = fields.Char()
    raison_sociale_fr = fields.Char()


