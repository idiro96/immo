# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHEchelon(models.Model):
    _name = 'rh.echelon'
    _rec_name = 'intitule'

    intitule = fields.Char()
    indice_echelon = fields.Integer()
    categorie_id = fields.Many2one('rh.categorie')
    groupe_id = fields.Many2one('rh.groupe',readonly=True, compute='_compute_categorie_fields')
    type_fonction = fields.Many2one('rh.type.fonction', domain="[('code_type_fonction', '!=', 'contractuel')]")
    section = fields.Many2one('rh.section')
    code_type_fonction = fields.Char(related='type_fonction.code_type_fonction',
                                     string='Code Type Fonction', store=True)
    grille_id = fields.Many2one('rh.grille', readonly=True, compute='_compute_grille_fields')
    # description_grille = fields.Char(related='section.categorie_id.grille_id.description_grille', store=True)
    # description_grille2 = fields.Char(related='categorie_id.groupe_id.grille_id.description_grille', store=True)

    @api.depends('categorie_id')
    def _compute_categorie_fields(self):
        for rec in self:
            rec.groupe_id = rec.categorie_id.groupe_id.id if rec.categorie_id else False

    @api.depends('categorie_id','section')
    def _compute_grille_fields(self):
        for rec in self:
            if rec.groupe_id:
                rec.grille_id = rec.categorie_id.groupe_id.grille_id.id
            elif rec.section:
                rec.grille_id = rec.section.categorie_id.grille_id.id


    @api.onchange('type_fonction')
    def onchange_type_fonction(self):
        domain = []
        for rec in self:
            if rec.type_fonction:

                categorie = self.env['rh.categorie'].search([('type_fonction_id', '=', rec.type_fonction.id)])
                domain.append(('id', 'in', categorie.ids))
        return {'domain': {'categorie_id': domain}}

    @api.onchange('categorie_id')
    def onchange_categorie_id(self):
        domain = []
        for rec in self:
            if rec.categorie_id:
                section = self.env['rh.section'].search([('categorie_id', '=', rec.categorie_id.id)])
                domain.append(('id', 'in', section.ids))
        return {'domain': {'section': domain}}