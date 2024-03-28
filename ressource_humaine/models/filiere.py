# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFiliere(models.Model):
    _name = 'rh.filiere'
    _rec_name = 'intitule_filiere'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    code_group = fields.Char()
    date_code = fields.Date()
    intitule_filiere = fields.Char()
    loi_id = fields.Many2one(comodel_name='rh.loi')



    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.filiere.sequence') or _('New')
        result = super(RHFiliere, self).create(vals)
        return result

