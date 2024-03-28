from odoo import models


class PromotiondXLS(models.AbstractModel):
    _name = 'report.ressource_humaine.tableau_des_promotions_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        promotion_droit = self._get_objs_for_report(objs.ids, data)

        format1 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D3D3D3', 'bold': True})
        format1.set_text_wrap()
        format1.set_align('center')
        format1.set_valign('vcenter')
        format2 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D3D3D3', 'bold': True})
        format2.set_text_wrap()
        format2.set_align('center')
        format2.set_valign('vcenter')
        format3 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#FFFFFF'})
        sheet = workbook.add_worksheet('جدول ترقية')
        sheet.right_to_left()

        sheet.set_row(0, 25)
        for row_num in range(1, len(promotion_droit) + 1):
            sheet.set_row(row_num, 20)

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 10)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 25)
        sheet.set_column(6, 6, 10)
        sheet.set_column(7, 7, 25)
        sheet.set_column(8, 8, 25)
        sheet.set_column(9, 9, 10)
        sheet.set_column(10, 10, 10)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 12, 25)
        sheet.set_column(13, 13, 30)

        sheet.write(0, 0, 'الرقم', format1)
        sheet.write(0, 1, 'الاسم و اللقب', format1)
        sheet.write(0, 2, 'تاريخ الميلاد', format1)
        sheet.write(0, 3, 'الحالة العائلية', format1)
        sheet.write(0, 4, 'الرتبة', format1)
        sheet.write(0, 5, 'المنصب', format1)
        sheet.write(0, 6, 'الدرجة', format1)
        sheet.write(0, 7, 'تاريخ سريان الترقيةالحالية', format1)
        sheet.write(0, 8, 'ترقية', format1)
        sheet.write(0, 9, 'عامين و نصف', format1)
        sheet.write(0, 10, 'المدة', format1)
        sheet.write(0, 11, 'التنقيط', format1)
        sheet.write(0, 12, 'تاريخ سريان الترقية القادمة', format1)
        sheet.write(0, 13, 'فرق المدة', format1)

        row = 1
        for index, line in enumerate(promotion_droit, start=1):
            if line.sauvegarde:
                sheet.write(row, 0, index, format2)
                sheet.write(row, 1, line.employee_id.name or '', format3)
                sheet.write(row, 2, line.birthday or '', format3)
                if line.marital == 'single':
                    if line.employee_id.gender == 'male':
                        sheet.write(row, 3, 'أعزب', format3)
                    elif line.employee_id.gender == 'female':
                        sheet.write(row, 3, 'عازبة', format3)
                    else:
                        sheet.write(row, 3, 'أعزب', format3)
                elif line.marital == 'married':
                    if line.employee_id.gender == 'male':
                        sheet.write(row, 3, 'متزوّج', format3)
                    elif line.employee_id.gender == 'female':
                        sheet.write(row, 3, 'متزوّجة', format3)
                    else:
                        sheet.write(row, 3, 'متزوّج', format3)
                elif line.marital == 'cohabitant':
                    sheet.write(row, 3, 'معاش قانوني', format3)
                elif line.employee_id.marital == 'widower':
                    if line.employee_id.gender == 'male':
                        sheet.write(row, 3, 'أرمل', format3)
                    elif line.employee_id.gender == 'female':
                        sheet.write(row, 3, 'أرملة', format3)
                    else:
                        sheet.write(row, 3, 'أرمل', format3)
                elif line.marital == 'divorced':
                    if line.employee_id.gender == 'male':
                        sheet.write(row, 3, 'مطلّق', format3)
                    elif line.employee_id.gender == 'female':
                        sheet.write(row, 3, 'مطلّقة', format3)
                    else:
                        sheet.write(row, 3, 'مطلّق', format3)
                else:
                    sheet.write(row, 3, '', format3)
                sheet.write(row, 4, line.grade_id.intitule_grade or '', format3)
                sheet.write(row, 5, line.job_id.name or '', format3)
                sheet.write(row, 6, line.employee_id.echelon_id.intitule or '', format3)
                sheet.write(row, 7, line.date_grade or '', format3)
                sheet.write(row, 8, line.grade_new_id.intitule_grade or '', format3)
                sheet.write(row, 9, '', format3)
                sheet.write(row, 10, line.duree or '', format3)
                sheet.write(row, 11, '', format3)
                sheet.write(row, 12, line.date_new_grade or '', format3)
                sheet.write(row, 13, line.time_difference or '', format3)
                row += 1

