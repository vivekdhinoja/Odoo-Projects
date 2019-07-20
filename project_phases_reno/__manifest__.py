# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project by Phases',
    'version': '11.0.0.1',
    'category': 'Projects',
    'author': 'Mitosis',
    'website': 'http://www.mitosis.com',
    'summary': 'This apps helps to manage Project and Task Phases',
    'description': """
        Project Phases.
        Task phases.
        Project by Phases
        Task by Project phases
        Task by Phases
        Project with phases
        Task with phases

""",
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
