
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RHTypeFonction(models.Model):
    _name = 'rh.type.fonction'
    _rec_name = "intitule_type_fonction"



    code_type_fonction = fields.Char()
    intitule_type_fonction = fields.Char()

    def unlink(self):
        for rec in self:
            raise UserError(
                    "Vous ne pouvez pas supprimer cet enregistrement")
        return super(RHTypeFonction, self).unlink()




