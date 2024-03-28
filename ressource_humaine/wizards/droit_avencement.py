# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar
from odoo.exceptions import ValidationError




class RHDroitAvencement(models.TransientModel):
    _name = 'droit.avencement'


    date_avancement = fields.Date()
    code = fields.Char()
    boul = fields.Boolean(default=False)
    reclassement = fields.Boolean(default=False)
    sauvegarde = fields.Boolean(default=False)


    @api.multi
    def Archiver(self):
        print('glllllllllll')
        self.sauvegarde = True

    def check_avancement_date_and_sauvegarde(self):
        for wizard_record in self:
            # Check if there is a corresponding record in RHAvencementDroit with sauvegarde=True
            avencement_droit_record = self.env['rh.avencement.droit'].search([
                ('date_avancement', '=', wizard_record.date_avancement),
                ('code', '=', wizard_record.code),  # Assuming code is a field in RHAvencementDroit
                ('sauvegarde', '=', True),
            ])
            if not avencement_droit_record:
                raise ValidationError(
                    "No corresponding RHAvencementDroit record found for the given date_avancement, code, and sauvegarde=True.")

    @api.multi
    def actualiser_droit_avencement(self):
        if self.boul == False:
            avancement_ligne_droit = self.env['rh.avencement.droit'].search([])
            for record in avancement_ligne_droit:
                if record.sauvegarde == False:
                    record.unlink()

            avancement_line = self.env['hr.employee'].search(
                    [('date_avancement', '<=', self.date_avancement),('fin_relation', '=', False)],
                    order='date_avancement DESC')
            if avancement_line:
                for avance in avancement_line:
                        avancement_ligne_droit2 = self.env['rh.avencement.droit'].search([('employee_id', '=', avance.id),('date_avancement', '=', self.date_avancement)])
                        avancement_ligne_droit3 = self.env['rh.avencement.droit'].search(
                            [('employee_id', '=', avance.id), ('sauvegarde', '=', True), ('retenue', '=', True)], order='date_avancement DESC', limit=1)
                        if not avancement_ligne_droit2:
                            dateDebut_object = fields.Date.from_string(self.date_avancement)
                            dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                            difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                            if self.reclassement == False:
                                if difference >= 30 and avance.nature_travail_id.code_type_fonction == 'fonction':
                                    if avancement_ligne_droit3:
                                        if fields.Date.from_string(
                                                avancement_ligne_droit3.date_new_avancement) == fields.Date.from_string(
                                                avance.date_avancement):
                                            self.env['rh.avencement.droit'].create({
                                                'employee_id': avance.id,
                                                'type_fonction_id': avance.nature_travail_id.id,
                                                'date_avancement': self.date_avancement,
                                                'date_old_avancement': avance.date_avancement,
                                                'grade_id': avance.grade_id.id,
                                                'job_id': avance.job_id.id,
                                                'grille_old_id': avance.grille_id.id,
                                                'groupe_old_id': avance.groupe_id.id,
                                                'categorie_old_id': avance.categorie_id.id,
                                                'echelon_old_id': avance.echelon_id.id,

                                                'grille_new_id': avance.grille_id.id,
                                                'groupe_new_id': avance.groupe_id.id,
                                                'categorie_new_id': avance.categorie_id.id,
                                                'echelon_new_id': avance.echelon_id.id,
                                                'duree': 30,
                                                'duree_lettre': 'superieure',
                                                'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(avance.date_avancement),
                                                'sauvegarde': self.sauvegarde,
                                                'retenue': self.sauvegarde
                                                })

                                        else:
                                            print('employe existe')
                                    else:
                                        self.env['rh.avencement.droit'].create({
                                            'employee_id': avance.id,
                                            'type_fonction_id': avance.nature_travail_id.id,
                                            'date_avancement': self.date_avancement,
                                            'date_old_avancement': avance.date_avancement,
                                            'grade_id': avance.grade_id.id,
                                            'job_id': avance.job_id.id,
                                            'grille_old_id': avance.grille_id.id,
                                            'groupe_old_id': avance.groupe_id.id,
                                            'categorie_old_id': avance.categorie_id.id,
                                            'echelon_old_id': avance.echelon_id.id,
                                            'grille_new_id': avance.grille_id.id,
                                            'groupe_new_id': avance.groupe_id.id,
                                            'categorie_new_id': avance.categorie_id.id,
                                            'echelon_new_id': avance.echelon_id.id,
                                            'duree': 30,
                                            'duree_lettre': 'superieure',
                                            'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(
                                                avance.date_avancement),
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })

                                elif difference >= 30 and avance.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                                    if avancement_ligne_droit3:
                                        if fields.Date.from_string(
                                                avancement_ligne_droit3.date_new_avancement) == fields.Date.from_string(
                                            avance.date_avancement):
                                            self.env['rh.avencement.droit'].create({
                                                'employee_id': avance.id,
                                                'type_fonction_id': avance.nature_travail_id.id,
                                                'date_avancement': self.date_avancement,
                                                'date_old_avancement': avance.date_avancement,
                                                'grade_id': avance.grade_id.id,
                                                'job_id': avance.job_id.id,
                                                'grille_old_id': avance.grille_id.id,
                                                'categorie_old_id': avance.categorie_id.id,
                                                'section_old_id': avance.section_id.id,
                                                'echelon_old_id': avance.echelon_id.id,
                                                'grille_new_id': avance.grille_id.id,
                                                'categorie_new_id': avance.categorie_id.id,
                                                'section_new_id': avance.section_id.id,
                                                'echelon_new_id': avance.echelon_id.id,
                                                'duree': 30,
                                                'duree_lettre': 'inferieure',
                                                'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(avance.date_avancement),
                                                'sauvegarde': self.sauvegarde,
                                                'retenue': self.sauvegarde
                                                })
                                        else:
                                            print('employe existe')
                                    else:
                                        self.env['rh.avencement.droit'].create({
                                            'employee_id': avance.id,
                                            'type_fonction_id': avance.nature_travail_id.id,
                                            'date_avancement': self.date_avancement,
                                            'date_old_avancement': avance.date_avancement,
                                            'grade_id': avance.grade_id.id,
                                            'job_id': avance.job_id.id,
                                            'grille_old_id': avance.grille_id.id,
                                            'categorie_old_id': avance.categorie_id.id,
                                            'section_old_id': avance.section_id.id,
                                            'echelon_old_id': avance.echelon_id.id,
                                            'grille_new_id': avance.grille_id.id,
                                            'categorie_new_id': avance.categorie_id.id,
                                            'section_new_id': avance.section_id.id,
                                            'echelon_new_id': avance.echelon_id.id,
                                            'duree': 30,
                                            'duree_lettre': 'inferieure',
                                            'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(
                                                avance.date_avancement),
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })

                                elif difference >= 30 and avance.nature_travail_id.code_type_fonction == 'postesuperieure':
                                     print('fff')


                            else:
                                if difference >= 24 and avance.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                                    if avancement_ligne_droit3:
                                        if fields.Date.from_string(
                                                avancement_ligne_droit3.date_new_avancement) == fields.Date.from_string(
                                            avance.date_avancement):
                                            self.env['rh.avencement.droit'].create({
                                                'employee_id': avance.id,
                                                'type_fonction_id': avance.nature_travail_id.id,
                                                'date_avancement': self.date_avancement,
                                                'date_old_avancement': avance.date_avancement,
                                                'grade_id': avance.grade_id.id,
                                                'job_id': avance.job_id.id,
                                                'grille_old_id': avance.grille_id.id,
                                                'categorie_old_id': avance.categorie_id.id,
                                                'section_old_id': avance.section_id.id,
                                                'echelon_old_id': avance.echelon_id.id,
                                                'grille_new_id': avance.grille_id.id,
                                                'categorie_new_id': avance.categorie_id.id,
                                                'section_new_id': avance.section_id.id,
                                                'echelon_new_id': avance.echelon_id.id,
                                                'duree': 24,
                                                'duree_lettre': 'inferieure',
                                                'date_new_avancement': relativedelta(months=24) + fields.Date.from_string(
                                                    avance.date_avancement),
                                                'sauvegarde': self.sauvegarde,
                                                'retenue': self.sauvegarde
                                            })
                                        else:
                                            print('employe existe')
                                    else:
                                        self.env['rh.avencement.droit'].create({
                                            'employee_id': avance.id,
                                            'type_fonction_id': avance.nature_travail_id.id,
                                            'date_avancement': self.date_avancement,
                                            'date_old_avancement': avance.date_avancement,
                                            'grade_id': avance.grade_id.id,
                                            'job_id': avance.job_id.id,
                                            'grille_old_id': avance.grille_id.id,
                                            'categorie_old_id': avance.categorie_id.id,
                                            'section_old_id': avance.section_id.id,
                                            'echelon_old_id': avance.echelon_id.id,
                                            'grille_new_id': avance.grille_id.id,
                                            'categorie_new_id': avance.categorie_id.id,
                                            'section_new_id': avance.section_id.id,
                                            'echelon_new_id': avance.echelon_id.id,
                                            'duree': 24,
                                            'duree_lettre': 'inferieure',
                                            'date_new_avancement': relativedelta(months=24) + fields.Date.from_string(
                                                avance.date_avancement),
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })

            return {
                'name': 'Droit Avancement',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.avencement.droit',
                'type': 'ir.actions.act_window',
                'domain': [('date_avancement', '=', self.date_avancement),]

            }
        else:
            return {
                'name': 'Droit Avancement',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.avencement.droit',
                'type': 'ir.actions.act_window',
                'domain': [('sauvegarde', '=', True)]

            }








