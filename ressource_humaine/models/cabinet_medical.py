# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHCabinetMedical(models.Model):
    _name = 'rh.cabinet.medical'
    _rec_name = 'raison_social'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    raison_social = fields.Char()
    nif_cabinet = fields.Char()
    nis_cabinet = fields.Char()
    num_article = fields.Char()
    adress = fields.Char()
    contact = fields.Char()
    rc = fields.Char()
    cabinet_medicale_file_lines = fields.One2many('rh.file', 'cabinet_medicale_id')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.cabinet.medical.sequence') or _('New')
        result = super(RHCabinetMedical, self).create(vals)
        return result
