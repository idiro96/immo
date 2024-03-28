# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHTypeFinRelation(models.Model):
    _name = 'rh.type.fin.relation'
    _rec_name = 'description'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    description = fields.Char()
    description_fr = fields.Char()
    age_male = fields.Integer(default=60)
    age_female = fields.Integer(default=55)

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.fin.relation.sequence') or _('New')
        result = super(RHTypeFinRelation, self).create(vals)
        return result