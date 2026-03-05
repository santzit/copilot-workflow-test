# copilot-workflow-test

A test repository for a **5-agent GitHub Copilot development pipeline** built on
DOODBA / Odoo 16.0.

---

## 🤖 5-Agent Pipeline

Every new issue (submitted via the **Feature Request** template) is automatically
routed through the following agent pipeline:

```
Issue Created
     │
     ▼
🏛️  Architect  ──── docs/architecture/<slug>.md ───► [Dev] sub-issue
                                                           │
                                                           ▼
                                                  👨‍💻  Developer  ─── PR ───► [QA] sub-issue
                                                                                   │
                                                                                   ▼
                                                                          🧪  QA  ──── QA Report ───► [Security] sub-issue
                                                                                                            │
                                                                                                            ▼
                                                                                                   🔒  Security  ─── Security Report ───► [Docs] sub-issue
                                                                                                                                               │
                                                                                                                                               ▼
                                                                                                                                      📚  Documentation  ─── Merge PR & Close Issue
```

### Agents

| File | Role |
|------|------|
| [`.github/agents/architect.md`](.github/agents/architect.md) | Analyses requirements, produces Architecture Document, creates `[Dev]` sub-issue |
| [`.github/agents/developer.md`](.github/agents/developer.md) | Implements the spec, opens a PR, creates `[QA]` sub-issue |
| [`.github/agents/qa.md`](.github/agents/qa.md) | Validates implementation, posts QA report, creates `[Security]` sub-issue |
| [`.github/agents/security.md`](.github/agents/security.md) | Reviews for vulnerabilities, posts Security Report, creates `[Docs]` sub-issue |
| [`.github/agents/documentation.md`](.github/agents/documentation.md) | Completes docs, merges PR, closes original issue |

### Pipeline Labels

| Label | Meaning |
|-------|---------|
| `needs-architect` | Issue is waiting for the Architect agent |
| `architect-done` | Architect finished → triggers `[Dev]` sub-issue |
| `needs-dev` | Sub-issue waiting for the Developer agent |
| `dev-done` | Developer finished → triggers `[QA]` sub-issue |
| `needs-qa` | Sub-issue waiting for the QA agent |
| `qa-done` | QA finished → triggers `[Security]` sub-issue |
| `needs-security` | Sub-issue waiting for the Security agent |
| `security-done` | Security finished → triggers `[Docs]` sub-issue |
| `needs-docs` | Sub-issue waiting for the Documentation agent |
| `no-pipeline` | Opt out of automatic routing |

### How to use

1. Open a new issue using the **Feature Request / Task** template.
2. The workflow automatically labels it `needs-architect` and pings `@copilot` to act
   as the Architect agent.
3. Once the Architect completes the Architecture Document, apply the label
   `architect-done` — the workflow creates the `[Dev]` sub-issue automatically.
4. Repeat for each stage (`dev-done` → QA, `qa-done` → Security, `security-done` →
   Documentation).
5. The Documentation agent merges the PR and closes the original issue.

> **Tip:** Add the `no-pipeline` label to any issue you want to handle manually.

---

## 📦 Modules

### `santzit_partner_test_field`

Tutorial Odoo module — adds a boolean field `test_field` to `res.partner`.
See [`docs/architecture/partner-test-field-module.md`](docs/architecture/partner-test-field-module.md)
for the full Architecture Document.