# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from odoo.exceptions import ValidationError, UserError


class RHPromotionDroit(models.Model):
    _name = 'rh.promotion.droit'

    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    job_id = fields.Many2one('hr.job')
    grade_id = fields.Many2one('rh.grade')
    categorie_id = fields.Many2one('rh.categorie')
    grade_new_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()
    date_new_grade = fields.Date()
    date_promotion = fields.Date()
    duree = fields.Integer()

    sauvegarde = fields.Boolean(Default=False)
    retenue = fields.Boolean(Default=False)

    test = fields.Char()
    time_years = fields.Integer(compute="_compute_time", store=True)
    time_months = fields.Integer(compute="_compute_time", store=True)
    time_days = fields.Integer(compute="_compute_time", store=True)
    time_difference = fields.Char(compute="_compute_time")

    # @api.depends('date_grade', 'date_promotion')

    @api.multi
    def write(self, vals):
        result = super(RHPromotionDroit, self).write(vals)
        record1 = self.env['rh.promotion.droit'].browse(self._context['active_ids'])
        print('ranah')
        for rec in self:
            print('ranah1')
            if rec.retenue:
                if not rec.sauvegarde:
                    raise UserError("أكد أولا الحق في التقدم في الرتبة")
            record2 = self.env['rh.promotion.line'].search([('employee_id', '=', rec.employee_id.id),('date_promotion', '=', rec.date_promotion)])
            print('erreure')
            print(rec.employee_id.id)
            print(rec.date_promotion)
            if record2:
                raise UserError("مستحيل تغيير تقدم في الرتبة اللذي تم تحققه")


        return result

    @api.multi
    def unlink(self):
        for rec in self:
            print('ranah')
            record2 = self.env['rh.promotion.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_promotion', '=', rec.date_promotion)])
            if record2:
                raise UserError(
                    "لا يمكنك من حذف تسجيل اللذي تم تحققه")
        return super(RHPromotionDroit, self).unlink()

    def _compute_time(self):
        for rec in self:
            if rec.date_grade and rec.date_promotion:
                date_grade = fields.Datetime.from_string(rec.date_grade)
                date_promotion = fields.Datetime.from_string(rec.date_promotion)
                delta = relativedelta(date_promotion, date_grade)

                years = delta.years
                months = delta.months
                days = delta.days

                rec.time_years = years
                rec.time_months = months
                rec.time_days = days

                # rec.time_difference = str(years) + ' annee et ' + str(months) + ' mois et ' + str(days) + 'jours'
                rec.time_difference = f"قدره {years} سنة و {months} شهر و {days} يوم"
                print(rec.time_difference)
                print('rec.time_difference')

    @api.onchange('duree')
    def _onchange_duree(self):
        for rec in self:
            rec.date_new_grade = relativedelta(months=rec.duree) + fields.Date.from_string(rec.date_grade)

    # def unlink(self):
    #     record = self.env['rh.promotion.droit'].browse(self._context['active_id'])
    #     for line in record:
    #         if line.sauvegarde:
    #             print('teste')
    #             raise ValidationError("Vous ne pouvez pas supprimer cette ligne ")
    #     # return super(RHPromotionDroit, self).unlink()