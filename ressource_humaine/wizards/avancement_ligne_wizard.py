# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHAvancementLine(models.TransientModel):
    _name = 'rh.avancement.line.wizard'

    date_avancement = fields.Date()
    avancement_id = fields.Many2one('hr.avancement')
    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    code_type_fonction = fields.Char(related='employee_id.nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)

    grille_old_id = fields.Many2one('rh.grille')
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie')
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    grille_new_id = fields.Many2one('rh.grille')
    groupe_new_id = fields.Many2one('rh.groupe')
    categorie_new_id = fields.Many2one('rh.categorie', domain="[('groupe_id', '=', groupe_new_id), ('type_fonction_id', '=', type_fonction_id)]")
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon', domain="[('categorie_id', '=', categorie_new_id)]")
    categorie_superieure_new_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_new_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_new_id = fields.Many2one('rh.niveau.hierarchique')
    auto_filled_field = fields.Char(readonly=True, compute='_compute_auto_filled_field')

    grade_id = fields.Many2one('rh.grade')
    job_id = fields.Many2one('hr.job')
    date_old_avancement = fields.Date()
    date_new_avancement = fields.Date()

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    duree = fields.Integer()
    duree_lettre = fields.Selection(
    selection=[('inferieure', 'Inferieure'), ('moyen', 'Moyen'), ('superieure', 'Supérieure')])
    
    @api.depends('type_fonction_id')
    def _compute_auto_filled_field(self):
        for record in self:
            if record.type_fonction_id:
                # Perform any logic to compute the value for auto_filled_field
                auto_filled_value = "Computed Value"
                record.auto_filled_field = auto_filled_value
            else:
                record.auto_filled_field = False







