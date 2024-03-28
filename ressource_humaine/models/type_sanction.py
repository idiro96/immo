
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHTypeSanction(models.Model):
    _name = 'rh.type.sanction'
    _rec_name = "intitule_type_sanction"


    code_type_sanction = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_type_sanction = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code_type_sanction', _('New')) == _('New'):
             vals['code_type_sanction'] = self.env['ir.sequence'].next_by_code('rh.type.sanction.sequence') or _('New')
        result = super(RHTypeSanction, self).create(vals)
        return result


