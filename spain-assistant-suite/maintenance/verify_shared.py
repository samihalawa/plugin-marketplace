"""Read-only check that standalone packages match the maintained shared runtime."""
from pathlib import Path
import argparse,hashlib,json
SLUGS=['licita-espana','ayudas-espana','boe-impact','borme-intelligence','catastro-pro','ine-evidence','spain-open-data']
NAMES=['core.py','presentation.py','__main__.py','__init__.py']
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repos-root',type=Path,required=True);args=p.parse_args()
base=Path(__file__).resolve().parent/'shared/spain_suite';rows=[]
for slug in SLUGS:
 for name in NAMES:
  target=args.repos_root/slug/'skills'/slug/'scripts/spain_suite'/name
  ok=target.is_file() and target.read_bytes()==(base/name).read_bytes()
  rows.append({'product':slug,'module':name,'matches':ok})
print(json.dumps({'all_match':all(r['matches'] for r in rows),'checks':rows},indent=2))
raise SystemExit(0 if all(r['matches'] for r in rows) else 1)
