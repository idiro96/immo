# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHSecteure(models.Model):
    _name = 'rh.corps'
    _rec_name = 'intitule_corps'


    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_corps= fields.Char()
    filiere_id = fields.Many2one(comodel_name='rh.filiere')
    loi_id = fields.Many2one(comodel_name='rh.loi')



    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.corps.sequence') or _('New')
        result = super(RHSecteure, self).create(vals)
        return result

    @api.onchange('loi_id')
    def _onchange_related_field(self):
        # This method will be called when the value of 'related_field' changes
        # Update the domain for 'field1' based on the value of 'related_field'
        print('teste')
        for rec in self:
            domain = []
            if rec.loi_id:
                print('teste')
                filiere = self.env['rh.filiere'].search([('loi_id', '=', rec.loi_id.id)])
                print(filiere)
                domain.append(('id', 'in', filiere.ids))
            else:
                domain = ''

        res = {'domain': {'filiere_id': domain}}
        print(res)
        return res