#!/usr/bin/env python3
"""Structured health checks. Required failures return 1, optional gaps degrade."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REQUIRED_SCRIPTS = ['weather_client.py', 'currency_client.py', 'holiday_check.py', 'http_client.py', 'doctor.py', 'environment.py', 'md2pdf.py', 'atlas-env.sh', 'install.sh', 'atlas-agent']
AGENTS = {'cursor': '.cursor/skills', 'claude': '.claude/skills', 'codex': '.codex/skills', 'copilot': '.agents/skills', 'hermes': '.hermes/skills/productivity'}


def run_probe(command, timeout=35):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return {'ok': result.returncode == 0, 'detail': (result.stderr or result.stdout).strip()[-1200:] if result.returncode else ''}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'ok': False, 'detail': str(exc)}


def pdf_probe(root):
    try:
        version = importlib.metadata.version('fpdf2')
        if tuple(int(n) for n in version.split('.')[:3]) < (2, 8, 4):
            return {'ok': False, 'detail': 'fpdf2 >= 2.8.4 required; found ' + version}
        try:
            importlib.metadata.distribution('fpdf')
            legacy = True
        except importlib.metadata.PackageNotFoundError:
            legacy = False
        if legacy:
            return {'ok': False, 'detail': 'Legacy PyFPDF conflicts with fpdf2; use a clean environment'}
        with tempfile.TemporaryDirectory(prefix='atlas-pdf-probe-') as folder:
            source = Path(folder) / 'probe.md'
            source.write_text('导出验证\n连续正文完整显示\n', encoding='utf-8')
            return run_probe([sys.executable, str(root / 'scripts/md2pdf.py'), str(source)], timeout=20)
    except importlib.metadata.PackageNotFoundError:
        return {'ok': False, 'detail': 'Optional fpdf2 is not installed'}


def diagnose(root, user_home, offline=False):
    root = Path(root)
    checks = {'python3': {'ok': sys.version_info >= (3, 9), 'detail': sys.version.split()[0]}, 'scripts': {'ok': all((root / 'scripts' / file).is_file() for file in REQUIRED_SCRIPTS), 'detail': ''}}
    skills = sorted(path.parent.name for path in (root / 'skills').glob('*/SKILL.md'))
    checks['skill_pack'] = {'ok': len(skills) == 9, 'detail': '{} skills found'.format(len(skills))}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {'fpdf2': pool.submit(pdf_probe, root)}
        if checks['scripts']['ok'] and not offline:
            jobs['weather_api'] = pool.submit(run_probe, [sys.executable, str(root / 'scripts/weather_client.py'), 'forecast', '--lat', '30.67', '--lon', '104.07', '--timezone', 'Asia/Shanghai', '--days', '1', '--json'])
            jobs['currency_api'] = pool.submit(run_probe, [sys.executable, str(root / 'scripts/currency_client.py'), 'convert', '1', '--from', 'USD', '--to', 'JPY', '--json'])
        for name, job in jobs.items():
            checks[name] = job.result()
    if offline:
        checks.update({name: {'ok': None, 'detail': 'Skipped (--offline)'} for name in ('weather_api', 'currency_api')})
    else:
        for name in ('weather_api', 'currency_api'):
            checks.setdefault(name, {'ok': False, 'detail': 'Runtime scripts missing'})
    installs = {}
    for agent, location in AGENTS.items():
        missing = [name for name in skills if not (Path(user_home) / location / name / 'SKILL.md').is_file()]
        installs[agent] = {'ok': bool(skills) and not missing, 'missing': missing}
    required = ['python3', 'scripts', 'skill_pack'] + ([] if offline else ['weather_api', 'currency_api'])
    ready = all(checks[name]['ok'] for name in required)
    status = 'unavailable' if not ready else 'ready' if checks['fpdf2']['ok'] and not offline and any(a['ok'] for a in installs.values()) else 'degraded'
    return {'atlas_root': str(root), 'status': status, 'checks': checks, 'installed_skills': installs, 'skill_cursor': installs['cursor']['ok'], 'skill_claude': installs['claude']['ok'], **{name: item['ok'] for name, item in checks.items()}}, 0 if ready else 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--json', action='store_true')
    p.add_argument('--offline', action='store_true')
    args = p.parse_args()
    root = os.environ.get('ATLAS_ROOT', str(Path(__file__).resolve().parents[1]))
    report, code = diagnose(root, os.environ.get('ATLAS_USER_HOME', str(Path.home())), args.offline)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print('AtlasAgent Doctor | ' + report['status'])
        print('ATLAS_ROOT: ' + report['atlas_root'])
        for name, item in report['checks'].items():
            print('  {} {} {}'.format('OK' if item['ok'] else 'SKIP' if item['ok'] is None else 'FAIL', name, item['detail']))
        for agent, item in report['installed_skills'].items():
            print('  {} skills: {}'.format(agent, 'all installed' if item['ok'] else ', '.join(item['missing']) or 'source pack missing'))
    return code


if __name__ == '__main__':
    sys.exit(main())
