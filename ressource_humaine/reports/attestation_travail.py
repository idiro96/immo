from datetime import datetime

from odoo import models, fields, api, _


class EmployeeAttestationTravail(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_employee_attestation_travail_report').report_action(self)


class EmployeeAttestationTravailReport(models.AbstractModel):
    _name = 'report.ressource_humaine.employee_attestation_travail_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employee = self.env['hr.employee'].browse(docids[0])
        report_birthday = employee.birthday
        formatted_date = datetime.strptime(report_birthday, "%Y-%m-%d").strftime("%Y/%m/%d")
        date_entrer = employee.date_entrer
        formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%Y/%m/%d")

        report_data = {
            'date_entrer': formatted_date_entrer,
            'formatted_date': formatted_date,
            'employee': employee,
            'company': self.env.user.company_id,
        }

        return report_data
