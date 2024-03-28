# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError, UserError

from babel.dates import format_date, format_datetime
import logging
import calendar
import time


class HrEmployeInherited(models.Model):
    _inherit = "hr.employee"

    # name = fields.Char(string="Employee Tag", required=True, compute='_compute_nom')
    handicape = fields.Boolean(default=False)
    promotion_dix = fields.Boolean(default=False)
    chef_bureau = fields.Boolean(default=False)
    niveau_hirerachique_chef_Bureau = fields.Many2one('rh.niveau.hierarchique.chef.bureau')
    service_militaire = fields.Boolean(default=False)
    fin_relation = fields.Boolean(default=False)
    date_fin_relation = fields.Date()
    date_debut_emploi = fields.Date()
    numero_securite_social = fields.Char()
    ref_promotion = fields.Char()
    date_ref_promotion = fields.Date()
    prenom_pere = fields.Char()
    nom_mere = fields.Char()
    prenom_mere = fields.Char()
    nom_fr = fields.Char()
    prenom_fr = fields.Char()
    annee_travail = fields.Float()
    date_entrer = fields.Date()
    date_job_id = fields.Date()
    date_reintegration = fields.Date()
    activite_conjoint = fields.Boolean(default=False)
    visite_medical_detaille_id = fields.Many2one('ressource_humaine.visite.medical.detaille')
    commission_avancement_id = fields.Many2one('ressource_humaine.commission.avancement')
    commission_promotion_id = fields.Many2one('ressource_humaine.commission_promotion')
    formation_detail_id = fields.Many2one('ressource_humaine.formation.detail')
    selection_employe = fields.Boolean('Sélection', default=False)
    # days_off = fields.Float(string='Total Days Off', store=True)
    wage = fields.Float(store=True)
    code_type_fonction = fields.Char(related='nature_travail_id.code_type_fonction', store=True)
    # days_off = fields.Float(compute='_compute_days_off', store=True, translate=True)
    type_id = fields.Many2one('hr.contract.type')
    # days_off = fields.Float(compute='_compute_days_off', store=True, translate=True)
    days_off = fields.Float(store=True)
    jour_sup = fields.Float(store=True)

    corps_id = fields.Many2one('rh.corps')
    grade_id = fields.Many2one('rh.grade')
    date_grade = fields.Date(translate=False, lang='fr_FR', )
    promotion_lines = fields.One2many('rh.promotion.line', inverse_name='employee_id')
    avancement_lines = fields.One2many('rh.avancement.line', inverse_name='employee_id')
    nature_travail_id = fields.Many2one('rh.type.fonction')
    position_statutaire = fields.Selection([('activite', 'Activite'),
                                            ('detachement', 'Detachement'),
                                            ('horscadre', 'Horscadre'), ('miseendisponibilite', 'Miseendisponibilite'),
                                            ('servicenationale', 'Servicenationale'), ],
                                           readonly=False, default='activite')
    methode_embauche = fields.Selection([('recrutement', 'Recrutement'),
                                         ('transfert', 'Transfert'),
                                         ('detachement', 'Detachement'), ],
                                        readonly=False, default='recrutement')
    ancienne_etablissement = fields.Char()
    nom_ar = fields.Char()
    prenom_ar = fields.Char()
    ancien_corps_id = fields.Many2one('rh.corps')
    ancien_grade_id = fields.Many2one('rh.grade')
    date_ancien_grade = fields.Date()
    nature_handicap = fields.Selection([('audio', 'Audio'),
                                        ('visuel', 'Visuel'),
                                        ('cinetique', 'Cinetique')],
                                       readonly=False, default='audio')
    taux_handicap = fields.Float()
    corps_visible = fields.Boolean(default=True)
    gender = fields.Selection(selection=[('male', 'Masculin'), ('female', 'Féminin')], readonly=False, required=True)
    nomination = fields.Selection(
        selection=[('satagiaire', 'Satagiaire'), ('nomination', 'Titulaire'), ('contractuel', 'Contractuel')],
        readonly=False, required=True)
    place_of_birth_fr = fields.Char('Lieu de naissance', groups="hr.group_hr_user", required=True)
    # place_of_birth_fr = fields.Char('Lieu de naissance', groups="hr.group_hr_user")
    grille_id = fields.Many2one('rh.grille', readonly=False)
    groupe_id = fields.Many2one('rh.groupe', readonly=False)
    point_indiciare = fields.Integer()
    indice_minimal = fields.Integer(store=True)
    indice_base = fields.Integer(store=True, default=0)
    total_indice = fields.Integer(store=True)
    bonification_indiciaire = fields.Integer(store=True)
    categorie_id = fields.Many2one('rh.categorie')
    categorie_superieure_id = fields.Many2one('rh.categorie.superieure')
    echelon_id = fields.Many2one('rh.echelon')
    niveau_hierarchique_id = fields.Many2one('rh.niveau.hierarchique')
    section_id = fields.Many2one('rh.section')
    section_superieure_id = fields.Many2one('rh.section.superieure')
    # grille_id = fields.Many2one('rh.grille')
    # code_type_fonction = fields.Char(related='nature_travail_id.code_type_fonction',
    #                                  string='Code Type Fonction', store=True)
    date_avancement = fields.Date()
    ref = fields.Char()
    date_ref = fields.Date()
    formation_file_lines = fields.One2many('rh.file', 'employee_id')
    address_perso = fields.Text()
    planning_choix_id = fields.Many2one('ressource_humaine.choisir.planning')
    emphy_id = fields.Many2one('rh.emphy')
    num_national = fields.Char(help="Il s'agit du numéro d'identité nationale de l'employé")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single')
    wage_range = fields.Selection([
        ('low', '15000-30000'),
        ('medium', '30000-50000'),
        ('high', '50000-100000'),
        ('very_high', '100000+')
    ], compute='_compute_wage_range', store=True)

    @api.depends('wage')
    def _compute_wage_range(self):
        for rec in self:
            if rec.wage < 30000:
                rec.wage_range = 'low'
            elif 30000 <= rec.wage < 50000:
                rec.wage_range = 'medium'
            elif 50000 <= rec.wage < 100000:
                rec.wage_range = 'high'
            else:
                rec.wage_range = 'very_high'

    @api.constrains('jour_sup')
    def _check_jour_sup_max_value(self):
        max_value = 12.0
        for record in self:
            if record.jour_sup > max_value:
                raise ValidationError('The maximum value for jour_sup is 12.0')

    # @api.depends('nom_ar', 'prenom_ar')
    # def _compute_nom(self):
    #     print('employee.name')
    #     for employee in self:
    #         print('employee.name')
    #         if employee.nom_ar != '' and employee.prenom_ar != '':
    #             print('employee.name')
    #             print(employee.name)
    #             employee.name = employee.nom_ar + ' ' + employee.prenom_ar
    #             print(employee.name)

    @api.depends('birthday')
    def calculer_age_employee(self):
        for emp in self:
            age = 0
            if emp.birthday:
                date_naiss = datetime.strptime(emp.birthday, '%Y-%m-%d').date()
                aujourdhui = date.today()
                age = aujourdhui.year - date_naiss.year - (
                        (aujourdhui.month, aujourdhui.day) < (date_naiss.month, date_naiss.day))
            emp.age_employee = age

    age_employee = fields.Integer(string="Age", compute='calculer_age_employee', store=True)

    age_range = fields.Selection([
        ('low', '20-30'),
        ('medium', '30-40'),
        ('high', '40-50'),
        ('very_high', '50+')
    ], compute='_compute_age_range', store=True, selection_sort=False)

    @api.depends('age_employee')
    def _compute_age_range(self):
        for rec in self:
            if rec.age_employee < 30:
                rec.age_range = 'low'
            elif 30 <= rec.age_employee < 40:
                rec.age_range = 'medium'
            elif 40 <= rec.age_employee < 50:
                rec.age_range = 'high'
            else:
                rec.age_range = 'very_high'

    @api.depends('date_entrer')
    def _compute_experience(self):
        for employee in self:
            if employee.date_entrer:
                date_entrer = fields.Datetime.from_string(employee.date_entrer)
                date_today = datetime.now().strftime('%Y-%m-%d')
                date_today = fields.Datetime.from_string(date_today)
                delta = relativedelta(date_today, date_entrer)

                years = delta.years
                months = delta.months
                days = delta.days

                employee.experience_years = years
                employee.experience_months = months
                employee.experience_days = days

    experience_years = fields.Integer(compute="_compute_experience", store=True)
    experience_months = fields.Integer(compute="_compute_experience", store=True)
    experience_days = fields.Integer(compute="_compute_experience", store=True)

    @api.onchange('grille_id')
    def _onchange_grille_id(self):
        for rec in self:
            domain = []
            if self.grille_id:
                self.groupe_id = False
                self.categorie_id = False
                self.section_id = False
                self.echelon_id = False
            # if self.groupe_id:
            type_fonction = self.env['rh.type.fonction'].search([('id', '=', self.nature_travail_id.id)])
            print(type_fonction.code_type_fonction)
            if type_fonction.code_type_fonction != 'fonctionsuperieure':
                if type_fonction.code_type_fonction == 'contractuel':
                    return {'domain': {'categorie_id': [('grille_id', '=', self.grille_id.id),(('type_fonction_id', '=', self.nature_travail_id.id))]}}
                elif type_fonction.code_type_fonction != 'contractuel':
                    return {'domain': {'groupe_id': [('grille_id', '=', self.grille_id.id)]}}
            elif type_fonction.code_type_fonction == 'fonctionsuperieure':
                print('dfs2')
                return {'domain': {'categorie_id': [('grille_id', '=', self.grille_id.id),(('type_fonction_id', '=', self.nature_travail_id.id))]}}

    # @api.onchange('groupe_id')
    # def _onchange_groupe_id(self):
    #     if self.groupe_id:
    #         self.categorie_id = False
    #         self.section_id = False
    #         self.echelon_id = False
    #         return {'domain': {'categorie_id': [('groupe_id', '=', self.groupe_id.id)]}}
    #     else:
    #         return {'domain': {'categorie_id': []}}

    @api.onchange('groupe_id')
    def onchange_groupe(self):
        for rec in self:
            domain = []
            self.categorie_id = None
            if rec.groupe_id:
                categorie = self.env['rh.categorie'].search([('groupe_id', '=', rec.groupe_id.id)])
                domain.append(('id', 'in', categorie.ids))
            else:
                categorie = self.env['rh.categorie'].search([('groupe_id', '=', None)])
                domain.append(('id', 'in', categorie.ids))

        res = {'domain': {'categorie_id': domain}}
        print(res)
        return res

    @api.onchange('categorie_id')
    def onchange_categorie(self):
        res = None
        if self.categorie_id:
            if self.grille_id:
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', self.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'contractuel':
                    if self.categorie_id.grille_id.id != self.grille_id.id:
                        self.categorie_id = None
                elif type_fonction.code_type_fonction == 'fonction':
                    if self.groupe_id:
                        if self.categorie_id.groupe_id.id != self.groupe_id.id:
                            self.categorie_id = None
                elif type_fonction.code_type_fonction == 'postesuperieure':
                    if self.groupe_id:
                        if self.categorie_id.groupe_id.id != self.groupe_id.id:
                            self.categorie_id = None
                elif type_fonction.code_type_fonction == 'fonctionsuperieure':
                    if self.categorie_id.grille_id.id != self.grille_id.id:
                        self.categorie_id = None

            self.section_id = False
            self.echelon_id = False
        print('rabah3')
        for rec in self:
            domain = []
            if rec.categorie_id:
                echelon = self.env['rh.echelon'].search([('categorie_id', '=', rec.categorie_id.id)])
                section = self.env['rh.section'].search([('categorie_id', '=', rec.categorie_id.id)])
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'contractuel':
                    self.indice_minimal = rec.categorie_id.Indice_minimal
                    self.wage = rec.indice_minimal * 45
                    self.point_indiciare = 0
                    self.indice_base = 0
                    self.total_indice = rec.indice_minimal
                elif type_fonction.code_type_fonction == 'fonction':
                    rec.total_indice = rec.indice_minimal + rec.point_indiciare
                    domain.append(('id', 'in', echelon.ids))
                    self.indice_base = 0
                    rec.indice_minimal = rec.categorie_id.Indice_minimal
                    res = {'domain': {'echelon_id': domain}}
                elif type_fonction.code_type_fonction == 'postesuperieure':
                    rec.total_indice = rec.indice_minimal + rec.point_indiciare
                    domain.append(('id', 'in', echelon.ids))
                    self.indice_base = 0
                    rec.indice_minimal = rec.categorie_id.Indice_minimal
                    res = {'domain': {'echelon_id': domain}}
                else:
                    domain.append(('id', 'in', section.ids))
                    res = {'domain': {'section_id': domain}}
                    self.total_indice = rec.indice_base + rec.point_indiciare

        return res

    @api.onchange('section_id')
    def onchange_section(self):
        self.total_indice = self.indice_base + self.indice_minimal + self.point_indiciare
        domain = []
        res = None
        if self.section_id:
            if self.categorie_id:
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', self.nature_travail_id.id)])
                if self.section_id.categorie_id.id != self.categorie_id.id:
                    self.section_id = None
            self.echelon_id = False
        for rec in self:
            if rec.section_id:
                rec.indice_base = rec.section_id.indice_base
                echelon = self.env['rh.echelon'].search([('section', '=', rec.section_id.id)])
                domain.append(('id', 'in', echelon.ids))
                self.point_indiciare = 0
                self.indice_minimal = 0
                rec.indice_minimal = rec.categorie_id.Indice_minimal
                res = {'domain': {'echelon_id': domain}}
                print('hello')
                print(echelon)
                self.total_indice = rec.indice_base + rec.point_indiciare
        return res

    @api.onchange('niveau_hierarchique_id')
    def onchange_niveau_hierarchique(self):
        for rec in self:
            if rec.niveau_hierarchique_id:
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'postesuperieure':
                    rec.bonification_indiciaire = rec.niveau_hierarchique_id.bonification_indiciaire
                    rec.wage = (rec.indice_minimal * 45 + rec.point_indiciare * 45) + rec.bonification_indiciaire

    @api.onchange('echelon_id')
    def onchange_echelon(self):
        # self.total_indice = self.indice_base + self.indice_minimal + self.point_indiciare
        for rec in self:
            domain = []
            if rec.echelon_id:
                echelon = self.env['rh.echelon'].search([('id', '=', rec.echelon_id.id)])
                section = echelon.section
                if rec.section_id:
                    if section.id != rec.section_id.id:
                        rec.echelon_id = None
                else:
                    if rec.echelon_id.categorie_id.id != rec.categorie_id.id:
                        rec.echelon_id = None
            if rec.echelon_id:
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'postesuperieure':
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                    rec.total_indice = rec.indice_minimal + rec.point_indiciare
                elif type_fonction.code_type_fonction == 'fonction':
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                    rec.wage = rec.indice_minimal * 45 + rec.point_indiciare * 45
                    self.total_indice = rec.indice_minimal + rec.point_indiciare
                else:
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                    rec.wage = rec.indice_base * 45 + rec.point_indiciare
                    self.total_indice = rec.indice_base + rec.point_indiciare

    @api.onchange('niveau_hirerachique_chef_Bureau')
    def onchange_niveau_hirerachique_chef_Bureau(self):
        for rec in self:
            rec.point_indiciare = rec.echelon_id.indice_echelon
            rec.bonification_indiciaire = rec.niveau_hirerachique_chef_Bureau.bonification_indiciaire
            rec.wage = (rec.indice_minimal * 45 + rec.point_indiciare * 45) + rec.niveau_hirerachique_chef_Bureau.bonification_indiciaire

    @api.onchange('nature_travail_id')
    def _onchange_related_field_filier(self):
        print('teste')
        for rec in self:
            domain = []
            if rec.nature_travail_id:
                rec.corps_id = False
                rec.grade_id = False
                if rec.nature_travail_id.code_type_fonction == 'contractuel':
                    corps_visible = False
                    jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                    domain.append(('id', 'in', jobs.ids))
                elif rec.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                    corps_visible = True
                    print('teste')
                    jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                    domain.append(('id', 'in', jobs.ids))
                elif rec.nature_travail_id.code_type_fonction == 'postesuperieure':
                    corps_visible = True
                    print('teste')
                    jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                    domain.append(('id', 'in', jobs.ids))
                else:
                    jobs = None
                    domain = None
            else:
                domain = ''

        res = {'domain': {'job_id': domain}}
        print(res)
        return res

    @api.onchange('corps_id')
    def _onchange_corps(self):
        print('teste')
        for rec in self:
            rec.grade_id = False
            domain = []
            if rec.corps_id:
                print('teste')
                corps = self.env['rh.grade'].search([('corps_id', '=', rec.corps_id.id)])
                domain.append(('id', 'in', corps.ids))
            else:
                domain = ''

        res = {'domain': {'grade_id': domain}}
        print(res)
        return res


