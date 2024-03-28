from odoo import fields, models, api
from datetime import datetime




class AttestationCessationReport(models.AbstractModel):
    _name = 'report.ressource_humaine.attestation_cessation'

    @api.model
    def get_report_values(self, docids, data=None):
        employees = self.env['hr.employee'].browse(docids)

        employee_date_entrer = {}
        for employee in employees:
            date_entrer = employee.date_entrer
            formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%d/%m/%Y")
            employee_date_entrer[employee.id] = formatted_date_entrer

        employee_date_fin_relation = {}
        for employee in employees:
            date_fin_relation = employee.date_fin_relation
            if date_fin_relation:
                formatted_date_fin_relation = datetime.strptime(date_fin_relation, "%Y-%m-%d").strftime("%d/%m/%Y")
                employee_date_fin_relation[employee.id] = formatted_date_fin_relation
            else:
                employee_date_fin_relation[employee.id] = ''

        employee_birthday = {}
        for employee in employees:
            birthday = employee.birthday
            if birthday:
                formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%d-%m-%Y")
                employee_birthday[employee.id] = formatted_birthday
            else:
                employee_birthday[employee.id] = ''

        report_data = {
            'employee_birthday': employee_birthday,
            'employee_date_fin_relation': employee_date_fin_relation,
            'employee_date_entrer': employee_date_entrer,
            'employees': employees,
            'company': self.env.user.company_id,
        }

        return report_data