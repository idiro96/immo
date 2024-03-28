# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHFormation(models.Model):
    _name = 'rh.formation'
    _rec_name = 'intitule_formation'

    code_for = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_formation = fields.Char()
    date_debut_formation = fields.Date()
    date_fin_formation = fields.Date()
    lieu_formation = fields.Char()
    salle_formation = fields.Char()
    budget_allouee_formation = fields.Float()
    type_formation_id = fields.Many2one('rh.type.formation')
    organisme_id = fields.Many2one('rh.organisme')
    formation_lines = fields.One2many('rh.formation.line', inverse_name='formation_id')
    formation_absence = fields.One2many('rh.absence.formation', inverse_name='formation_id')
    formation_file_lines = fields.One2many('rh.file', 'formation_id')
    state = fields.Selection([('draft', 'Brouillon'),
                              ('confirm', 'Validé'),],
                               readonly=True,default='draft')

    def unlink(self):
        for rec in self:
            if rec.state in ['confirm']:
                raise ValidationError('You cannot delete a record that is confirmed or refused.')
        return super(RHFormation, self).unlink()
    def action_confirm(self):
        for rec in self:
            rec.state='confirm'


    def formation_detail_wizard(self):
        return {
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name': 'تفاصيل التكوين',
        'view_mode': 'form',
        'res_model': 'formation.detail',
        }


    @api.model
    def create(self, vals):
        if vals.get('code_for', _('New')) == _('New'):
             vals['code_for'] = self.env['ir.sequence'].next_by_code('rh.formation.sequence') or _('New')
        result = super(RHFormation, self).create(vals)
        return result


    @api.constrains('date_debut_formation', 'date_fin_formation', 'formation_lines')
    def _check_contract_overlap(self):
        for formation in self:
            for line in formation.formation_lines:
                employee = line.employee_id
                date_start = line.date_debut_formation_line
                date_end = line.date_fin_formation_line

                if not (formation.date_debut_formation <= date_start <= formation.date_fin_formation) or \
                        not (formation.date_debut_formation <= date_end <= formation.date_fin_formation):
                    raise ValidationError("la date doit étre compris dans l'intervale")

                # Check for overlapping formations for each employee
                overlapping_formations = self.search([
                    ('formation_lines.employee_id', '=', employee.id),
                    ('formation_lines.date_debut_formation_line', '<=', date_end),
                    ('formation_lines.date_fin_formation_line', '>=', date_start),
                    ('id', '!=', formation.id),
                ])
                if overlapping_formations:
                    raise ValidationError("vous avez sélectioner des employees en qui sont déja en formation")




    # @api.constrains('formation_lines')
    # def _check_contract_overlap(self):
    #     for formation in self:
    #         for line in formation.formation_lines:
    #             employee = line.employee_id
    #             date_start = line.date_debut_formation_line
    #             date_end = line.date_fin_formation_line
    #
    #             overlapping_formations = self.search([
    #                 ('formation_lines.employee_id', '=', employee.id),
    #                 ('formation_lines.date_debut_formation_line', '<=', date_end),
    #                 ('formation_lines.date_fin_formation_line', '>=', date_start),
    #                 ('id', '!=', formation.id),
    #             ])
    #             if overlapping_formations:
    #                 raise ValidationError("vous avez sélectioner des employees en qui sont déja en formation")

