from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeAttestationTravailFr(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_employee_attestation_travail_fr_report').report_action(self)


class EmployeeAttestationTravailFrReport(models.AbstractModel):
    _name = 'report.ressource_humaine.employee_attestation_travail_fr_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employee = self.env['hr.employee'].browse(docids[0])
        birthday = employee.birthday
        date_entrer = employee.date_entrer
        formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%d/%m/%Y")
        formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%d/%m/%Y")

        report_data = {
            'formatted_date_entrer': formatted_date_entrer,
            'formatted_birthday': formatted_birthday,
            'employee': employee,
            'company': self.env.user.company_id,
        }

        return report_data
