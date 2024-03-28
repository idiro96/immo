# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from odoo.exceptions import UserError


class RHCongeDroit(models.Model):
    _name = 'rh.congedroit'


    id_personnel = fields.Many2one(comodel_name='hr.employee')
    exercice_conge = fields.Char()
    nbr_jour = fields.Float()
    nbr_jour_consomme = fields.Float()
    nbr_jour_reste = fields.Float()

    @api.model
    def my_function(self):
        (print('testaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))

    @api.multi
    def unlink(self):
        for rec in self:
            raise UserError(
                    "Vous ne pouvez pas supprimer cet enregistrement")
        return super(RHCongeDroit, self).unlink()



