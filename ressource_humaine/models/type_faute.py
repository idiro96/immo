

from odoo import models, fields, api, _



class RHTypeFaute(models.Model):
    _name = 'rh.type.faute'
    _rec_name = 'intitule_type_faute'


    code_type_faute = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_type_faute = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code_type_faute', _('New')) == _('New'):
             vals['code_type_faute'] = self.env['ir.sequence'].next_by_code('rh.type.faute.sequence') or _('New')
        result = super(RHTypeFaute, self).create(vals)
        return result


