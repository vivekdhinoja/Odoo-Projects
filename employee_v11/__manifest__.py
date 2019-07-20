# -*- coding: utf-8 -*-
{
    'name': "Employee Information",
    'author': "Vivek",
    'website': "http://www.techxstar.com",
    'version': '1.0',
    'depends': ['sale', 'base'],
    'data': [
        "security/ir.model.access.csv",
        "security/employee_security.xml",
        "wizard/wizard_workingdays_view.xml",
        "data/ir_sequence_data.xml",
        "views/employee.xml",
        "report/employee_report.xml",
        "views/report_custom_paper_format.xml",
        "views/report_custom_header.xml",
        "views/report_custom_internal_layout.xml",
        "views/report_employee.xml",
    ],
}
