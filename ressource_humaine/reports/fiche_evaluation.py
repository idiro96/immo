from datetime import datetime

from odoo import models, api, _, fields

class FicheEvaluation(models.AbstractModel):
    _name = 'report.ressource_humaine.fiche_evaluation_report'


    @api.model
    def get_report_values(self, docids, data=None):
        employee_evaluee = self.env['rh.fiche.evaluation'].browse(docids[0])
        employee_info = self.env['hr.employee'].search([('id', '=', employee_evaluee.employee_id.id)])
        # print(employee_evaluee.grade_id.intitule_grade)
        report_data = {
            'employee_evaluee': employee_evaluee,
            'employee_info': employee_info,
        }
        return report_data