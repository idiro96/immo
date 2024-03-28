from datetime import datetime

from odoo import models, api, _, fields



class ArretSalaireReport(models.AbstractModel):
    _name = 'report.ressource_humaine.arret_salaire_rapport'

    @api.model
    def get_report_values(self, docids, data=None):

        decision = self.env['arret.salaire'].browse(docids[0])

        # nom_employee = self.env['rh.fin.relation'].browse(docids)
        # print(nom_employee)
        # nom_employee2 = self.env['rh.fin.relation'].browse(docids[0]).employee_id
        # employee = self.env['hr.employee'].browse(docids)
        # promotion = self.env['rh.promotion.line'].search([('employee_id', '=', nom_employee2.id)])
        # date_grade = nom_employee.employee_id.date_grade
        # formatted_date = datetime.strptime(date_grade, "%Y-%m-%d").strftime("%d-%m-%Y")
        # # info_promotion = self.env['rh.promotion'].search([('id', '=', promotion.promotion_id)])
        # # promo = self.env['rh.promotion'].search([('promotion_lines.employee_id', '=', nom_employee2.id)])
        # promo = self.env['rh.promotion'].search([('promotion_lines.employee_id', '=', nom_employee2.id)])

        report_data = {
            'decision': decision,
            # 'nom_employee': nom_employee,
            # 'employee': employee,
            # 'promotion': promotion,
            # 'date_grade': formatted_date,
            # 'promo': promo,
            # 'company': self.env.user.company_id,
        }
        return report_data