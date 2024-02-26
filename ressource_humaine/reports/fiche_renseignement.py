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

        report_data = {
            'employee': employee,
            'company': self.env.user.company_id,
        }

        return report_data
