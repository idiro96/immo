from datetime import datetime

from odoo import models, fields, api, _


class FicheRenseignement(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def print_fiche(self):
        return self.env.ref('ressource_humaine.action_fiche_renseignement_report').report_action(self)


class FicheRenseignementReport(models.AbstractModel):
    _name = 'report.ressource_humaine.fiche_renseignement_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employee = self.env['hr.employee'].browse(docids[0])
        conjoint = self.env['rh.conjoint'].search([('employee_id', '=', employee.id)])
        enfant = self.env['rh.enfant'].search([('employee_id', '=', employee.id)])
        date_naissance_enfant = []
        for rec in enfant:
            if rec.date_naissance_enfant:
                formatted_date = datetime.strptime(rec.date_naissance_enfant, "%Y-%m-%d").strftime("%d-%m-%Y")
                date_naissance_enfant.append(formatted_date)
            else:
                date_naissance_enfant.append('')

        report_data = {
            'doc_ids': docids,
            'company': self.env.user.company_id,
            'employee': employee,
            'conjoint': conjoint,
            'enfant': enfant,
            'date_naissance_enfant': date_naissance_enfant,
        }

        return report_data
