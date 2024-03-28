# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RHAvancement(models.Model):
    _name = 'rh.avancement'

    date_avancement = fields.Date()
    date_signature = fields.Date()
    code = fields.Char()
    code_decision_groupe = fields.Char()
    date_decision_groupe = fields.Date()
    date_effet_decision_groupe = fields.Date()
    avancement_lines = fields.One2many('rh.avancement.line', inverse_name='avancement_id')
    avancement_lines_wizard = fields.One2many('rh.avancement.line.wizard', inverse_name='avancement_id')
    date_comission = fields.Date()
    avancement_wizard = fields.Boolean(default=True)
    choisir_commission_lines = fields.One2many('rh.avancement.commission.line', 'avancement_id')
    promotion_file_lines = fields.One2many('rh.file', 'promotion_id')
    avancement_file_lines = fields.One2many('rh.file', 'avancement_id')


    @api.model
    def create(self, vals):
        avancement = super(RHAvancement, self).create(vals)
        if avancement.avancement_lines_wizard and avancement.avancement_lines_wizard.ids:
            for rec in avancement.avancement_lines_wizard:
                if rec.employee_id.nature_travail_id.code_type_fonction == 'fonction':

                    avance_line = self.env['rh.avancement.line'].create({
                    'code': self.env['ir.sequence'].next_by_code('rh.avancement.line.sequence'),
                    'employee_id': rec.employee_id.id,
                    'type_fonction_id': rec.employee_id.nature_travail_id.id,
                    'date_old_avancement': rec.date_old_avancement,
                    'ref': rec.employee_id.ref,
                    'date_ref': rec.employee_id.date_ref,
                    'grade_id': rec.grade_id.id,
                    'job_id': rec.job_id.id,
                    'date_avancement': avancement.date_avancement,
                    'avancement_id': avancement.id,
                    'grille_old_id': rec.grille_old_id.id,
                    'groupe_old_id': rec.groupe_old_id.id,
                    'categorie_old_id': rec.categorie_old_id.id,
                    'echelon_old_id': rec.echelon_old_id.id,

                    'grille_new_id': rec.grille_new_id.id,
                    'groupe_new_id': rec.groupe_new_id.id,
                    'categorie_new_id': rec.categorie_new_id.id,
                    'echelon_new_id': rec.echelon_new_id.id,
                    'duree': rec.duree,
                    'duree_lettre': rec.duree_lettre,
                    'date_new_avancement': rec.date_new_avancement
                    })
                    employee = self.env['hr.employee'].search(
                    [('id', '=', rec.employee_id.id)])
                    employee.write({
                        'date_avancement': avance_line.date_new_avancement,
                    })
                    employee.write({
                        'groupe_id': rec.groupe_new_id.id,
                    })
                    employee.write({
                        'grille_id': rec.grille_new_id.id,
                    })
                    employee.write({
                        'categorie_id': rec.categorie_new_id.id,
                    })
                    employee.write({
                        'echelon_id': rec.echelon_new_id.id,
                    })
                    employee.write({
                        'ref': avance_line.code,
                    })
                    print('icii')
                    print(avance_line.code)
                    employee.write({
                        'date_ref': avancement.date_signature,
                    })
                    rec.employee_id.point_indiciare = rec.employee_id.echelon_id.indice_echelon
                    employee.write({
                        'point_indiciare': rec.employee_id.point_indiciare,
                    })
                    rec.employee_id.indice_minimal = rec.employee_id.categorie_id.Indice_minimal
                    employee.write({
                        'indice_minimal': rec.employee_id.indice_minimal,
                    })
                    rec.employee_id.total_indice = rec.employee_id.point_indiciare + rec.employee_id.indice_minimal
                    employee.write({
                        'total_indice': rec.employee_id.total_indice,
                    })

                    rec.employee_id.wage = rec.employee_id.indice_minimal * 45 + rec.employee_id.point_indiciare * 45
                    employee.write({
                        'wage': rec.employee_id.wage,
                    })
                elif rec.employee_id.nature_travail_id.code_type_fonction == 'fonctionsuperieure':

                    avance_line = self.env['rh.avancement.line'].create({
                        'employee_id': rec.employee_id.id,
                        'code': self.env['ir.sequence'].next_by_code('rh.avancement.line.sequence'),
                        'type_fonction_id': rec.employee_id.nature_travail_id.id,
                        'date_old_avancement': rec.date_old_avancement,
                        'ref': rec.employee_id.ref,
                        'date_ref': rec.employee_id.date_ref,
                        'grade_id': rec.grade_id.id,
                        'job_id': rec.job_id.id,
                        'date_avancement': avancement.date_avancement,
                        'avancement_id': avancement.id,
                        'grille_old_id': rec.grille_old_id.id,
                        'categorie_old_id': rec.categorie_old_id.id,
                        'section_old_id': rec.section_old_id.id,
                        'echelon_old_id': rec.echelon_old_id.id,

                        'grille_new_id': rec.grille_new_id.id,
                        'categorie_new_id': rec.categorie_new_id.id,
                        'section_new_id': rec.section_new_id.id,
                        'echelon_new_id': rec.echelon_new_id.id,
                        'duree': rec.duree,
                        'duree_lettre': rec.duree_lettre,
                        'date_new_avancement': rec.date_new_avancement
                    })
                    employee = self.env['hr.employee'].search(
                        [('id', '=', rec.employee_id.id)])
                    employee.write({
                        'date_avancement': avance_line.date_new_avancement,
                    })
                    employee.write({
                        'section_new_id': rec.section_new_id.id,
                    })
                    employee.write({
                        'grille_id': rec.grille_new_id.id,
                    })
                    employee.write({
                        'categorie_id': rec.categorie_new_id.id,
                    })
                    employee.write({
                        'echelon_id': rec.echelon_new_id.id,
                    })
                    employee.write({
                        'section_id': rec.section_new_id.id,
                    })
                    employee.write({
                        'ref': avance_line.code,
                    })
                    employee.write({
                        'date_ref': avancement.date_signature,
                    })
                    rec.employee_id.point_indiciare = rec.employee_id.echelon_id.indice_echelon
                    employee.write({
                        'point_indiciare': rec.employee_id.point_indiciare,
                    })
                    rec.employee_id.indice_base = rec.employee_id.section_id.indice_base
                    employee.write({
                        'indice_base': rec.employee_id.indice_base,
                    })
                    rec.employee_id.total_indice = rec.employee_id.section_id.indice_base + rec.employee_id.point_indiciare
                    employee.write({
                        'total_indice': rec.employee_id.total_indice,
                    })

                    rec.employee_id.wage = rec.employee_id.indice_base * 45 + rec.employee_id.point_indiciare
                    employee.write({
                        'wage': rec.employee_id.wage,
                    })
                elif rec.employee_id.nature_travail_id.code_type_fonction == 'postesuperieure':
                    print('teste')

                sequence = self.env['ir.sequence'].next_by_code('rh.avancement.sequence')
                avance_line.write({'code': sequence})
        else:
            raise UserError("Vous ne pouvez pas enregistrer une liste vide")
        return avancement

    @api.multi
    def write(self, vals):
        res = super(RHAvancement, self).write(vals)
        res1 = self.env['rh.avancement.line'].search([('avancement_id', '=', self.id)])
        for rec in res1:
            employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
            if rec.date_new_avancement == employee.date_avancement:
                employee.write({
                    'ref': rec.code,
                })
                employee.write({
                    'date_ref': self.date_signature,
                })

    @api.onchange('date_avancement')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        for rec1 in self:
            rec1.avancement_wizard = True

        domain = []
        employee = self.env['hr.employee'].search([])
        avancement_ligne_droit = self.env['rh.avancement.line.wizard'].search([])
        for record in avancement_ligne_droit:
            record.unlink()
        for rec2  in self:
            avancement_line = self.env['rh.avencement.droit'].search(
                [('date_avancement', '=', rec2.date_avancement),('sauvegarde', '=', True),('retenue', '=', True)],
                order='date_avancement desc')
        if avancement_line:
             for avance in avancement_line:
                    dateDebut_object = fields.Date.from_string(self.date_avancement)
                    dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                    difference = (
                                             dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    # difference = dateDebut_object - dateDebut_object2
                    print(avance.employee_id.id)
                    print('difference')
                    record2 = self.env['rh.avancement.line'].search(
                        [('employee_id', '=', avance.employee_id.id), ('date_avancement', '=', self.date_avancement)])
                    if not record2:
                        if avance.type_fonction_id.code_type_fonction == 'fonction':
                            self.env['rh.avancement.line.wizard'].create({
                                'employee_id': avance.employee_id.id,
                                'type_fonction_id': avance.type_fonction_id.id,
                                'date_old_avancement': avance.date_old_avancement,
                                'date_avancement': avance.date_avancement,
                                'grade_id': avance.grade_id.id,
                                'job_id': avance.job_id.id,
                                'grille_old_id': avance.grille_old_id.id,
                                'groupe_old_id': avance.groupe_old_id.id,
                                'categorie_old_id': avance.categorie_old_id.id,
                                'echelon_old_id': avance.echelon_old_id.id,
                                'grille_new_id': avance.grille_new_id.id,
                                'groupe_new_id': avance.groupe_new_id.id,
                                'categorie_new_id': avance.categorie_new_id.id,
                                'echelon_new_id': avance.echelon_new_id.id,
                                'duree': avance.duree,
                                'duree_lettre': avance.duree_lettre,
                                'date_new_avancement': avance.date_new_avancement,

                            })
                        elif avance.type_fonction_id.code_type_fonction == 'fonctionsuperieure':
                            self.env['rh.avancement.line.wizard'].create({
                                'employee_id': avance.employee_id.id,
                                'type_fonction_id': avance.type_fonction_id.id,
                                'date_old_avancement': avance.date_old_avancement,
                                'date_avancement': avance.date_avancement,
                                'grade_id': avance.grade_id.id,
                                'job_id': avance.job_id.id,
                                'grille_old_id': avance.grille_old_id.id,
                                'categorie_old_id': avance.categorie_old_id.id,
                                'section_old_id': avance.section_old_id.id,
                                'echelon_old_id': avance.echelon_old_id.id,

                                'grille_new_id': avance.grille_new_id.id,
                                'categorie_new_id': avance.categorie_new_id.id,
                                'section_new_id': avance.section_new_id.id,
                                'echelon_new_id': avance.echelon_new_id.id,
                                'duree': avance.duree,
                                'duree_lettre': avance.duree_lettre,
                                'date_new_avancement': avance.date_new_avancement,

                            })
                        elif avance.type_fonction_id.code_type_fonction == 'postesuperieure':
                            print('teste')

        self.avancement_lines_wizard = self.env['rh.avancement.line.wizard'].search([])

        return {
                'type': 'ir.actions.act_window',
                'target': 'new',
                'name': 'Avancement',
                'view_mode': 'form',
                'res_model': 'rh.avancement',
            }

    def choisir_commission(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Commission Avancement',
            'view_mode': 'form',
            'res_model': 'commission.avancement',
        }

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_droit_avancement_report').report_action(self)



class DroitAvancementReport(models.AbstractModel):
    _name = 'report.ressource_humaine.droit_avancement_report'

    @api.model
    def get_report_values(self, docids, data=None):
        avancement = self.env['rh.avancement'].browse(docids[0])

        avancement_lines = avancement.avancement_lines
        avance = []
        avance_first= []
        avance_next= []
        derniere_grille = []
        for rec in avancement_lines:
            employe_avancement_lines = self.env['rh.avancement.line'].search([('employee_id', '=', rec.employee_id.id),('date_avancement', '<=', avancement.date_avancement)],order='date_avancement desc', limit=2)
            avancement_lines_grille = self.env['rh.avancement.line'].search([('employee_id', '=', rec.employee_id.id),('date_avancement', '<=', avancement.date_avancement)],order='date_avancement desc')
            if avancement_lines_grille:
                for rec1 in avancement_lines_grille:
                    avancement_lines_grille3 = self.env['rh.avancement.line'].search(
                        [('employee_id', '=', rec.employee_id.id),
                         ('grille_old_id', '=', rec.grille_old_id.id),
                         ('date_avancement', '<=', avancement.date_avancement)], order='date_avancement desc')
                    if rec.grille_old_id.id != rec1.grille_old_id.id:
                          if not avancement_lines_grille3[-1] in derniere_grille:
                            derniere_grille.append(avancement_lines_grille3[-1])
                            print(avancement_lines_grille[0].echelon_old_id.intitule)
                if not employe_avancement_lines[-1] in derniere_grille and not avancement_lines_grille3[-1] in derniere_grille:
                    derniere_grille.append(avancement_lines_grille[-1])


            if employe_avancement_lines:
                # print(employe_avancement_lines[0])
                # print(employe_avancement_lines[1])
                # print(rec.employee_id)
                # print(employe_avancement_lines[1].employee_id)
                # print(employe_avancement_lines[1].echelon_new_id.intitule)
                if len(employe_avancement_lines) == 1:
                    avance.append(employe_avancement_lines[0])
                    avance_first.append(employe_avancement_lines[0])
                else:
                    avance.append(employe_avancement_lines[1])
                    avance_next.append(employe_avancement_lines[0])



        line_date_old_avancement = {}
        for rec in avancement_lines:
            date_old_avancement_str = rec.date_old_avancement
            if date_old_avancement_str:
                formatted_date_old_avancement = datetime.strptime(date_old_avancement_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_old_avancement[rec.id] = formatted_date_old_avancement
            else:
                line_date_old_avancement[rec.id] = ''

        line_date_old_avancement1 = {}
        for rec in avancement_lines_grille:
            date_old_avancement_str = rec.date_old_avancement
            if date_old_avancement_str:
                formatted_date_old_avancement = datetime.strptime(date_old_avancement_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_old_avancement1[rec.id] = formatted_date_old_avancement
            else:
                line_date_old_avancement1[rec.id] = ''

        line_date_ref = {}
        for rec in avancement_lines:
            date_ref_str = rec.date_ref
            if date_ref_str:
                formatted_date_ref = datetime.strptime(date_ref_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_ref[rec.id] = formatted_date_ref
            else:
                line_date_ref[rec.id] = ''

        line_date_avancement = {}
        for rec in avancement:
            date_avancement_str = rec.date_avancement
            if date_avancement_str:
                formatted_date_avancement = datetime.strptime(date_avancement_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_avancement[rec.id] = formatted_date_avancement
            else:
                line_date_avancement[rec.id] = ''

        line_date_decision_groupe = {}
        for rec in avancement:
            date_decision_groupe_str = rec.date_decision_groupe
            print('date:')

            if date_decision_groupe_str:
                formatted_date_decision_groupe = datetime.strptime(date_decision_groupe_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_decision_groupe[rec.id] = formatted_date_decision_groupe
            else:
                line_date_decision_groupe[rec.id] = ''

        line_date_effet_decision_groupe = {}
        for rec in avancement:
            date_effet_decision_groupe_str = rec.date_effet_decision_groupe
            print('date:')

            if date_decision_groupe_str:
                formatted_date_effet_decision_groupe = datetime.strptime(date_effet_decision_groupe_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_effet_decision_groupe[rec.id] = formatted_date_effet_decision_groupe
            else:
                line_date_effet_decision_groupe[rec.id] = ''

        line_date_signature = {}
        for rec in avancement:
            date_signature_str = rec.date_signature
            if date_signature_str:
                formatted_date_signature = datetime.strptime(date_signature_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_signature[rec.id] = formatted_date_signature
            else:
                line_date_signature[rec.id] = '..................'

        line_date_new_avancement = {}
        for rec in avancement_lines:
            date_new_avancement_str = rec.date_new_avancement
            if date_new_avancement_str:
                formatted_date_new_avancement = datetime.strptime(date_new_avancement_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_new_avancement[rec.id] = formatted_date_new_avancement
            else:
                line_date_new_avancement[rec.id] = ''

        line_date_code = {}
        for rec in avancement_lines:
            date_code_str = rec.employee_id.corps_id.filiere_id.date_code
            if date_code_str:
                formatted_date_code = datetime.strptime(date_code_str, "%Y-%m-%d %H:%M:%S").strftime(
                    "%d-%m-%Y")
                line_date_code[rec.id] = formatted_date_code
            else:
                line_date_code[rec.id] = ''

        report_data = {
            'avancement': avancement,
            'company': self.env.user.company_id,
            'avancement_lines': avancement_lines,
            'avancement_old': avance,
            'avance_first': avance_first,
            'avance_next': avance_next,
            'grille_old': derniere_grille,
            'line_date_old_avancement1': line_date_old_avancement1,
            'line_date_old_avancement': line_date_old_avancement,
            'line_date_ref': line_date_ref,
            'line_date_avancement': line_date_avancement,
            'line_date_decision_groupe': line_date_decision_groupe,
            'line_date_effet_decision_groupe': line_date_effet_decision_groupe,
            'line_date_signature': line_date_signature,
            'line_date_new_avancement': line_date_new_avancement,
            'line_date_code': line_date_code,
        }

        return report_data

