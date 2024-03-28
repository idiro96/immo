# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFormateur(models.Model):
    _name = 'rh.formateur'

    code_formateur = fields.Char()
    nom_formateur = fields.Char()
    prenom_formateur = fields.Char()
    adresse_formateur = fields.Char()
    tel_formateur = fields.Char()
    email_formateur = fields.Char()




