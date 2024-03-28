from odoo import models, fields, api, _


class PlanningConge(models.TransientModel):
    _name = 'planning.conge'

    department_id = fields.Many2one('hr.department', required=True)

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.report_planning_conge').report_action(self)


class PlanningCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.planning_conge'

    @api.model
    def get_report_values(self, docids, data=None):
        conge = self.env['planning.conge'].browse(docids[0])

        employees = self.env['hr.employee'].search([('department_id', '=', conge.department_id.id)])

        report_data = {
            'conge': conge,
            'company': self.env.user.company_id,
            'employees': employees,
        }

        return report_data
