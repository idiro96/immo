from odoo import models, fields, api, _


class ListeDesEmployes(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_employee'

    @api.model
    def get_report_values(self, docids, data=None):
        employee = self.env['hr.employee'].search([('fin_relation', '=', False)])

        report_data = {
            'employee': employee,
            'company': self.env.user.company_id,
        }

        return report_data
