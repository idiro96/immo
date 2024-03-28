from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from num2words import num2words


class TitreCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.titre_conge'

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

    @api.model
    def get_report_values(self, docids, data=None):
        conge = self.env['hr.holidays'].browse(docids[0])

        contract = self.env['hr.contract'].search([('employee_id', '=', conge.employee_id.id)], limit=1)
        conge_date_to = conge.date_to
        formatted_conge_date_to = datetime.strptime(conge_date_to, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
        conge_date_from = conge.date_from
        formatted_conge_date_from = datetime.strptime(conge_date_from, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")

        arabic_number_of_days_words = self.number_to_arabic_words(int(conge.number_of_days_temp))

        report_data = {
            'conge': conge,
            'company': self.env.user.company_id,
            'contract': contract,
            'conge_date_to': formatted_conge_date_to,
            'conge_date_from': formatted_conge_date_from,
            'arabic_number_of_days_words': arabic_number_of_days_words,
        }

        return report_data

    def number_to_arabic_words(self, number):
        units = ['', 'واحد', 'اثنان', 'ثلاثة', 'أربعة', 'خمسة', 'ستة', 'سبعة', 'ثمانية', 'تسعة']
        teens = ['عشرة', 'أحد عشر', 'اثنا عشر', 'ثلاثة عشر', 'أربعة عشر', 'خمسة عشر', 'ستة عشر', 'سبعة عشر',
                 'ثمانية عشر', 'تسعة عشر']
        tens = ['', 'عشرون', 'ثلاثون', 'أربعون', 'خمسون', 'ستون', 'سبعون', 'ثمانون', 'تسعون']
        thousands = ['', 'ألف', 'مليون', 'مليار', 'تريليون', 'كوادريليون', 'كوينتليون', 'سكستيليون', 'سبتيليون',
                     'أوكتيليون', 'نوفيليون', 'ديسيليون']

        def convert_chunk(chunk):
            result = []

            # Traitement des centaines
            if chunk // 100 > 0:
                result.append(units[chunk // 100] + ' مئة')
                chunk %= 100

            # Traitement des dizaines et unités
            if 0 < chunk < 10:
                result.append(units[chunk])
            elif 10 <= chunk < 20:
                result.append(teens[chunk - 10])
            elif chunk >= 20:
                result.append(tens[chunk // 10 - 1])
                if chunk % 10 > 0:
                    result.append(units[chunk % 10])

            return result

        if number == 0:
            return 'صفر'

        result_words = []
        chunk_count = 0

        while number > 0:
            chunk = number % 1000
            if chunk > 0:
                chunk_words = convert_chunk(chunk)
                if chunk_count > 0:
                    chunk_words.append(thousands[chunk_count])
                result_words = chunk_words + result_words

            number //= 1000
            chunk_count += 1

        return ' و'.join(result_words)
