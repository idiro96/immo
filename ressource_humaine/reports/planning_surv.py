from odoo import models, fields, api, _


class PlanningSurveillanceReport(models.AbstractModel):
    _name = 'report.ressource_humaine.planning_surveillance_report'

    @api.model
    def get_report_values(self, docids, data=None):
        planning = self.env['rh.planning'].browse(docids[0])

        planning_surveillance_line = planning.planning_surveillance_line

        report_data = {
            'planning': planning,
            'company': self.env.user.company_id,
            'planning_surveillance_line': planning_surveillance_line,
        }

        return report_data


# class NoticePlanningSurveillanceReport(models.AbstractModel):
#     _name = 'report.ressource_humaine.notice_planning_surveillance_report'
#
#     @api.model
#     def get_report_values(self, docids, data=None):
#         planning = self.env['rh.planning'].browse(docids[0])
#
#         planning_surveillance_line = planning.planning_surveillance_line
#
#         report_data = {
#             'planning': planning,
#             'company': self.env.user.company_id,
#             'planning_surveillance_line': planning_surveillance_line,
#         }
#
#         return report_data
