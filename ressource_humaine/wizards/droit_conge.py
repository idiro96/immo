# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class RHDroitConge(models.TransientModel):
    _name = 'droit.conge'

    boul = fields.Boolean(default=True)


    @api.multi
    def actualiserDroitConge(self):
        if self.boul == False:
            liste_emploiyee = self.env['hr.employee'].search([('date_entrer','!=',None),('date_fin_relation', '=', False)])
            for empl in liste_emploiyee:

                days_off = 0
                current_date = datetime.now().date()
                current_date2 = datetime.now().date()

                entrer_date1 = empl.date_entrer
                print(entrer_date1)
                entrer_date2 = empl.date_entrer
                dateDebut_object = fields.Date.from_string(entrer_date1)
                jour = datetime.strptime(entrer_date1, '%Y-%m-%d').day
                mois = datetime.strptime(entrer_date1, '%Y-%m-%d').month
                year = datetime.strptime(entrer_date1, '%Y-%m-%d').year


                debut_annee = date(dateDebut_object.year, mois, jour)
                year_current = current_date.year
                current_date = dateDebut_object
                while current_date <= current_date2:


                    if mois >= 7 and mois <= 12:
                        year = year
                        year_suivant = year + 1
                    else:
                            year_suivant = year
                            year = year - 1


                    first_date = date(year, 7, 1)
                    second_date = date(year_suivant, 6, 30)

                    if current_date <=second_date:
                        print('passer')


                    else:
                        mois = current_date.month
                        year = current_date.year
                        if mois >= 7 and mois <= 12:
                            year = year
                            year_suivant = year + 1
                        else:
                            year = year - 1
                            year_suivant = year + 1


                    # anne_encours = str(year)  + '/' + str(year_suivant)
                    anne_encours = str(year) + '/' + str(year_suivant)

                    conge_existe = self.env['rh.congedroit'].search(
                            [('exercice_conge', '=', anne_encours), ('id_personnel', '=', empl.id)])

                    if conge_existe:
                                days_off = conge_existe.nbr_jour
                                print("exercice existe déja")
                                month_now = current_date.month
                                print('ra')
                                print(current_date)
                                print(month_now)
                                print(month_now)
                                print(conge_existe)
                                conge_existe_month = self.env['rh.conge_droit_month'].search([('id_conge_droit', '=', conge_existe.id),('month', '=', month_now)])
                                print(conge_existe_month)

                                if not conge_existe_month:
                                        days_off = days_off + 2.5
                                        conge_existe.write({'nbr_jour': days_off})
                                        conge_existe.write({'nbr_jour_reste': days_off})
                                        conge_droit_month_new = self.env['rh.conge_droit_month'].create({
                                                            'id_conge_droit': conge_existe.id,
                                                            'month': month_now,
                                                        })
                                        print('rabah')

                    else:

                        if ((jour > 15) and (current_date == debut_annee)):
                            days_off = 0

                        else:
                            days_off = 2.5


                        conge_droit2 = self.env['rh.congedroit'].create({
                                            'id_personnel': empl.id,
                                            'exercice_conge': anne_encours,
                                            'nbr_jour': days_off,
                                            'nbr_jour_consomme': 0,
                                            'nbr_jour_reste': days_off,
                                        })

                        conge_droit_month_new = self.env['rh.conge_droit_month'].create({
                            'id_conge_droit': conge_droit2.id,
                            'month': mois,
                        })


                    res = calendar.monthrange(current_date.year, current_date.month)
                    day = res[1]
                    current_date = current_date + relativedelta(day=day)
                    current_date_mois = current_date.month
                    current_date_year = current_date.year
                    current_date = date(current_date_year, current_date_mois, 15)
                    current_date = relativedelta(months=1) + current_date


                conge_empl_total = self.env['rh.congedroit'].search(
                    [('id_personnel', '=', empl.id)])
                jour_reste = 0
                for cong in conge_empl_total:
                    jour_reste = cong.nbr_jour_reste + jour_reste
                empl.write({'days_off': jour_reste})
            current_date2 = datetime.now().date()
            mois2 = current_date2.month
            year2 = current_date2.year
            if mois2 >= 7 and mois2 <= 12:
                year2 = year2
                year_suivant2 = year2 + 1
            else:
                year2 = year2 - 1
                year_suivant2 = year2 + 1

            anne_encours2 = str(year2) + '/' + str(year_suivant2)
            year3 = year2 - 1
            year_suivant3 = year_suivant2 - 1
            anne_encours3 = str(year3) + '/' + str(year_suivant3)
            year4 = year3 - 1
            year_suivant4 = year_suivant3 - 1
            anne_encours4 = str(year4) + '/' + str(year_suivant4)
            return {
                'name': 'Droit Conge',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.congedroit',
                'type': 'ir.actions.act_window',
                'domain': ['|', ('exercice_conge', '=', anne_encours2), '|', ('exercice_conge', '=', anne_encours3),
                           ('exercice_conge', '=', anne_encours4)],

            }
        else:
            current_date2 = datetime.now().date()
            mois2 = current_date2.month
            year2 = current_date2.year
            if mois2 >= 7 and mois2 <= 12:
                year2 = year2
                year_suivant2 = year2 + 1
            else:
                year2 = year2 - 1
                year_suivant2 = year2 + 1

            anne_encours2 = str(year2) + '/' + str(year_suivant2)
            year3 = year2-1
            year_suivant3 = year_suivant2-1
            anne_encours3 = str(year3) + '/' + str(year_suivant3)
            year4 = year3 - 1
            year_suivant4 = year_suivant3 - 1
            anne_encours4 = str(year4) + '/' + str(year_suivant4)
            return {
                'name': 'Droit Conge',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.congedroit',
                'type': 'ir.actions.act_window',
                'domain': ['|',('exercice_conge', '=',anne_encours2),'|',('exercice_conge', '=',anne_encours3),('exercice_conge', '=',anne_encours4)],

            }







