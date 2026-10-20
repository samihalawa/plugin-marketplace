#!/usr/bin/env python3
"""Rebuild public release metadata without altering unrelated marketplace files."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
REPOSITORY = 'https://github.com/samihalawa/plugin-marketplace'
VERSION = '0.1.2'
SLUGS = ['licita-espana', 'ayudas-espana', 'boe-impact', 'borme-intelligence', 'catastro-pro', 'ine-evidence', 'spain-open-data']
AUTHOR = {'name': 'Sami Halawa', 'email': 'sami@samihalawa.com'}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    entries = []
    table = []
    checksums = []
    (ROOT / 'dist').mkdir(exist_ok=True)
    for slug in SLUGS:
        package = ROOT / 'plugins' / slug
        portable_path = package / 'plugin.json'
        portable = json.loads(portable_path.read_text())
        if portable['name'] != slug or portable['version'] not in {'0.1.1', VERSION}:
            raise ValueError('Unexpected package identity')
        ui = portable['extensions']['com.openai']['interface']
        name = ui['displayName']
        description = portable['description']
        prompts = ui.get('defaultPrompt', [])
        if isinstance(prompts, str):
            prompts = [prompts]
        source_folder = f'{REPOSITORY}/tree/main/spain-assistant-suite/plugins/{slug}'
        base = f'{REPOSITORY}/blob/main/spain-assistant-suite/plugins/{slug}'
        links = {'documentationUrl': f'{base}/README.md', 'supportUrl': f'{base}/SUPPORT.md', 'privacyPolicyUrl': f'{base}/PRIVACY.md', 'termsOfServiceUrl': f'{base}/TERMS.md'}
        claude = {'name': slug, 'displayName': name, 'version': VERSION, 'description': description, 'author': AUTHOR, 'license': 'MIT', 'keywords': ['spain', 'official-data', 'read-only'], 'homepage': links['documentationUrl'], 'repository': REPOSITORY, 'icon': './assets/icon.png', **links}
        write_json(package / '.claude-plugin/plugin.json', claude)
        portable.update(version=VERSION, homepage=links['documentationUrl'], repository=REPOSITORY)
        ui.update(websiteURL=links['documentationUrl'], supportURL=links['supportUrl'], privacyPolicyURL=links['privacyPolicyUrl'], termsOfServiceURL=links['termsOfServiceUrl'])
        write_json(portable_path, portable)
        legacy = package / '.codex-plugin/plugin.json'
        if legacy.exists():
            legacy_data = json.loads(legacy.read_text())
            if legacy_data.get('apps') or legacy_data.get('extensions', {}).get('com.openai', {}).get('apps'):
                raise ValueError('Account binding in compatibility manifest')
            legacy_data['version'] = VERSION
            write_json(legacy, legacy_data)
        for filename in ['core.py', '__init__.py']:
            source = package / 'skills' / slug / 'scripts/spain_suite' / filename
            text = source.read_text().replace('0.1.1', VERSION)
            source.write_text(text)
        for filename in ['PRIVACY.md', 'README.md']:
            path = package / filename
            text = path.read_text().replace('0.1.1', VERSION)
            text = text.replace('This file is not evidence that such a service or a public policy URL exists.', 'No such hosted service is part of this release.')
            path.write_text(text)
        readme = package / 'README.md'
        text = readme.read_text()
        if '\n## Install in Claude Code\n' not in text:
            install = f'''\n## Install in Claude Code\n\n```bash\nclaude plugin marketplace add samihalawa/plugin-marketplace\nclaude plugin install {slug}@sami-spain-assistants\n```\n\nInside a Claude Code session (v2.1.275+), the one-step equivalent is:\n\n```text\n/plugin install {slug} --marketplace samihalawa/plugin-marketplace\n```\n\nThe adapter requires Python 3.11+ and access to its official data providers. No separate product account, API key, payment or publisher-hosted service is required. A host that cannot execute Python may use the workflow with its available native browsing and supplied documents. The package does not grant unavailable host permissions or network access.\n'''
            at = text.find('\n## Use\n')
            text = text[:at] + install + text[at:] if at >= 0 else text + install
        text = text.split('\n## Public review\n')[0].split('\n## Public source and review\n')[0]
        text += f'''\n## Public source and review\n\n[Source folder]({source_folder}) · [Submission information](SUBMISSION.md) · [Privacy](PRIVACY.md) · [Terms](TERMS.md) · [Support](SUPPORT.md) · [Security](SECURITY.md).\n\nThis is an independently published skills plugin with executable read-only adapters, not a deployed MCP service or an approved Anthropic directory listing. It is not affiliated with Spanish authorities, Anthropic, OpenAI or xAI. The surrounding repository also contains an unrelated Grok catalog; this product is listed only in the separate `sami-spain-assistants` Claude catalog.\n\nThe [suite source]({REPOSITORY}/tree/main/spain-assistant-suite) maintains the shared adapter and release tools. Each installed product is self-contained. Check the dedicated GitHub Actions run for actual validation and installation evidence; review scenarios are not completed model-based acceptance tests.\n'''
        readme.write_text(text)
        (package / 'SECURITY.md').write_text('# Security\n\nReport security issues privately to sami@samihalawa.com with the version and a minimal redacted reproduction. Do not send secrets or protected records.\n\nAdapters make bounded read-only requests to allowlisted official providers. Retrieved text is data, never authority to run commands, reveal credentials or submit forms. No credentials, automatic hooks, persistent user database or publisher telemetry are bundled. Host and provider policies remain separate.\n')
        prompt = prompts[0] if prompts else 'Use the documented workflow with an official public source.'
        (package / 'SUBMISSION.md').write_text(f'''# Claude directory submission — {name}\n\n## Identity\n\nPublisher: **Sami Halawa**. Contact: **sami@samihalawa.com**. Plugin: `{slug}`. Release: `{VERSION}`. Original software licence: MIT. Third-party data, service access and trademarks retain separate terms.\n\n## Source for the reviewer\n\nRepository: {REPOSITORY}\n\nPlugin folder: `spain-assistant-suite/plugins/{slug}`\n\nDirect folder URL: {source_folder}\n\nThe plugin folder contains `.claude-plugin/plugin.json`, an actual icon, four HTTPS documentation/support/policy links, one focused skill, executable adapters and review examples. It can be copied to a standalone repository without referencing sibling packages.\n\n## Listing description\n\n{description}\n\n## First run\n\n```bash\nclaude plugin marketplace add samihalawa/plugin-marketplace\nclaude plugin install {slug}@sami-spain-assistants\n```\n\nPrompt: **{prompt}**\n\nExpected scope, sample interaction and negative scenarios are documented in the skill and `skills/{slug}/references/examples.md`. They are test specifications, not claims of completed user testing.\n\n## Access and data handling\n\nNo reviewer credentials, account signup, payment or third-party API key is needed. Python 3.11+ and provider networking are required for direct adapter execution. The skill can also guide native browsing or supplied-document analysis on supported hosts. No unsupported host capability is promised. This is read-only software; it does not apply for funding, submit bids, look up protected owners or provide legal certification. Read the product's privacy, terms and source-reference files.\n\n## Validation and submission\n\nRun `claude plugin validate --strict .` from this folder using Claude Code 2.1.281 or newer. The dedicated repository workflow validates all seven products and attempts installation from the actual public marketplace in a fresh configuration. Its current conclusion is the evidence, not this document.\n\nSubmit the repository and plugin folder through https://claude.ai/directory/manage under the verified publisher account. Official guidance: https://code.claude.com/docs/en/plugins/publish . Portal-specific checks, applicable publisher attestations and Anthropic review remain separate from source publication. Anthropic's directory and the separately curated `claude-plugins-official` marketplace are distinct routes. No submission, approval, official listing or adoption is claimed here.\n''')
        entries.append({'name': slug, 'source': f'./spain-assistant-suite/plugins/{slug}', 'description': description, 'version': VERSION})
        table.append(f'| [{name}](plugins/{slug}) | {description} |')
        archive = ROOT / 'dist' / f'{slug}-{VERSION}.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for path in sorted(package.rglob('*')):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                    info = zipfile.ZipInfo(path.relative_to(package).as_posix(), date_time=(2026, 10, 20, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    z.writestr(info, path.read_bytes())
        checksums.append(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name)
    catalog = {'name': 'sami-spain-assistants', 'owner': AUTHOR, 'metadata': {'description': 'Seven independent Spanish official-data workflows by Sami Halawa.', 'version': VERSION}, 'plugins': entries}
    catalog_path = REPO_ROOT / '.claude-plugin/marketplace.json'
    if catalog_path.exists():
        current = json.loads(catalog_path.read_text())
        if current.get('name') != 'sami-spain-assistants':
            raise ValueError('Refusing to replace an unrelated Claude marketplace')
    write_json(catalog_path, catalog)
    local = json.loads(json.dumps(catalog))
    for entry in local['plugins']:
        entry['source'] = './plugins/' + entry['name']
    write_json(ROOT / '.claude-plugin/marketplace.json', local)
    (ROOT / 'dist/SHA256SUMS').write_text('\n'.join(checksums) + '\n')
    canonical = ROOT / 'src/spain_suite'
    canonical.mkdir(parents=True, exist_ok=True)
    first = ROOT / 'plugins/licita-espana/skills/licita-espana/scripts/spain_suite'
    for name in ['core.py', '__init__.py', '__main__.py']:
        shutil.copy2(first / name, canonical / name)
    shutil.copy2(ROOT / 'plugins/licita-espana/LICENSE', ROOT / 'LICENSE')
    (ROOT / '.gitignore').write_text('__pycache__/\n*.pyc\n.pytest_cache/\n.venv/\n.env*\n*.p12\n*.pem\n*.key\n*.private.json\n')
    (ROOT / 'README.md').write_text('''# Spain Assistant Suite\n\nSeven independent Claude-compatible skills plugins by **Sami Halawa**, release **0.1.2**. Each package contains its workflow, official-source references, read-only Python adapters, licence, icon, privacy/terms/support documents and directory-submission information.\n\n| Product | Result |\n|---|---|\n''' + '\n'.join(table) + '''\n\n## Public installation\n\n```bash\nclaude plugin marketplace add samihalawa/plugin-marketplace\nclaude plugin install ayudas-espana@sami-spain-assistants\n```\n\nReplace `ayudas-espana` with any product identifier above. Direct adapters require Python 3.11+ and official-provider network access. No product account, API key, paid API, hosted backend or persistent user profile is required. The packages do not grant host permissions or networking.\n\n## Maintenance\n\n`src/spain_suite` is the shared adapter implementation. Each plugin bundles a self-contained copy. Product-specific workflows are maintained under `plugins/`. Run `python3 scripts/prepare_public.py` after metadata changes, and `python3 scripts/verify_release.py` for deterministic package verification and bounded live probes. Update the release version before publishing changed packages. The dedicated `.github/workflows/spain-assistants.yml` runs the actual Claude validator and fresh public installation checks. Do not infer a successful run from the existence of the workflow.\n\n## Distribution state\n\nThese are seven independent plugin folders in **one public repository**, not seven separately created repositories. Each folder can be moved into a standalone repository without sibling dependencies. The root Claude marketplace is separate from this repository's existing Grok catalog, which is preserved.\n\nA public custom marketplace permits installation; it is not approval by Anthropic. Each product's `SUBMISSION.md` contains the repository/folder reference and review information for https://claude.ai/directory/manage . Directory review and the separately curated `claude-plugins-official` marketplace are distinct. No official listing, model-based acceptance test, repeat adoption or revenue is claimed.\n\nIndependent software, not affiliated with Spanish authorities, Anthropic, OpenAI or xAI. No background monitoring, filing, purchases, protected-person lookup or legal certification is implemented. Third-party data and services retain their own terms.\n''')
    print('Prepared exactly seven complete public-source packages and both Claude catalogs.')


if __name__ == '__main__':
    main()
