# Spain Assistant Suite — clearer results, stronger evidence

Seven independent products by **Sami Halawa**, now at **0.2.0**. Each has a public product page, a real saved-source demonstration, readable reports and its own standalone repository.

| Product and live demo | Promise | Public release |
|---|---|---|
| [Licita España](https://samihalawa.github.io/licita-espana/) | Decide qué licitación merece tu tiempo. | [Source](https://github.com/samihalawa/licita-espana) · [0.2.0](https://github.com/samihalawa/licita-espana/releases/tag/v0.2.0) |
| [Ayudas España](https://samihalawa.github.io/ayudas-espana/) | De una ayuda publicada a un próximo paso claro. | [Source](https://github.com/samihalawa/ayudas-espana) · [0.2.0](https://github.com/samihalawa/ayudas-espana/releases/tag/v0.2.0) |
| [BOE Impact](https://samihalawa.github.io/boe-impact/) | Ve qué cambió. Entiende qué revisar. | [Source](https://github.com/samihalawa/boe-impact) · [0.2.0](https://github.com/samihalawa/boe-impact/releases/tag/v0.2.0) |
| [BORME Intelligence](https://samihalawa.github.io/borme-intelligence/) | Los cambios de una empresa, con su fuente delante. | [Source](https://github.com/samihalawa/borme-intelligence) · [0.2.0](https://github.com/samihalawa/borme-intelligence/releases/tag/v0.2.0) |
| [Catastro Pro](https://samihalawa.github.io/catastro-pro/) | Una referencia. Una ficha clara. | [Source](https://github.com/samihalawa/catastro-pro) · [0.2.0](https://github.com/samihalawa/catastro-pro/releases/tag/v0.2.0) |
| [INE Evidence](https://samihalawa.github.io/ine-evidence/) | La cifra correcta, con su contexto. | [Source](https://github.com/samihalawa/ine-evidence) · [0.2.0](https://github.com/samihalawa/ine-evidence/releases/tag/v0.2.0) |
| [Spain Open Data](https://samihalawa.github.io/spain-open-data/) | Encuentra el dataset. Comprueba si te sirve. | [Source](https://github.com/samihalawa/spain-open-data) · [0.2.0](https://github.com/samihalawa/spain-open-data/releases/tag/v0.2.0) |

## What improved

Spanish-first outcome-led onboarding replaces defensive technical intros. The primary skills are shorter, with detailed source and safety guidance in references. Read-only adapters now produce Markdown, JSON and printable self-contained HTML; `demo` works offline with an explicitly historical official-source snapshot. `doctor` checks the local runtime without sending queries.

The new grant shortlist and seven-day BORME lookup join reliability fixes in pagination, error handling, date triage, coordinates and report escaping. The shared runtime has a read-only consistency checker under [maintenance](maintenance/).

[Critique by product](CRITIQUE.md) · [Versioned verification evidence](evidence/)

## Install

```bash
claude plugin marketplace add samihalawa/plugin-marketplace
claude plugin install ayudas-espana@sami-spain-assistants
```

The catalog pins the exact reviewed v0.2.0 release commits. Every product can also be installed through its own repository marketplace. Direct adapters require Python 3.11+ and official-provider access, but no product account, API key or publisher-hosted backend. ChatGPT workflows use only native host capabilities; this is not a hosted MCP service.

## Evidence and limits

The same 64-test suite passes in all seven repositories. All 18 adapter functions passed bounded live-source checks. Desktop/mobile page and saved-report behavior was tested in 28 isolated browser views. Each release contains its exact timestamps, source scope and verification records. These tests do not prove model-based user acceptance, demand, retention or legal eligibility. Fresh public installation checks are recorded separately after the release.

CI remains a template because the publishing credential lacks workflow-write scope. The temporary import workflow is disabled. Public code, GitHub Pages and custom-marketplace installation are not Anthropic directory approval. No new submission or acceptance is claimed. The unrelated Grok catalog in this repository is preserved.
