# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _


class RHPlanning(models.Model):
    _name = 'rh.planning'
    _rec_name = 'date_surveillance'

    date_surveillance = fields.Date()
    #president_emphy = fields.Many2one('hr.employee')
    time_surveillance_start = fields.Char()
    time_surveillance_end = fields.Char()
    planning_surveillance_line = fields.One2many('rh.planning.line', 'planning_survellance_id')

    def action_planning(self):
        print()
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'إختيار المراقبون',
            'view_mode': 'form',
            'res_model': 'choisir.planning',
        }



