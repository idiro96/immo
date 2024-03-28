# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _



class RHAvancementLine(models.Model):
    _name = 'rh.avancement.line'

    date_avancement = fields.Date()
    code = fields.Char(readonly=False, default=lambda self: self.env['ir.sequence'].next_by_code('rh.avancement.line.sequence'))
    ref = fields.Char()
    date_ref = fields.Date()
    avancement_id = fields.Many2one('rh.avancement')
    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
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
    categorie_new_id = fields.Many2one('rh.categorie')
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon')
    categorie_superieure_new_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_new_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_new_id = fields.Many2one('rh.niveau.hierarchique')

    grade_id = fields.Many2one('rh.grade')
    job_id = fields.Many2one('hr.job')
    date_old_avancement = fields.Date()
    date_new_avancement = fields.Date()
    duree = fields.Integer()
    duree_lettre = fields.Selection(
        selection=[('inferieure', 'Inferieure'), ('moyen', 'Moyen'), ('superieure', 'Supérieure')])

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()

    avancement_line_file_line = fields.Binary()

    @api.depends('date_new_avancement', 'avancement_id.date_avancement')
    def _compute_time(self):
        for rec in self:
            if rec.date_new_avancement and rec.avancement_id.date_avancement:
                date_new_avancement = fields.Datetime.from_string(rec.date_new_avancement)
                date_avancement = fields.Datetime.from_string(rec.avancement_id.date_avancement)
                delta = relativedelta(date_avancement, date_new_avancement)

                years = delta.years
                months = delta.months
                days = delta.days

                rec.time_years = years
                rec.time_months = months
                rec.time_days = days

    time_years = fields.Integer(compute="_compute_time", store=True)
    time_months = fields.Integer(compute="_compute_time", store=True)
    time_days = fields.Integer(compute="_compute_time", store=True)





