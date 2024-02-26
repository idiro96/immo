# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHLoi(models.Model):
    _name = 'rh.loi'
    _rec_name = 'intitule_loi'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_loi = fields.Char()
    description = fields.Text()


    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.loi.sequence') or _('New')
        result = super(RHLoi, self).create(vals)
        return result

