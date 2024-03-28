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
        supp_employees = []
        for job in job_supp:
            employees = self.env['hr.employee'].search(
                [('job_id', '=', job.id), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            supp_employees.append({'job': job, 'employees': employees})

        job_hight_org_1 = self.env['hr.job'].search(
            [('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
             ('poste_organique', '=', 'organique'), ('name', 'ilike', 'مكتب')])
        hight_org_1_employees = []
        for job in job_hight_org_1:
            employees = self.env['hr.employee'].search(
                [('job_id', '=', job.id), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            hight_org_1_employees.append({'job': job, 'employees': employees})

        job_hight_org_2 = self.env['hr.job'].search(
            [('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
             ('poste_organique', '=', 'organique')])

        job_hight_org = job_hight_org_2 - job_hight_org_1
        hight_org_employees = []
        for job in job_hight_org:
            employees = self.env['hr.employee'].search(
                [('job_id', '=', job.id), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            hight_org_employees.append({'job': job, 'employees': employees})

        job_hight_squ = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
                                                   ('poste_organique', '=', 'squelaire')])
        hight_squ_employees = []
        for job in job_hight_squ:
            employees = self.env['hr.employee'].search(
                [('job_id', '=', job.id), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            hight_squ_employees.append({'job': job, 'employees': employees})

        grade_proff = self.env['rh.grade'].search([('intitule_grade', 'ilike', 'أستاذ')])
        proff_employees = []
        for grade in grade_proff:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            proff_employees.append({'grade': grade, 'employees': employees})
        proff_employees.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_a = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة أ')])
        grade_a_excluded = grade_a - grade_proff
        grade_a_excluded_employees = []
        for grade in grade_a_excluded:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            grade_a_excluded_employees.append({'grade': grade, 'employees': employees})
        grade_a_excluded_employees.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_b = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة ب')])
        grade_b_employees = []
        for grade in grade_b:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            grade_b_employees.append({'grade': grade, 'employees': employees})
        grade_b_employees.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_c = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة ج')])
        grade_c_employees = []
        for grade in grade_c:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            grade_c_employees.append({'grade': grade, 'employees': employees})
        grade_c_employees.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_d = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة د')])
        grade_d_2 = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة د'),
                                                 ('corps_id.intitule_corps', 'ilike', 'مهن')])
        grade_d_2_employees = []
        for grade in grade_d_2:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            grade_d_2_employees.append({'grade': grade, 'employees': employees})
        grade_d_2_employees.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_cdi_plein = self.env['rh.grade'].search(['|', ('corps_id.intitule_corps', 'ilike', 'متعاقد'),
                                                       ('corps_id.intitule_corps', 'ilike', 'سيار'),
                                                       ('intitule_grade', 'ilike', '%غير محدد%كامل%')])
        employees_cdi_plein = []
        for grade in grade_cdi_plein:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('position_statutaire', '=', 'activite'),
                 ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'pleintemps_indeterminee'),
                 ('fin_relation', '=', False)])
            employees_cdi_plein.append({'grade': grade, 'employees': employees})
        employees_cdi_plein.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_cdd_plein = self.env['rh.grade'].search(['|', ('corps_id.intitule_corps', 'ilike', 'متعاقد'),
                                                       ('corps_id.intitule_corps', 'ilike', 'سيار'),
                                                       ('intitule_grade', 'ilike', '%محدد%كامل%'),
                                                       ('intitule_grade', 'not ilike', '%غير%')])
        employees_cdd_plein = []
        for grade in grade_cdd_plein:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('position_statutaire', '=', 'activite'),
                 ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'pleintemps_determinee'),
                 ('fin_relation', '=', False)])
            employees_cdd_plein.append({'grade': grade, 'employees': employees})
        employees_cdd_plein.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_cdi_partiel = self.env['rh.grade'].search(['|', ('corps_id.intitule_corps', 'ilike', 'متعاقد'),
                                                         ('corps_id.intitule_corps', 'ilike', 'سيار'),
                                                         ('intitule_grade', 'ilike', '%غير محدد%جزئي%')])
        employees_cdi_partiel = []
        for grade in grade_cdi_partiel:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('position_statutaire', '=', 'activite'),
                 ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'partiel_indeterminee'),
                 ('fin_relation', '=', False)])
            employees_cdi_partiel.append({'grade': grade, 'employees': employees})
        employees_cdi_partiel.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_cdd_partiel = self.env['rh.grade'].search(['|', ('corps_id.intitule_corps', 'ilike', 'متعاقد'),
                                                         ('corps_id.intitule_corps', 'ilike', 'سيار'),
                                                         ('intitule_grade', 'ilike', '%محدد%جزئي%'),
                                                         ('intitule_grade', 'not ilike', '%غير%')])
        employees_cdd_partiel = []
        for grade in grade_cdd_partiel:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('position_statutaire', '=', 'activite'),
                 ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'partiel_determinee'),
                 ('fin_relation', '=', False)])
            employees_cdd_partiel.append({'grade': grade, 'employees': employees})
        employees_cdd_partiel.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        grade_d_1 = grade_d - grade_d_2
        grade_d_1_employees = []
        for grade in grade_d_1:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            grade_d_1_employees.append({'grade': grade, 'employees': employees})
        grade_d_1_employees.sort(key=lambda x: x['grade'].categorie_id.intitule, reverse=True)

        report_data = {
            'company': self.env.user.company_id,
            'job_supp': supp_employees,
            'job_hight_org_1': hight_org_1_employees,
            'job_hight_org': hight_org_employees,
            'job_hight_squ': hight_squ_employees,
            'grade_proff': proff_employees,
            'grade_a_excluded': grade_a_excluded_employees,
            'grade_b': grade_b_employees,
            'grade_c': grade_c_employees,
            'grade_d_1': grade_d_1_employees,
            'grade_d_2': grade_d_2_employees,
            'grade_cdi_plein': employees_cdi_plein,
            'grade_cdd_plein': employees_cdd_plein,
            'grade_cdi_partiel': employees_cdi_partiel,
            'grade_cdd_partiel': employees_cdd_partiel,

        }

        return report_data
