from odoo import models, fields, api, _


class ListeNominatifs(models.TransientModel):
    _name = 'liste.nominatifs'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_liste_nominatife').report_action(self)


class PlanningCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_nominatife_employee'

    @api.model
    def get_report_values(self, docids, data=None):
        job_sup = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'postesuperieure')])
        supp_employees = []
        for job in job_sup:
            employees = self.env['hr.employee'].search([('job_id', '=', job.id), ('position_statutaire', '=', 'activite'),
                                                        ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                supp_employees.append({'job': job, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                supp_employees.append({'job': job, 'employees': employees, 'promotion_lines': None})

        job_hight_org = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
                                               ('poste_organique', '=', 'organique')])
        hight_org_employees = []
        for job in job_hight_org:
            employees = self.env['hr.employee'].search([('job_id', '=', job.id), ('position_statutaire', '=', 'activite'),
                                                        ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                hight_org_employees.append({'job': job, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                hight_org_employees.append({'job': job, 'employees': employees, 'promotion_lines': None})

        job_hight_squ = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
                                                   ('poste_organique', '=', 'squelaire')])

        squ_employees = self.env['hr.employee'].search(
                [('job_id.poste_organique', '=', 'squelaire'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
        squ_employees_promotion_mapping = {}
        for employee in squ_employees:
            promotion_line = self.env['rh.promotion.line'].search([
                ('employee_id', '=', employee.id)
            ], order='date_new_grade DESC', limit=1)
            squ_employees_promotion_mapping[employee] = promotion_line

        grade_enseignant = self.env['rh.grade'].search([('intitule_grade', 'ilike', '%أستاذ%')])
        enseignant_employees = []
        for grade in grade_enseignant:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                enseignant_employees.append(
                    {'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                enseignant_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        grade_a = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', '%المجموعة أ%')])
        grade_a_excluded = grade_a - grade_enseignant
        grade_a_employees = []
        for grade in grade_a_excluded:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                grade_a_employees.append(
                    {'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                grade_a_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        grade_b = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', '%المجموعة ب%')])
        grade_b_employees = []
        for grade in grade_b:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                grade_b_employees.append(
                    {'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                grade_b_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        grade_c = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', '%المجموعة ج%')])
        grade_c_employees = []
        for grade in grade_c:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                grade_c_employees.append(
                    {'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                grade_c_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        grade_d = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', '%المجموعة د%')])
        grade_ing = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', '%المجموعة د%'),
                                                 ('corps_id.intitule_corps', 'ilike', '%مهن%')])
        grade_contract = self.env['rh.grade'].search(['|', ('corps_id.intitule_corps', 'ilike', '%متعاقد%'), ('corps_id.intitule_corps', 'ilike', '%سيار%')])
        grade_d_filtered = grade_d - grade_ing
        grade_d_filtered_employees = []
        for grade in grade_d_filtered:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                grade_d_filtered_employees.append(
                    {'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                grade_d_filtered_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        grade_ing_employees = []
        for grade in grade_ing:
            employees = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
                 ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                grade_ing_employees.append(
                    {'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                grade_ing_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        grade_contract_employees = []
        for grade in grade_contract:
            employees_contract = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            employees_cdi_plein = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'pleintemps_indeterminee'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines_cdi_plein = self.env['rh.promotion.line'].search(
                [('employee_id', 'in', employees_cdi_plein.ids)],
                order='date_new_grade DESC', limit=1)
            employees_cdd_plein = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'pleintemps_determinee'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines_cdd_plein = self.env['rh.promotion.line'].search(
                [('employee_id', 'in', employees_cdd_plein.ids)],
                order='date_new_grade DESC', limit=1)
            employees_cdi_partiel = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'partiel_indeterminee'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines_cdi_partiel = self.env['rh.promotion.line'].search(
                [('employee_id', 'in', employees_cdi_partiel.ids)],
                order='date_new_grade DESC', limit=1)
            employees_cdd_partiel = self.env['hr.employee'].search(
                [('grade_id', '=', grade.id), ('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                 ('type_id.code_type_contract', '=', 'partiel_determinee'), ('position_statutaire', '=', 'activite'),
                 ('fin_relation', '=', False)])
            promotion_lines_cdd_partiel = self.env['rh.promotion.line'].search(
                [('employee_id', 'in', employees_cdd_partiel.ids)],
                order='date_new_grade DESC', limit=1)
            if promotion_lines_cdi_plein and promotion_lines_cdd_plein and promotion_lines_cdi_partiel and promotion_lines_cdd_partiel:
                grade_contract_employees.append(
                    {'grade': grade,
                     'employees_contract': employees_contract,
                     'employees_cdi_plein': employees_cdi_plein,
                     'employees_cdd_plein': employees_cdd_plein,
                     'employees_cdi_partiel': employees_cdi_partiel,
                     'employees_cdd_partiel': employees_cdd_partiel,
                     'promotion_lines_cdi_plein': promotion_lines_cdi_plein,
                     'promotion_lines_cdd_plein': promotion_lines_cdd_plein,
                     'promotion_lines_cdi_partiel': promotion_lines_cdi_partiel,
                     'promotion_lines_cdd_partiel': promotion_lines_cdd_partiel})
            else:
                grade_contract_employees.append(
                    {'grade': grade,
                     'employees_contract': employees_contract,
                     'employees_cdi_plein': employees_cdi_plein,
                     'employees_cdd_plein': employees_cdd_plein,
                     'employees_cdi_partiel': employees_cdi_partiel,
                     'employees_cdd_partiel': employees_cdd_partiel,
                     'promotion_lines_cdi_plein': None,
                     'promotion_lines_cdd_plein': None,
                     'promotion_lines_cdi_partiel': None,
                     'promotion_lines_cdd_partiel': None})

        employees_detachement = self.env['hr.employee'].search([('position_statutaire', '=', 'detachement'),
                                                                ('fin_relation', '=', False)])
        employees_horscadre = self.env['hr.employee'].search([('position_statutaire', '=', 'horscadre'),
                                                                ('fin_relation', '=', False)])
        employees_miseendisponibilite = self.env['hr.employee'].search([('position_statutaire', '=', 'miseendisponibilite'),
                                                              ('fin_relation', '=', False)])
        employees_servicenationale = self.env['hr.employee'].search([('position_statutaire', '=', 'servicenationale'),
                                                              ('fin_relation', '=', False)])

        report_data = {
            'doc_ids': docids,
            'job_sup': supp_employees,
            'job_hight_org': hight_org_employees,
            'job_hight_squ': job_hight_squ,
            'squ_employees': squ_employees,
            'squ_employees_promotion_mapping': squ_employees_promotion_mapping,
            'grade_enseignant': enseignant_employees,
            'grade_a': grade_a_employees,
            'grade_b': grade_b_employees,
            'grade_c': grade_c_employees,
            'grade_d_filtered': grade_d_filtered_employees,
            'grade_ing': grade_ing_employees,
            'grade_contract': grade_contract_employees,
            'employees_detachement': employees_detachement,
            'employees_horscadre': employees_horscadre,
            'employees_miseendisponibilite': employees_miseendisponibilite,
            'employees_servicenationale': employees_servicenationale,
        }

        return report_data
