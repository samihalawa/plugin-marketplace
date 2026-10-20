#!/usr/bin/env python3
"""One-time import of exactly seven packages approved for public source release.

The transient object URLs expose only the source packages being published, not
account APIs. They are removed from the current tree after successful import.
Archive contents are verified before becoming executable repository files.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ['licita-espana', 'ayudas-espana', 'boe-impact', 'borme-intelligence',
         'catastro-pro', 'ine-evidence', 'spain-open-data']
EXPECTED_CORE = 'e80c2f0ea47c60ba389856981ee122393ba679f6d183c6f4de984efd431802b2'


def import_one(item):
    slug = item['name']
    target = ROOT / 'plugins' / slug
    if target.exists():
        manifest = json.loads((target / '.claude-plugin/plugin.json').read_text())
        if manifest['name'] == slug and manifest['version'] == '0.1.2':
            return {'name': slug, 'state': 'existing-public-release-preserved'}
        raise RuntimeError(f'Refusing to overwrite an existing unverified directory: {slug}')
    parsed = urllib.parse.urlsplit(item['url'])
    if parsed.scheme != 'https' or not parsed.hostname or not parsed.hostname.endswith('.oaiusercontent.com') or parsed.username or parsed.password:
        raise ValueError('Unexpected source-archive host')
    request = urllib.request.Request(item['url'], headers={'User-Agent': 'Sami-Spain-Plugin-Publication/0.1.2'})
    with urllib.request.urlopen(request, timeout=40) as response:
        blob = response.read(8_000_001)
    if len(blob) > 8_000_000:
        raise ValueError('Archive exceeds size limit')
    with tempfile.TemporaryDirectory(prefix='spain-plugin-import-') as temp:
        stage = Path(temp)
        with tarfile.open(fileobj=io.BytesIO(blob), mode='r:*') as archive:
            members = archive.getmembers()
            if len(members) > 200 or sum(m.size for m in members) > 12_000_000:
                raise ValueError('Archive expansion exceeds limit')
            for member in members:
                rel = PurePosixPath(member.name)
                if rel.is_absolute() or '..' in rel.parts or member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                    raise ValueError('Unsafe archive member')
                if any(p in {'.git', '.env', '.app.json', '__pycache__', 'node_modules'} for p in rel.parts):
                    raise ValueError('Private or generated archive member')
                if member.isfile() and rel.suffix.lower() not in {'.json', '.md', '.py', '.png'} and rel.name != 'LICENSE':
                    raise ValueError('Unexpected archive file type')
            archive.extractall(stage, filter='data')
        manifests = list(stage.glob('plugin.json'))
        if not manifests:
            manifests = list(stage.glob('*/plugin.json'))
        if len(manifests) != 1:
            raise ValueError('Archive must contain one plugin root')
        package = manifests[0].parent
        portable = json.loads(manifests[0].read_text())
        if portable.get('name') != slug or portable.get('version') != '0.1.1':
            raise ValueError('Unexpected source package identity or version')
        if portable.get('apps') or portable.get('extensions', {}).get('com.openai', {}).get('apps'):
            raise ValueError('Private account bindings must not be published')
        core = package / 'skills' / slug / 'scripts/spain_suite/core.py'
        if hashlib.sha256(core.read_bytes()).hexdigest() != EXPECTED_CORE:
            raise ValueError('Source differs from the inspected and tested adapter')
        if (package / '.app.json').exists() or list(package.rglob('*.p12')) or list(package.rglob('*.pem')):
            raise ValueError('Unexpected private account material')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package, target)
        count = sum(p.is_file() for p in target.rglob('*'))
    return {'name': slug, 'imported_version': '0.1.1', 'archive_sha256': hashlib.sha256(blob).hexdigest(), 'verified_core_sha256': EXPECTED_CORE, 'file_count': count}


def main():
    path = ROOT / 'bootstrap/source-links.json'
    data = json.loads(path.read_text())
    if [x.get('name') for x in data] != SLUGS:
        raise ValueError('Expected all seven products, in the specified order')
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(import_one, data))
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    (evidence / 'source-import.json').write_text(json.dumps(results, indent=2) + '\n')
    path.unlink()
    print('Imported and verified seven complete source packages; transient source links removed.')


if __name__ == '__main__':
    main()
