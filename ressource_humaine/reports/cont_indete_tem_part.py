from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ContratIndetermine(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def print_report(self):
        if self.state != 'open':
            raise UserError(
                _("Ce contrat n'est pas en cours. Vous ne pouvez imprimer l'attestation que pour les contrats en cours."))

        return self.env.ref('ressource_humaine.cont_indete_tem_part_report').report_action(self)


class ContratIdetermineReport(models.AbstractModel):
    _name = 'report.ressource_humaine.cont_indete_tem_part_report'

    @api.model
    def get_report_values(self, docids, data=None):
        contract = self.env['hr.contract'].browse(docids[0])

        superior_job = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'postesuperieur')], limit=1)

        superior_employee = self.env['hr.employee'].search([('job_id', '=', superior_job.id)], limit=1)

        report_data = {
            'contract': contract,
            'company': self.env.user.company_id,
            'superior_employee': superior_employee,
        }

        return report_data
