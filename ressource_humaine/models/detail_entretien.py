# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHDetailEntretien(models.Model):
    _name = 'rh.detail.entretien'

    code_entretien = fields.Char()
    salle_entretien = fields.Integer()
    decision_recrutement = fields.Boolean()
    date_prevue_recrutement = fields.Date()
    rdv_integration = fields.Date()





