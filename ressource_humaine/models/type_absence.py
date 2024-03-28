
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHTypeAbsence(models.Model):
    _name = 'rh.type.absence'
    _rec_name = "intitule_type_absence"



    code_type_absence = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_type_absence = fields.Char()




