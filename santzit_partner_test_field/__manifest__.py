{
    "name": "SantzIT — Campo de Teste no Parceiro",
    "summary": "Adiciona o campo booleano test_field ao modelo res.partner.",
    "description": """
SantzIT — Campo de Teste no Parceiro
=====================================

Módulo tutorial que estende o modelo *res.partner* adicionando um campo
booleano chamado ``test_field``.

Este módulo faz parte do projeto de aprendizado do ciclo completo de
desenvolvimento de módulos Odoo com o workflow de 5 agentes (Arquiteto,
Dev, QA, Segurança, Documentação) no contexto de um projeto DOODBA 16.0.
    """,
    "version": "16.0.1.0.0",
    "author": "SantzIT",
    "website": "https://santzit.com",
    "license": "AGPL-3",
    "category": "Customizations",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
