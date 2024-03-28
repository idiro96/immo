# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHCategorie(models.Model):
    _name = 'rh.categorie'
    _rec_name = 'intitule'

    intitule = fields.Char()
    description = fields.Char()
    Indice_minimal = fields.Integer()
    groupe_id = fields.Many2one('rh.groupe')
    grille_id = fields.Many2one('rh.grille')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    code_type_fonction = fields.Char(related='type_fonction_id.code_type_fonction',
                                      store=True)


    @api.onchange('grille_id')
    def _onchange_grille_id(self):
        if self.grille_id:
            self.groupe_id = False
            return {'domain': {'groupe_id': [('grille_id', '=', self.grille_id.id)]}}
        else:
            return {'domain': {'groupe_id': []}}
