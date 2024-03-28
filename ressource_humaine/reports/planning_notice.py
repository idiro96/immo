from odoo import models, fields, api, _



class PlanningSurveillanceReport(models.AbstractModel):
    _name = 'report.ressource_humaine.notice_planning_surveillance_report'

    @api.model
    def get_report_values(self, docids, data=None):

        employee= self.env['programme.employee'].browse(docids)
        print("employee", employee.employee_id)
        planning = self.env['rh.planning.line'].search([('employee_id', '=', employee.employee_id.id)])
        print("planning", planning)


        report_data = {
            'planning': planning,
            "employee": employee,


        }

        return report_data
