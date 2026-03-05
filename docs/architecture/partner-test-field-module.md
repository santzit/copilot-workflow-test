# Architecture Document — `santzit_partner_test_field`

## 1. Module Overview

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| Technical Name   | `santzit_partner_test_field`              |
| Human Name       | SantzIT — Campo de Teste no Parceiro      |
| Version          | `16.0.1.0.0`                              |
| Odoo Series      | 16.0                                      |
| License          | AGPL-3.0-or-later                         |
| Author           | SantzIT                                   |
| Category         | Customizations                            |

## 2. Purpose and Scope

This module is a **learning tutorial** that demonstrates the full 5-agent collaborative
development lifecycle (Architect → Dev → QA → Security → Documentation) on a DOODBA
Odoo 16.0 project.

**Functional scope:** add a single boolean field `test_field` to the built-in
`res.partner` model and expose it on the partner form view.

This module is intentionally minimal so that every agent can focus on process and
tooling rather than complex business logic.

## 3. Layer Diagram

```
┌──────────────────────────────────────────────────┐
│  Browser / Odoo Web Client                       │
│  (res.partner form view — partner_test_field)    │
└────────────────────┬─────────────────────────────┘
                     │ RPC / JSON-RPC
┌────────────────────▼─────────────────────────────┐
│  Odoo Server — Python / ORM Layer                │
│  santzit_partner_test_field.models.res_partner   │
│  (_inherit = "res.partner")                      │
└────────────────────┬─────────────────────────────┘
                     │ SQL
┌────────────────────▼─────────────────────────────┐
│  PostgreSQL 14                                   │
│  Column: res_partner.test_field (boolean, false) │
└──────────────────────────────────────────────────┘
```

### Where this module sits in the DOODBA stack

```
doodba-santzit-br/
└── odoo/
    └── custom/
        └── src/
            └── santzit_partner_test_field/   ← this module
```

Mounted into the Odoo container via `docker-compose` volume at
`/mnt/extra-addons/santzit_partner_test_field`.

## 4. Inheritance Strategy

```python
class ResPartner(models.Model):
    _inherit = "res.partner"
```

**Why `_inherit` (class-level extension)?**

- `_inherit` without `_name` adds fields/methods to an **existing** model and its
  existing database table. No new table is created — PostgreSQL simply adds a column
  to `res_partner`.
- This is the idiomatic Odoo pattern for lightweight extensions that do not need a
  separate comodel or delegation inheritance.
- `_inherits` (delegation) would create a separate table and is unnecessary here.
- Creating a new `_name` would produce a standalone model unrelated to partners.

## 5. Field Definition

| Attribute   | Value                                  |
|-------------|----------------------------------------|
| Field name  | `test_field`                           |
| Odoo type   | `fields.Boolean`                       |
| Default     | `False`                                |
| String (pt_BR) | `"Campo de Teste"`                  |
| Help (pt_BR) | `"Campo booleano de teste tutorial."` |
| Required    | No                                     |
| Readonly    | No                                     |
| Store       | `True` (default for Boolean)           |
| Index       | No (not needed for a tutorial field)   |

```python
test_field = fields.Boolean(
    string="Campo de Teste",
    help="Campo booleano de teste tutorial.",
    default=False,
)
```

## 6. View Changes

### 6.1 Form View

Inherit the default `res.partner` form view and append `test_field` inside the
**"Sales & Purchase"** tab (or at the bottom of the first page if the tab is absent
in a minimal Odoo installation).

```xml
<record id="view_partner_form_test_field" model="ir.ui.view">
    <field name="name">res.partner.form.test_field</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//page[@name='sales_purchases']" position="inside">
            <group string="Tutorial">
                <field name="test_field"/>
            </group>
        </xpath>
    </field>
</record>
```

### 6.2 List View (optional)

For demonstration purposes a list-view inheritance is **not** included in v1.0.0.
It can be added in a future iteration without any model changes.

## 7. Security

### 7.1 Access Rights

`test_field` lives on `res.partner`, which already has access records defined by the
`base` module. **No new `ir.model.access.csv` entries are required** — every user who
can read/write a partner can read/write the new field automatically.

If field-level access control is needed in the future, Odoo's `ir.model.fields`
`groups` attribute can be used:

```python
test_field = fields.Boolean(
    ...,
    groups="base.group_system",   # restrict to administrators only
)
```

This is intentionally left unrestricted in the tutorial to keep the scope minimal.

### 7.2 Groups (recommended future scope)

| Group                   | Read | Write |
|-------------------------|------|-------|
| Internal User (default) | ✅   | ✅    |
| Portal User             | ❌   | ❌    |
| Public User             | ❌   | ❌    |

Enforcement via `groups` attribute on the field definition is sufficient — no extra
access rules are required.

## 8. Translations

A `i18n/pt_BR.po` file is provided with Brazilian Portuguese strings for:
- Field label: `"Campo de Teste"`
- Field help: `"Campo booleano de teste tutorial."`

## 9. Dependencies

```python
"depends": ["base"],
```

`base` is always present in every Odoo installation. No OCA or third-party modules
are required.

## 10. File Structure

```
santzit_partner_test_field/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── res_partner.py
├── views/
│   └── res_partner_views.xml
├── security/
│   └── ir.model.access.csv          # empty — base rules are sufficient
└── i18n/
    └── pt_BR.po
```

## 11. Handoff Notes for Dev Agent

1. The module technical name is `santzit_partner_test_field`.
2. All user-visible strings must use `pt_BR` as the primary language.
3. The view xpath targets `//page[@name='sales_purchases']`; fall back to
   `//sheet//group[1]` if the tab is not present.
4. Run `pre-commit` (flake8, pylint-odoo, prettier-xml) before committing.
5. The module version follows the Odoo convention `<series>.<major>.<minor>.<patch>` →
   `16.0.1.0.0`.
6. No migration scripts are needed for v1.0.0.
