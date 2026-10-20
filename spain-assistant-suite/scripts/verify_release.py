#!/usr/bin/env python3
"""Verify public packages; report live-source checks separately from package checks."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ['licita-espana', 'ayudas-espana', 'boe-impact', 'borme-intelligence', 'catastro-pro', 'ine-evidence', 'spain-open-data']
VERSION = '0.1.2'


def package_checks():
    from PIL import Image
    import yaml
    checks = []
    def check(condition, label):
        if not condition:
            raise AssertionError(label)
        checks.append(label)
    catalog = json.loads((ROOT.parent / '.claude-plugin/marketplace.json').read_text())
    check(catalog['name'] == 'sami-spain-assistants', 'Claude marketplace identity')
    check([p['name'] for p in catalog['plugins']] == SLUGS, 'Exactly seven marketplace entries')
    canonical = (ROOT / 'src/spain_suite/core.py').read_bytes()
    for slug in SLUGS:
        base = ROOT / 'plugins' / slug
        manifest = json.loads((base / '.claude-plugin/plugin.json').read_text())
        check(manifest['name'] == slug and manifest['version'] == VERSION, f'{slug}: identity and release')
        check(manifest['author']['name'] == 'Sami Halawa' and manifest['license'] == 'MIT', f'{slug}: author and licence')
        for key in ['documentationUrl', 'supportUrl', 'privacyPolicyUrl', 'termsOfServiceUrl']:
            check(manifest[key].startswith('https://github.com/samihalawa/plugin-marketplace/blob/main/spain-assistant-suite/plugins/' + slug + '/'), f'{slug}: {key}')
        icon = base / manifest['icon']
        with Image.open(icon) as im:
            check(im.format == 'PNG' and im.size == (512, 512), f'{slug}: actual square PNG icon')
        for name in ['README.md', 'LICENSE', 'PRIVACY.md', 'SUPPORT.md', 'TERMS.md', 'SECURITY.md', 'SUBMISSION.md']:
            check((base / name).is_file() and (base / name).stat().st_size > 30, f'{slug}: {name}')
        check('/plugin install ' + slug + ' --marketplace samihalawa/plugin-marketplace' in (base / 'README.md').read_text(), f'{slug}: concrete install instructions')
        skill = base / 'skills' / slug
        text = (skill / 'SKILL.md').read_text()
        front = yaml.safe_load(text.split('---', 2)[1])
        check(front['name'] == slug and bool(front['description']), f'{slug}: skill frontmatter')
        check((skill / 'scripts/spain_suite/core.py').read_bytes() == canonical, f'{slug}: shared adapter consistency')
        run = subprocess.run([sys.executable, str(skill / 'scripts/run.py'), 'list'], capture_output=True, text=True, timeout=20, check=True)
        listed = json.loads(run.stdout)
        check(isinstance(listed, dict) and set(listed) == {slug}, f'{slug}: executable product-scoped CLI')
        portable = json.loads((base / 'plugin.json').read_text())
        check(portable['name'] == slug and portable['version'] == VERSION, f'{slug}: portable identity')
        check(not portable.get('apps') and not portable.get('extensions', {}).get('com.openai', {}).get('apps'), f'{slug}: no private app bindings')
        with zipfile.ZipFile(ROOT / 'dist' / f'{slug}-{VERSION}.zip') as archive:
            names = archive.namelist()
            check('plugin.json' in names and '.claude-plugin/plugin.json' in names and 'assets/icon.png' in names, f'{slug}: complete distributable archive')
            check(all(not name.startswith('/') and '..' not in Path(name).parts and '__pycache__' not in name and '.env' not in Path(name).name and Path(name).suffix not in {'.p12', '.pem', '.key', '.pyc'} for name in names), f'{slug}: archive hygiene')
            check(archive.read('.claude-plugin/plugin.json') == (base / '.claude-plugin/plugin.json').read_bytes(), f'{slug}: archive/source equality')
    return {'state': 'passed', 'check_count': len(checks), 'checks': checks, 'version': VERSION, 'core_sha256': hashlib.sha256(canonical).hexdigest(), 'checked_at': datetime.now(timezone.utc).isoformat()}


def live_checks():
    sys.path.insert(0, str(ROOT / 'src'))
    from spain_suite import core
    results = []
    replies = {}
    def run(item):
        name, args = item
        begin = time.monotonic()
        try:
            value = core.call_tool(name, args)
            replies[name] = value
            row = {'tool': name, 'arguments': args, 'ok': value.get('ok') is True,
                   'elapsed_seconds': round(time.monotonic() - begin, 3),
                   'coverage': value.get('coverage'), 'sources': value.get('sources', []),
                   'error': value.get('error')}
            if isinstance(value.get('data'), list):
                row['record_count'] = len(value['data'])
        except Exception as exc:
            row = {'tool': name, 'arguments': args, 'ok': False, 'error_type': type(exc).__name__}
        results.append(row)
        print('LIVE', name, 'PASS' if row['ok'] else 'FAILED')
        return replies.get(name, {})
    initial = [
        ('licita_search', {'query': '', 'max_pages': 1, 'limit': 3}),
        ('ayudas_search', {'query': 'digital', 'page_size': 2}),
        ('ayudas_call', {'bdns_number': '936585'}),
        ('boe_daily', {'date': '2026-10-19', 'limit': 3}),
        ('boe_document', {'document_id': 'BOE-A-2026-21668', 'max_chars': 1000}),
        ('boe_consolidated', {'law_id': 'BOE-A-2017-12902', 'limit': 10}),
        ('boe_compare', {'law_id': 'BOE-A-2017-12902', 'block_id': 'a4', 'older_date': '2020-01-01', 'newer_date': '2026-10-19'}),
        ('borme_company_notices', {'company': 'LINGUASERVE', 'date': '2026-10-19', 'province': 'MADRID'}),
        ('catastro_property', {'reference': '2749704YJ0624N0001DI'}),
        ('catastro_coordinates', {'reference': '2749704YJ0624N0001DI'}),
        ('ine_operations', {'query': 'precios consumo'}),
        ('ine_series', {'series_code': 'IPC251852', 'last': 3}),
        ('open_data_search', {'query': 'empleo', 'page_size': 2}),
        ('open_data_dataset', {'dataset_id': 'l01281317-ofertas-de-empleo-publico-y-convocatorias-del-ayuntamiento'}),
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(run, initial))
    operations = replies.get('ine_operations', {})
    if operations.get('ok') and operations.get('data'):
        operation = next((x for x in operations['data'] if x.get('Codigo') == 'IPC'), operations['data'][0])
        tables = run(('ine_tables', {'operation_id': operation['Id'], 'limit': 10}))
        if tables.get('ok') and tables.get('data'):
            run(('ine_table_series', {'table_id': tables['data'][0]['Id'], 'limit': 3}))
    tested = {r['tool'] for r in results}
    missing = sorted(set(core.TOOLS) - tested)
    passed = sum(r['ok'] for r in results)
    return {'checked_at': datetime.now(timezone.utc).isoformat(), 'state': 'passed' if passed == 16 and not missing else 'partial',
            'passed': passed, 'attempted': len(results), 'expected_functions': 16, 'not_tested': missing,
            'scope': 'Bounded adapter smoke tests, not full historical coverage or model-based user acceptance.', 'tests': results}


def main():
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    package = package_checks()
    (evidence / 'package-verification.json').write_text(json.dumps(package, ensure_ascii=False, indent=2) + '\n')
    print('PACKAGE_CHECKS_PASSED', package['check_count'])
    live = live_checks()
    (evidence / 'live-probes.json').write_text(json.dumps(live, ensure_ascii=False, indent=2) + '\n')
    print('LIVE_PROBES', live['passed'], '/', live['expected_functions'], live['state'])
    if live['state'] != 'passed':
        print('::warning::Some provider checks failed or were not exercised; inspect live-probes.json. This is not a successful empty search.')


if __name__ == '__main__':
    main()
