# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrTypeContractInherited(models.Model):
    _inherit = "hr.contract.type"

    code_type_contract = fields.Char()


