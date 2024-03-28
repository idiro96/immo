# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFile(models.Model):
    _name = 'rh.file'

    fichier = fields.Binary()
    description_fichier = fields.Char()
    sanction_id = fields.Many2one('rh.sanction')
    organisme_id = fields.Many2one('rh.organisme')
    fin_relation_id = fields.Many2one('rh.fin_relation')
    cabinet_medicale_id = fields.Many2one('rh.fin_relation')
    enfant_id = fields.Many2one('rh.enfant')
    conjoint_id = fields.Many2one('rh.conjoint')
    absence_id = fields.Many2one('rh.absence')
    formation_id = fields.Many2one('rh.formation')
    avancement_id = fields.Many2one('rh.avancement')
    avancement_line_id = fields.Many2one('rh.avancement.line')
    promotion_line_id = fields.Many2one('rh.promotion.line')
    promotion_id = fields.Many2one('rh.promotion_id')
    accident_travail_id = fields.Many2one('rh.accident_travail')
    type_file_id = fields.Many2one('rh.type.file')
    employee_id = fields.Many2one('hr.employee')