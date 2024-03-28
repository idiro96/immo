# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.hr_holidays.models.hr_holidays import Holidays
from odoo.exceptions import ValidationError, UserError


class HrHolidaysInherited(models.Model):
    _inherit = "hr.holidays"

    holiday_status_id = fields.Many2one("hr.holidays.status", string="Leave Type", required=False, readonly=True,
                                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                        compute='_get_default_value')
    code = fields.Char()

    def _get_default_value(self):
        # You can set the default value based on your requirements
        # For example, if you want to set a specific record as default, you can use the `search` method
        default_record = self.env['hr.holidays.status'].search([('name', '=', 'Legal Leaves 2023')], limit=1)
        print('ici')
        print(default_record)
        # Return the ID of the default record
        return default_record

    @api.multi
    def print_conge(self):
        return self.env.ref('ressource_humaine.report_titre_conge').report_action(self)

    @api.multi
    def note_conge(self):
        return self.env.ref('ressource_humaine.report_note_conge').report_action(self)

    @api.multi
    def planning_conge(self):
        return self.env.ref('ressource_humaine.report_planning_conge').report_action(self)

    @api.multi
    def _check_holidays(self):
        # Votre code ici
        leave_days = 0

        employ = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        if employ:
            leave_days = employ.days_off
            leave_days = 0
            print('ici conge1')
        result = super(Holidays, self)._check_holidays()
        employ.write({'days_off': 0})
        print('ici conge2')
        # Votre code supplémentaire ici
        return result

    @api.model
    def create(self, vals):
        holidays = super(HrHolidaysInherited, self).create(vals)
        employ = self.env['hr.employee'].search([('id', '=', holidays.employee_id.id)])
        holiday = self.env['hr.holidays'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'confirm')])
        if employ:
            print(holiday)
            print(employ.days_off - holiday.number_of_days_temp)
            if employ.days_off - holiday.number_of_days >= holidays.number_of_days_temp:
                pass
            else:
                raise ValidationError(_('The number of remaining leaves is not sufficient for this leave type.\n'
                                        'Please verify also the leaves waiting for validation.'))

        print('rrrrrrr2')

        return holidays

    @api.multi
    def action_approve(self):
        for holidays in self:
            employ = self.env['hr.employee'].search([('id', '=', holidays.employee_id.id)])
            if employ:
                print('rrrrrrr')
                if employ.days_off >= holidays.number_of_days_temp:
                    droitconge = self.env['rh.congedroit'].search([('id_personnel', '=', employ.id)], limit=3)
                    jours_conge = holidays.number_of_days_temp
                    nbr_jour_reste = 0
                    nbr_jour_consomme = 0
                    for droit in droitconge:
                        if droit.nbr_jour >= droit.nbr_jour_reste:
                            if droit.nbr_jour_reste > jours_conge:
                                if jours_conge > 0:
                                    nbr_jour_resteOld = droit.nbr_jour_reste
                                    print('ancien')
                                    print(nbr_jour_resteOld)
                                    nbr_jour_reste = droit.nbr_jour_reste - jours_conge
                                    print('new ')
                                    print(nbr_jour_reste)
                                    nbr_jour_consomme = droit.nbr_jour - nbr_jour_reste
                                    print('consomme new ')
                                    print(nbr_jour_consomme)
                                    jours_conge = jours_conge - (nbr_jour_resteOld - nbr_jour_reste)
                                    print('reste conge new ')
                                    print(nbr_jour_consomme)
                                    droit.write({'nbr_jour_reste': nbr_jour_reste})
                                    droit.write({'nbr_jour_consomme': nbr_jour_consomme})
                            else:
                                jours_conge = jours_conge - droit.nbr_jour_reste
                                print('conge')
                                print(jours_conge)
                                droit.nbr_jour_reste = 0
                                nbr_jour_consomme = droit.nbr_jour - nbr_jour_reste

                                droit.write({'nbr_jour_reste': 0})
                                droit.write({'nbr_jour_consomme': nbr_jour_consomme})

                    leave_days = employ.days_off - holidays.number_of_days_temp
                    employ.write({'days_off': leave_days})

            holidays.write({'state': 'validate'})

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == 'validate':
                raise UserError(
                    "Vous ne pouvez pas supprimer un enregistrement déja validé")
        return super(HrHolidaysInherited, self).unlink()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):

        for rec in self:
            department = self.env['hr.department'].search([('id', '=', rec.employee_id.department_id.id)])
        self.department_id = department

    @api.onchange('date_to')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        date_from = fields.Date.from_string(self.date_from)
        date_to = fields.Date.from_string(self.date_to)
        difference = date_to - date_from
        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.number_of_days_temp = difference.days + 1
        else:
            self.number_of_days_temp = 0

    @api.onchange('date_from')
    def _onchange_date_from(self):
        """ Update the number_of_days. """
        date_from = fields.Date.from_string(self.date_from)
        date_to = fields.Date.from_string(self.date_to)
        if date_to and date_from:
            difference = date_to - date_from
        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.number_of_days_temp = difference.days + 1
        else:
            self.number_of_days_temp = 0


class NoteCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.note_conge'

    @api.model
    def get_report_values(self, docids, data=None):
        data = self.env['hr.holidays'].browse(docids[0])

        report_data = {
            'code': data.code,
        }

        return report_data
