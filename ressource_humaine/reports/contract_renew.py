from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AttestationTravailReport(models.AbstractModel):
    _name = 'report.ressource_humaine.renew_contract_report'

    @api.model
    def get_report_values(self, docids, data=None):
        contract = self.env['hr.contract'].browse(docids[0])

        report_data = {
            'contract': contract,
            'company': self.env.user.company_id,
        }

        return report_data
