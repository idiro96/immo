# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from odoo.exceptions import UserError


class RHAvencementDroit(models.Model):
    _name = 'rh.avencement.droit'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    grille_old_id = fields.Many2one('rh.grille')
    grille_new_id = fields.Many2one('rh.grille')
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie')
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    groupe_new_id = fields.Many2one('rh.groupe',)
    categorie_new_id = fields.Many2one('rh.categorie', domain="[('groupe_id', '=', groupe_new_id)]")
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon', domain="[('categorie_id', '=', categorie_new_id)]")

    grade_id = fields.Many2one('rh.grade')
    job_id = fields.Many2one('hr.job')
    date_old_avancement = fields.Date()
    date_new_avancement = fields.Date()

    sauvegarde = fields.Boolean(Default=False)
    retenue = fields.Boolean(Default=False)
    test = fields.Char()
    date_avancement = fields.Date()
    duree = fields.Integer()
    duree_lettre = fields.Selection(selection=[('inferieure', 'Inferieure'), ('moyen', 'Moyen'), ('superieure', 'Supérieure')])
    code_type_fonction = fields.Char(related='employee_id.nature_travail_id.code_type_fonction',
                                     store=True)

    time_years = fields.Integer(compute="_compute_time", store=True)
    time_months = fields.Integer(compute="_compute_time", store=True)
    time_days = fields.Integer(compute="_compute_time", store=True)
    time_difference = fields.Char(compute="_compute_time")
    def _compute_time(self):
        for rec in self:
            if rec.date_old_avancement and rec.date_new_avancement:
                date_old_avancement = fields.Datetime.from_string(rec.date_old_avancement)
                date_new_avancement = fields.Datetime.from_string(rec.date_new_avancement)
                delta = relativedelta(date_new_avancement, date_old_avancement)

                years = delta.years
                months = delta.months
                days = delta.days

                rec.time_years = years
                rec.time_months = months
                rec.time_days = days

                # rec.time_difference = str(years) + ' annee et ' + str(months) + ' mois et ' + str(days) + 'jours'
                rec.time_difference = f"قدره {years} سنة و {months} شهر و {days} يوم"
                print(rec.time_difference)
                print('rec.time_difference')



    # @api.multi
    # def write(self, vals):
    #     res = super(RHAvencementDroit, self).write(vals)
    #     for rec in self:
    #         if rec.sauvegarde != False
    #     res1 = self.env['account.asset.asset'].search([('id', '=', self.id)])


    @api.onchange('grille_new_id')
    def _onchange_grille_new_id(self):
        # if self.grille_new_id:
        #     self.groupe_new_id = False
        #     self.categorie_new_id = False
        #     self.section_new_id = False
        #     self.echelon_new_id = False
        # if self.groupe_new_id:
        #     return {'domain': {'groupe_new_id': [('grille_id', '=', self.grille_new_id.id)]}}
        # else:
        #     return {'domain': {'categorie_new_id': [('grille_id', '=', self.grille_new_id.id)]}}
        for rec in self:
            domain = []
            if self.grille_new_id:
                self.groupe_new_id = False
                self.categorie_new_id = False
                self.section_new_id = False
                self.echelon_new_id = False
            # if self.groupe_id:
            type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.employee_id.nature_travail_id.id)])
            print(type_fonction.code_type_fonction)
            if type_fonction.code_type_fonction != 'fonctionsuperieure':
                if type_fonction.code_type_fonction == 'contractuel':
                    return {'domain': {'categorie_new_id': [('grille_id', '=', rec.grille_new_id.id),
                                                        (('type_fonction_id', '=', rec.employee_id.nature_travail_id.id))]}}
                elif type_fonction.code_type_fonction != 'contractuel':
                    return {'domain': {'groupe_new_id': [('grille_id', '=', rec.grille_new_id.id)]}}
            elif type_fonction.code_type_fonction == 'fonctionsuperieure':
                print('dfs2')
                return {'domain': {'categorie_new_id': [('grille_id', '=', rec.grille_new_id.id),
                                                    (('type_fonction_id', '=', rec.employee_id.nature_travail_id.id))]}}

    @api.multi
    def write(self, vals):
        result1 = super(RHAvencementDroit, self).write(vals)
        # record1 = self.env['rh.avancement.droit'].browse(self._context['active_ids'])
        for rec in self:
            print('ranah22')
            if rec.retenue:
                print('ranah223')
                if not rec.sauvegarde:
                    print('ranah224')
                    raise UserError("أكد أولا الحق في التقدم في الدرجة")
            record2 = self.env['rh.avancement.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_avancement', '=', rec.date_avancement)])
            if record2:
                raise UserError("مستحيل تغيير تقدم في الدرجة اللذي تم تحققه")

        return result1

    @api.multi
    def unlink(self):
        for rec in self:
            print('ranah')
            record2 = self.env['rh.avancement.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_avancement', '=', rec.date_avancement)])
            if record2:
                raise UserError(
                    "لا يمكنك من حذف تسجيل اللذي تم تحققه")
        return super(RHAvencementDroit, self).unlink()

        # endroit = self.env['invest.affectation'].search([('endroit_id', '=', self.id)])
        # if endroit:
        #     raise UserError(
        #         "Vous ne pouvez pas supprimer cet emplacement, car un bien est déja affecté à ce lieu")
        #
        # fils = self.env['invest.endroit'].search([('parent_id', '=', self.id)])
        # if fils:
        #     raise UserError(
        #         "Vous ne pouvez pas supprimer cet emplacement, car ce lieu possède des ascendants")


    @api.onchange('duree')
    def _onchange_duree(self):
        for rec in self:
            rec.date_new_avancement = relativedelta(months=rec.duree) + fields.Date.from_string(rec.date_old_avancement)
            if rec.duree == 30:
                rec.duree_lettre = 'inferieure'
            elif rec.duree == 36:
                rec.duree_lettre = 'moyen'
            else:
                rec.duree_lettre = 'superieure'

    @api.onchange('groupe_new_id')
    def _onchange_groupe_new_id(self):
        # if self.groupe_new_id:
        #     self.categorie_new_id = False
        #     self.section_new_id = False
        #     self.echelon_new_id = False
        #     return {'domain': {'categorie_new_id': [('groupe_id', '=', self.groupe_new_id.id)]}}
        # else:
        #     return {'domain': {'categorie_new_id': []}}
        for rec in self:
            domain = []
            rec.categorie_new_id = None
            if rec.groupe_new_id:
                categorie = self.env['rh.categorie'].search([('groupe_id', '=', rec.groupe_new_id.id)])
                domain.append(('id', 'in', categorie.ids))
            else:
                categorie = self.env['rh.categorie'].search([('groupe_id', '=', None)])
                domain.append(('id', 'in', categorie.ids))

        res = {'domain': {'categorie_new_id': domain}}
        print(res)
        return res

    @api.onchange('categorie_new_id')
    def _onchange_categorie_new_id(self):
        # if self.categorie_new_id:
        #     self.section_new_id = False
        #     self.echelon_new_id = False
        # if self.section_new_id :
        #     return {'domain': {'section_new_id': [('categorie_id', '=', self.categorie_new_id.id)]}}
        # else:
        #     return {'domain': {'echelon_new_id': [('categorie_id', '=', self.categorie_new_id.id)]}}
        res = None
        if self.categorie_new_id:
            self.section_new_id = False
            self.echelon_new_id = False
        for rec in self:
            domain = []
            if rec.categorie_new_id:
                echelon = self.env['rh.echelon'].search([('categorie_id', '=', rec.categorie_new_id.id)])
                section = self.env['rh.section'].search([('categorie_id', '=', rec.categorie_new_id.id)])
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.employee_id.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'contractuel':
                    print('teste')
                    # rec.indice_minimal = rec.categorie_id.Indice_minimal
                    # rec.wage = rec.indice_minimal * 45
                elif type_fonction.code_type_fonction == 'fonction':
                    domain.append(('id', 'in', echelon.ids))
                    # rec.indice_minimal = rec.categorie_id.Indice_minimal
                    res = {'domain': {'echelon_id': domain}}
                elif type_fonction.code_type_fonction == 'postesuperieure':
                    domain.append(('id', 'in', echelon.ids))
                    # rec.indice_minimal = rec.categorie_id.Indice_minimal
                    res = {'domain': {'echelon_new_id': domain}}
                else:
                    domain.append(('id', 'in', section.ids))
                    res = {'domain': {'section_new_id': domain}}

        return res
    @api.onchange('section_new_id')
    def _onchange_section_new_id(self):
        if self.section_new_id:
            self.echelon_new_id = False
            return {'domain': {'echelon_new_id': [('section', '=', self.section_new_id.id)]}}

        else:
            return {'domain': {'echelon_new_id': []}}



    @api.multi
    def print_promotion(self):
        return self.env.ref('ressource_humaine.action_hr_tableau_promotion').with_context(landscape=True).report_action(self)
