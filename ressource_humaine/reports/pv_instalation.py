from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from num2words import num2words

class TitreCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.pv_instalation'

    ARABIC_MONTHS = {
        1: 'يناير',
        2: 'فبراير',
        3: 'مارس',
        4: 'أبريل',
        5: 'مايو',
        6: 'يونيو',
        7: 'يوليو',
        8: 'أغسطس',
        9: 'سبتمبر',
        10: 'أكتوبر',
        11: 'نوفمبر',
        12: 'ديسمبر',
    }
    ARABIC_ORDINALS = {
        1: 'الأول',
        2: 'الثاني',
        3: 'الثالث',
        4: 'الرابع',
        5: 'الخامس',
        6: 'السادس',
        7: 'السابع',
        8: 'الثامن',
        9: 'التاسع',
        10: 'العاشر',
        11: 'الحادي عشر',
        12: 'الثاني عشر',
        13: 'الثالث عشر',
        14: 'الرابع عشر',
        15: 'الخامس عشر',
        16: 'السادس عشر',
        17: 'السابع عشر',
        18: 'الثامن عشر',
        19: 'التاسع عشر',
        20: 'العشرون',
        21: 'الحادي والعشرون',
        22: 'الثاني والعشرون',
        23: 'الثالث والعشرون',
        24: 'الرابع والعشرون',
        25: 'الخامس والعشرون',
        26: 'السادس والعشرون',
        27: 'السابع والعشرون',
        28: 'الثامن والعشرون',
        29: 'التاسع والعشرون',
        30: 'الثلاثون',
        31: 'الحادي والثلاثون'
    }

    @api.model
    def get_report_values(self, docids, data=None):
        pv_insta = self.env['hr.contract'].browse(docids[0])

        start_date = pv_insta.date_start  # Assuming date_start is the field containing the start date

        # Check if start_date is a string, convert it to a datetime object if necessary
        if isinstance(start_date, str):
            start_date = fields.Date.from_string(start_date)

        # Convert the date to a readable format
        formatted_date = fields.Date.to_string(start_date)

        # Convert the formatted date to Arabic text
        arabic_date = self.convert_date_to_arabic(formatted_date)

        superior_job_type_code = 'postesuperieure'
        superior_employee = self.env['hr.employee'].search(
            [('nature_travail_id.code_type_fonction', '=', superior_job_type_code)], limit=1)

        print(superior_employee)

        report_data = {
            'pv_insta': pv_insta,
            'company': self.env.user.company_id,
            'arabic_date': arabic_date,
            'superior_employee': superior_employee,
        }

        return report_data

    def convert_date_to_arabic(self, date_string):
        # Parse the date string to get day, month, and year
        date_obj = datetime.strptime(date_string, DEFAULT_SERVER_DATE_FORMAT)
        day = num2words(date_obj.day, lang='ar')
        month = self.ARABIC_MONTHS.get(date_obj.month, '')  # Get Arabic month name

        year = num2words(date_obj.year, lang='ar')

        # Form the Arabic date string
        arabic_date = f"في {day} من شهر {month} و في سنة {year}"
        return arabic_date




# from odoo import models, fields, api, _
# from odoo.exceptions import UserError
#
#
# class TitreCongeReport(models.AbstractModel):
#     _name = 'report.ressource_humaine.pv_instalation'
#
#     @api.model
#     def get_report_values(self, docids, data=None):
#
#         pv_insta = self.env['hr.contract'].browse(docids[0])
#
#
#         report_data = {
#             'pv_insta': pv_insta,
#             'company': self.env.user.company_id,
#         }
#
#         return report_data
