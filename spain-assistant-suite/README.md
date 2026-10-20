# Spain Assistant Suite — public repositories

Seven independent public repositories by **Sami Halawa**, with Claude plugin manifests at each repository root and tagged **v0.1.2** releases.

| Public repository | Review material | Version |
|---|---|---|
| [Licita España](https://github.com/samihalawa/licita-espana) | [Submission brief](https://github.com/samihalawa/licita-espana/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/licita-espana/releases/tag/v0.1.2) |
| [Ayudas España](https://github.com/samihalawa/ayudas-espana) | [Submission brief](https://github.com/samihalawa/ayudas-espana/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/ayudas-espana/releases/tag/v0.1.2) |
| [BOE Impact](https://github.com/samihalawa/boe-impact) | [Submission brief](https://github.com/samihalawa/boe-impact/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/boe-impact/releases/tag/v0.1.2) |
| [BORME Intelligence](https://github.com/samihalawa/borme-intelligence) | [Submission brief](https://github.com/samihalawa/borme-intelligence/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/borme-intelligence/releases/tag/v0.1.2) |
| [Catastro Pro](https://github.com/samihalawa/catastro-pro) | [Submission brief](https://github.com/samihalawa/catastro-pro/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/catastro-pro/releases/tag/v0.1.2) |
| [INE Evidence](https://github.com/samihalawa/ine-evidence) | [Submission brief](https://github.com/samihalawa/ine-evidence/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/ine-evidence/releases/tag/v0.1.2) |
| [Spain Open Data](https://github.com/samihalawa/spain-open-data) | [Submission brief](https://github.com/samihalawa/spain-open-data/blob/main/SUBMISSION.md) | [Release](https://github.com/samihalawa/spain-open-data/releases/tag/v0.1.2) |

## Install from the shared Claude marketplace

```bash
claude plugin marketplace add samihalawa/plugin-marketplace
claude plugin install ayudas-espana@sami-spain-assistants
```

Replace `ayudas-espana` with any of the seven identifiers. The catalog pins each verified release commit; maintainers should update the tag and commit when publishing a new version. Each product can also be installed through its own repository marketplace as documented in its README.

## Source and validation

The standalone repositories are canonical; this catalog does not maintain duplicate source packages. Each includes its workflow, Python adapters, actual icon, MIT licence, support/privacy/terms pages, test scripts, validation evidence and SUBMISSION.md. No product account, payment or API key is required. Direct adapters need Python 3.11+ and official-provider network access.

CI templates are included under `ci/` in each product but are not active because the publishing credential lacks workflow-write scope. The obsolete temporary import workflow in this catalog repository is disabled. Local strict validation, live provider tests and fresh-install checks are separate evidence; templates are never counted as executed tests.

## Anthropic review

Submit each standalone repository through https://claude.ai/directory/manage . Source publication and custom-marketplace installation are not Anthropic approval. The portal applies additional checks and publisher requirements. Official guidance: https://code.claude.com/docs/en/plugins/publish .

This independent Claude catalog is separate from the surrounding repository's pre-existing Grok catalog, which has been preserved. No affiliation with xAI, Anthropic, OpenAI or Spanish authorities is claimed.
