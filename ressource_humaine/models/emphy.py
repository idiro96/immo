# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _




class RHEmphy(models.Model):
    _name = 'rh.emphy'
    _rec_name = 'intitule_emphy'


    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_emphy = fields.Char()



    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.emphy.sequence') or _('New')
        result = super(RHEmphy, self).create(vals)
        return result

