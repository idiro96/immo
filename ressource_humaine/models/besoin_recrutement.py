# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHBesoinRecrutement(models.Model):
    _name = 'rh.besoin.recrutement'

    motif_recrutement = fields.Char()
    exercice_recrutement = fields.Char()
    budget_alloue_recrutement = fields.Float()
    echeance_contrat = fields.Integer()
    annee_experience = fields.Integer()
    lieu_travail = fields.Char()
    deplacement_provisoire = fields.Boolean()
    autres_aspects = fields.Char()
    date_entrer_prevue = fields.Date()









