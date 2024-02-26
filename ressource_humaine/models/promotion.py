# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _

class RHPromotion(models.Model):
    _name = 'rh.promotion'

    date_examin_professionnel= fields.Date()
    date_promotion = fields.Date()
    code = fields.Char()
    promotion_lines = fields.One2many('rh.promotion.line', inverse_name='promotion_id')
    promotion_file_lines = fields.One2many('rh.file', 'promotion_id')
    promotion_lines_wizard = fields.One2many('rh.promotion.line.wizard', inverse_name='promotion_id')

    avancement_wizard = fields.Boolean(default=True)

    type_fonction_id = fields.Many2one('rh.type.fonction')
    job_id = fields.Many2one('hr.job')
    grade_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    choisir_commission_lines = fields.One2many('rh.promotion.commission.line', 'promotion_id')
    date_creation = fields.Char(compute="_compute_date", store=True)

    @api.depends('date_promotion')
    def _compute_date(self):
        for record in self:
            if record.create_date:
                # Convertit le champ en un objet datetime
                datetime_object = record.create_date.split(' ')
                # Récupère uniquement la date
                date_creation = datetime_object[0]
                record.date_creation = date_creation


    @api.model
    def create(self, vals):
        print('errrrrrrrreeeeeeeeeeeerre')
        for rec2 in self:
            rec2.avancement_wizard = False

        promotion = super(RHPromotion, self).create(vals)
        if promotion.promotion_lines_wizard and promotion.promotion_lines_wizard.ids:
            for rec in promotion.promotion_lines_wizard:
                if rec.employee_id.nature_travail_id.code_type_fonction == 'fonction':
                    promo_line = self.env['rh.promotion.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.type_fonction_id.id,
                        'job_id': rec.job_id.id,
                        'date_examin_professionnel': promotion.date_examin_professionnel,
                        'promotion_id': promotion.id,
                        'date_promotion': promotion.date_promotion,
                        'grade_id': rec.grade_id.id,
                        'date_grade': rec.date_grade,
                        'grade_new_id': rec.grade_new_id.id,
                        'date_new_grade': rec.date_new_grade,
                        'duree': rec.duree,
                    })
                    employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                    grade = self.env['rh.grade'].search([('grade_id', '=', rec.grade_new_id.id)])
                    if grade:
                        employee.write({'corps_id': grade.corps_id.id})
                    employee.write({'grade_id': rec.grade_new_id.id})
                    employee.write({'date_grade': rec.date_new_grade})
                elif rec.employee_id.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                    promo_line = self.env['rh.promotion.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.type_fonction_id.id,
                        'job_id': rec.job_id.id,
                        'date_examin_professionnel': self.date_examin_professionnel,
                        'promotion_id': promotion.id,
                        'date_promotion': self.date_promotion,
                        'grade_id': rec.grade_id.id,
                        'date_grade': rec.date_grade,
                        'grade_new_id': rec.grade_new_id.id,
                        'date_new_grade': rec.date_new_grade,
                        'duree': rec.duree,

                    })
                    employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                    grade = self.env['rh.grade'].search([('grade_id', '=', rec.grade_new_id.id)])
                    if grade:
                        employee.write({'corps_id': grade.corps_id.id})
                    employee.write({'grade_id': rec.grade_new_id.id})
                    employee.write({'date_grade': rec.date_new_grade})
                elif rec.employee_id.nature_travail_id.code_type_fonction == 'postesuperieure':
                    promo_line = self.env['rh.promotion.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.type_fonction_id.id,
                        'job_id': rec.job_id.id,
                        'date_examin_professionnel': self.date_examin_professionnel,
                        'promotion_id': promotion.id,
                        'date_promotion': self.date_promotion,
                        'grade_id': rec.grade_id.id,
                        'date_grade': rec.date_grade,
                        'grade_new_id': rec.grade_new_id.id,
                        'date_new_grade': rec.date_new_grade

                    })
                    print('errrrrrrrreeeeeeeeeeeerre2')
                    employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                    grade = self.env['rh.grade'].search([('grade_id', '=', rec.grade_new_id.id)])
                    print('errrrrrrrreeeeeeeeeeeerre3')
                    if grade:
                        employee.write({'corps_id': grade.corps_id.id})
                    employee.write({'grade_id': rec.grade_new_id.id})
                    employee.write({'date_grade': rec.date_new_grade})

        return promotion

    @api.onchange('date_promotion')
    def _onchange_date_promotion(self):
        """ Update the number_of_days. """
        for rec1 in self:
            rec1.promotion_wizard = True

        employee = self.env['hr.employee'].search([])
        promotion_ligne_droit = self.env['rh.promotion.line.wizard'].search([])
        for record in promotion_ligne_droit:
            record.unlink()
        for rec2  in self:
            promotion_line = self.env['rh.promotion.droit'].search(
                [('date_promotion', '=', rec2.date_promotion),('sauvegarde', '=', True),('retenue', '=', True)],
                order='date_promotion desc')
        if promotion_line:
            for promo in promotion_line:
                dateDebut_object = fields.Date.from_string(self.date_promotion)
                dateDebut_object2 = fields.Date.from_string(promo.date_promotion)
                difference = (
                                        dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                record2 = self.env['rh.promotion.line'].search(
                    [('employee_id', '=', promo.employee_id.id), ('date_promotion', '=', self.date_promotion)])
                if not record2:
                    self.env['rh.promotion.line.wizard'].create({
                                'employee_id': promo.employee_id.id,
                                'type_fonction_id': promo.type_fonction_id.id,
                                'job_id': promo.job_id.id,
                                'grade_id': promo.grade_id.id,
                                'date_grade': promo.date_grade,
                                'grade_new_id': promo.grade_new_id.id,
                                'date_new_grade': promo.date_new_grade,
                                'duree': promo.duree,

                            })

        self.promotion_lines_wizard = self.env['rh.promotion.line.wizard'].search([])

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Promotion',
            'view_mode': 'form',
            'res_model': 'rh.promotion',
        }

    def choisir_commission(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Commission Promotion',
            'view_mode': 'form',
            'res_model': 'commission.promotion',
        }

    @api.multi
    def print_promotions(self):
        return self.env.ref('ressource_humaine.action_hr_tableau_des_promotions').with_context(landscape=True).report_action(self)


class TableauDesPromotions(models.AbstractModel):

    _name = 'report.ressource_humaine.tableau_des_promotions'

    @api.model
    def get_report_values(self, docids, data=None):
        promotion_droit = self.env['rh.promotion.droit'].browse(docids)

        promotion_droit_sauvegarde = promotion_droit.filtered(lambda r: r.sauvegarde)

        droit_promotion = self.env['rh.promotion.droit'].browse(docids[0])
        date_promotion = droit_promotion.date_promotion
        formatted_date_promotion = datetime.strptime(date_promotion, "%Y-%m-%d").strftime("%Y")

        report_data = {
            'promotion_droit': promotion_droit_sauvegarde,
            'company': self.env.user.company_id,
            'date': formatted_date_promotion,
        }

        return report_data


