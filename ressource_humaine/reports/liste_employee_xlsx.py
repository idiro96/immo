from odoo import models


class EmployeeXLS(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_employee_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        employees = self.env['hr.employee'].search([('fin_relation', '=', False)])

        format1 = workbook.add_format({'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#D3D3D3', 'bold': True})
        format1.set_text_wrap()
        format1.set_align('center')
        format1.set_valign('vcenter')
        format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#D3D3D3', 'bold': True})
        format2.set_text_wrap()
        format2.set_align('center')
        format2.set_valign('vcenter')
        format3 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#ADD8E6'})
        format4 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#ADD8E6', 'bold': True})
        format5 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#FFB6C1'})
        format6 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#FFB6C1', 'bold': True})
        format7 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#FFFFFF'})
        sheet = workbook.add_worksheet('Liste des Employés')
        sheet.right_to_left()

        sheet.set_row(0, 25)
        for row_num in range(1, len(employees) + 1):
            sheet.set_row(row_num, 20)

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 10)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 25)
        sheet.set_column(6, 6, 25)
        sheet.set_column(7, 7, 25)
        sheet.set_column(8, 8, 25)
        sheet.set_column(9, 9, 35)
        sheet.set_column(10, 10, 10)
        sheet.set_column(11, 11, 25)

        sheet.write(0, 0, 'الرقم', format1)
        sheet.write(0, 1, 'الاسم و اللقب', format1)
        sheet.write(0, 2, 'تاريخ الميلاد', format1)
        sheet.write(0, 3, 'مكان الميلاد', format1)
        sheet.write(0, 4, 'الرتبة', format1)
        sheet.write(0, 5, 'الوظيفة', format1)
        sheet.write(0, 6, 'تاريح بداية العمل بالمدرسة', format1)
        sheet.write(0, 7, 'تاريخ تعيين في الرتبة', format1)
        sheet.write(0, 8, 'تاريخ التعيين في الوظيفة', format1)
        sheet.write(0, 9, 'Nom et Prénom', format1)
        sheet.write(0, 10, 'ملاحظة', format1)
        sheet.write(0, 11, 'رقم الضمان الاجتماعي', format1)

        # Write employee data
        row = 1
        for index, employee in enumerate(employees, start=1):
            if employee.gender == 'male':
                sheet.write(row, 0, index, format2)
                sheet.write(row, 1, employee.name or '', format3)
                sheet.write(row, 2, employee.birthday or '', format4)
                sheet.write(row, 3, employee.place_of_birth or '', format3)
                sheet.write(row, 4, employee.grade_id.intitule_grade or '', format3)
                sheet.write(row, 5, employee.job_id.name or '', format3)
                sheet.write(row, 6, employee.date_entrer or '', format4)
                sheet.write(row, 7, employee.date_grade or '', format4)
                sheet.write(row, 8, employee.date_job_id or '', format4)
                sheet.write(row, 9, f"{employee.nom_fr or ''} {employee.prenom_fr or ''}", format3)
                sheet.write(row, 10, '', format3)
                sheet.write(row, 11, employee.numero_securite_social or '', format7)
            if employee.gender == 'female':
                sheet.write(row, 0, index, format2)
                sheet.write(row, 1, employee.name or '', format5)
                sheet.write(row, 2, employee.birthday or '', format6)
                sheet.write(row, 3, employee.place_of_birth or '', format5)
                sheet.write(row, 4, employee.grade_id.intitule_grade or '', format5)
                sheet.write(row, 5, employee.job_id.name or '', format5)
                sheet.write(row, 6, employee.date_entrer or '', format6)
                sheet.write(row, 7, employee.date_grade or '', format6)
                sheet.write(row, 8, employee.date_job_id or '', format6)
                sheet.write(row, 9, f"{employee.nom_fr or ''} {employee.prenom_fr or ''}", format3)
                sheet.write(row, 10, '', format5)
                sheet.write(row, 11, employee.numero_securite_social or '', format7)
            if not employee.gender:
                sheet.write(row, 0, index, format2)
                sheet.write(row, 1, employee.name or '', format7)
                sheet.write(row, 2, employee.birthday or '', format7)
                sheet.write(row, 3, employee.place_of_birth or '', format7)
                sheet.write(row, 4, employee.grade_id.intitule_grade or '', format7)
                sheet.write(row, 5, employee.job_id.name or '', format7)
                sheet.write(row, 6, employee.date_entrer or '', format7)
                sheet.write(row, 7, employee.date_grade or '', format7)
                sheet.write(row, 8, employee.date_job_id or '', format7)
                sheet.write(row, 9, f"{employee.nom_fr or ''} {employee.prenom_fr or ''}", format3)
                sheet.write(row, 10, '', format7)
                sheet.write(row, 11, employee.numero_securite_social or '', format7)
            row += 1
