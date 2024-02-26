from odoo import models, fields, api, _
from itertools import groupby


class ListeNominative(models.TransientModel):
    _name = 'liste.nominative'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_liste_nominative').report_action(self)


class ListeNominativeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_nominative'

    @api.model
    def get_report_values(self, docids, data=None):
        job_supp = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'postesuperieure')])
        job_hight_org_1 = self.env['hr.job'].search(
            [('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
             ('poste_organique', '=', 'organique'), ('name', 'ilike', 'مكتب')])
        job_hight_org_2 = self.env['hr.job'].search(
            [('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
             ('poste_organique', '=', 'organique')])
        job_hight_org = job_hight_org_2 - job_hight_org_1
        job_hight_squ = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
                                                   ('poste_organique', '=', 'squelaire')])

        pleintemps_indeterminee = self.env['hr.contract'].search(
            [('type_id.code_type_contract', '=', 'pleintemps_indeterminee'),
             ('employee_id.job_id', '!=', False)])

        grouped_pleintemps_indeterminee = {}
        for contract in pleintemps_indeterminee:
            job_id = contract.job_id.id
            if job_id not in grouped_pleintemps_indeterminee:
                grouped_pleintemps_indeterminee[job_id] = contract
            else:
                if contract.create_date < grouped_pleintemps_indeterminee[job_id].create_date:
                    grouped_pleintemps_indeterminee[job_id] = contract

        first_pleintemps_indeterminee = list(grouped_pleintemps_indeterminee.values())
        print(first_pleintemps_indeterminee)

        pleintemps_determinee = self.env['hr.contract'].search(
            [('type_id.code_type_contract', '=', 'pleintemps_determinee'),
             ('employee_id.job_id', '!=', False)])

        grouped_pleintemps_determinee = {}
        for contract in pleintemps_determinee:
            job_id = contract.job_id.id
            if job_id not in grouped_pleintemps_determinee:
                grouped_pleintemps_determinee[job_id] = contract
            else:
                if contract.create_date < grouped_pleintemps_determinee[job_id].create_date:
                    grouped_pleintemps_determinee[job_id] = contract

        first_pleintemps_determinee = list(grouped_pleintemps_determinee.values())

        partiel_indeterminee = self.env['hr.contract'].search(
            [('type_id.code_type_contract', '=', 'partiel_indeterminee'),
             ('employee_id.job_id', '!=', False)])

        grouped_partiel_indeterminee = {}
        for contract in partiel_indeterminee:
            job_id = contract.job_id.id
            if job_id not in grouped_partiel_indeterminee:
                grouped_partiel_indeterminee[job_id] = contract
            else:
                if contract.create_date < grouped_partiel_indeterminee[job_id].create_date:
                    grouped_partiel_indeterminee[job_id] = contract

        first_partiel_indeterminee = list(grouped_partiel_indeterminee.values())

        partiel_determinee = self.env['hr.contract'].search(
            [('type_id.code_type_contract', '=', 'partiel_determinee'),
             ('employee_id.job_id', '!=', False)])

        grouped_partiel_determinee = {}
        for contract in partiel_determinee:
            job_id = contract.job_id.id
            if job_id not in grouped_partiel_determinee:
                grouped_partiel_determinee[job_id] = contract
            else:
                if contract.create_date < grouped_partiel_determinee[job_id].create_date:
                    grouped_partiel_determinee[job_id] = contract

        first_partiel_determinee = list(grouped_partiel_determinee.values())

        grade_proff = self.env['rh.grade'].search([('intitule_grade', 'ilike', 'أستاذ')])
        grade_a = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة أ')])
        grade_a_excluded = grade_a - grade_proff
        grade_b = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة ب')])
        grade_c = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة ج')])
        grade_d = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة د')])
        grade_d_2 = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة د'),
                                                 ('corps_id.intitule_corps', 'ilike', 'مهن')])
        grade_contract = self.env['rh.grade'].search([('corps_id.intitule_corps', 'ilike', 'متعاقد')])
        grade_d_1 = grade_d - grade_d_2 - grade_contract

        report_data = {
            'company': self.env.user.company_id,
            'job_supp': job_supp,
            'job_hight_org_1': job_hight_org_1,
            'job_hight_org': job_hight_org,
            'job_hight_squ': job_hight_squ,
            'first_pleintemps_indeterminee': first_pleintemps_indeterminee,
            'first_pleintemps_determinee': first_pleintemps_determinee,
            'first_partiel_indeterminee': first_partiel_indeterminee,
            'first_partiel_determinee': first_partiel_determinee,
            'grade_proff': grade_proff,
            'grade_a_excluded': grade_a_excluded,
            'grade_b': grade_b,
            'grade_c': grade_c,
            'grade_d_1': grade_d_1,
            'grade_d_2': grade_d_2,
            'grade_contract': grade_contract,
        }

        return report_data
