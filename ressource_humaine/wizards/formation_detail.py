# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class RHFormationDetail(models.TransientModel):
    _name = 'formation.detail'



    formation_id = fields.Many2one('rh.formation')
    employee_id_lines = fields.One2many('hr.employee', 'formation_detail_id', string="Formation Lines",
                                        default=lambda self: self._default_employees())

    date_debut_formation_line = fields.Date()
    date_fin_formation_line = fields.Date()
    groupe = fields.Selection(
        [('groupe1', 'Groupe 1'), ('groupe2', 'Groupe 2'), ('groupe3', 'Groupe 3'), ('groupe4', 'Groupe 4'),
         ('groupe5', 'Groupe 5')])

    # def detail_formation(self):
    #     record = self.env['rh.formation'].browse(self._context['active_id'])
    #     for line in self.employee_id_lines:
    #         if line.selection_employe== True:
    #             visite_medical = self.env['rh.formation.line'].create({
    #             'employee_id': line.id,
    #             'formation_id':record.id,
    #             'date_debut_formation_line':self.date_debut_formation_line,
    #             'date_fin_formation_line':self.date_debut_formation_line,
    #             'groupe': self.groupe
    #             })

    def detail_formation(self):
        record = self.env['rh.formation'].browse(self._context['active_id'])
        for line in self.employee_id_lines:
            if line.selection_employe:
                # Check if the dates fall within the absence period
                date_start = record.date_debut_formation
                date_end = record.date_fin_formation

                if not (date_start <= self.date_debut_formation_line <= date_end) or \
                        not (date_start <= self.date_fin_formation_line <= date_end):
                    raise ValidationError("la date doit étre compris dans l'intervale")

                # Check for overlapping formations for each employee
                overlapping_formations = self.env['rh.formation.line'].search([
                    ('employee_id', '=', line.id),
                    ('date_debut_formation_line', '<=', self.date_fin_formation_line),
                    ('date_fin_formation_line', '>=', self.date_debut_formation_line),
                    ('formation_id', '!=', record.id),
                ])
                if overlapping_formations:
                    raise ValidationError("vous avez sélectioner des employees en qui sont déja en formation")

                # Creating formation line
                self.env['rh.formation.line'].create({
                    'employee_id': line.id,
                    'formation_id': record.id,
                    'date_debut_formation_line': self.date_debut_formation_line,
                    'date_fin_formation_line': self.date_fin_formation_line,
                    'groupe': self.groupe
                 })

    @api.model
    def _default_employees(self):
        records = self.env['hr.employee'].search([])
        for rec in records:
            rec.selection_employe = False
        return records



