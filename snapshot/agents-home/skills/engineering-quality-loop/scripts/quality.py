#!/usr/bin/env python3
"""Local evidence recorder and consistency gate. Not a trusted release authority."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import signal
import stat
import subprocess
import sys
import time

RUBRIC = {'correctness': (.25, 9), 'verification': (.25, 9), 'security': (.15, 9),
          'reliability': (.15, 8), 'efficiency': (.10, 8), 'simplicity': (.10, 8)}
LIMIT = 1_048_576


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(), parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))


def write_new(path, value):
    # Exclusive creation keeps accidental retries from overwriting evidence.
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def words(value):
    return isinstance(value, str) and bool(value.strip())


def ident(value):
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value)


def keyed(rows, label):
    require(isinstance(rows, list), f'{label} must be a list')
    require(all(isinstance(r, dict) and ident(r.get('id')) for r in rows), f'invalid {label} ID')
    result = {r['id']: r for r in rows}
    require(len(result) == len(rows), f'duplicate {label} ID')
    return result


def validate_plan(plan):
    require(isinstance(plan, dict) and words(plan.get('task')), 'plan requires task')
    require(plan.get('risk') in ('low', 'medium', 'high'), 'plan risk must be low, medium, or high')
    criteria = keyed(plan.get('criteria'), 'criterion')
    checks = keyed(plan.get('checks'), 'check')
    require(criteria and checks, 'nonempty criteria and checks required')
    require(not ({'candidate', 'review'} & set(checks)), 'reserved check ID: candidate/review')
    require(all(words(c.get('description')) for c in criteria.values()), 'criterion description required')
    covered = set()
    for c in checks.values():
        refs = c.get('criteria')
        require(isinstance(refs, list) and refs and all(isinstance(r, str) and r in criteria for r in refs), 'invalid check criteria')
        covered.update(refs)
        require(c.get('kind') in ('command', 'observation'), 'unknown check kind')
        if c['kind'] == 'command':
            require(isinstance(c.get('argv'), list) and c['argv'] and all(words(a) for a in c['argv']), 'argv must be nonempty strings')
            t = c.get('timeout_seconds')
            require(type(t) in (int, float) and math.isfinite(t) and 0 < t <= 3600, 'timeout must be 0..3600 seconds')
        else:
            require(words(c.get('procedure')), 'observation procedure required')
    require(covered == set(criteria), 'every criterion must have a planned check')
    return criteria, checks


def snapshot(root, extra):
    root = Path(root).resolve(strict=True)
    require(root.is_dir(), 'source root must be a directory')
    git = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if git.returncode == 0:
        require(Path(git.stdout.strip()).resolve() == root, 'use repository root, not a subtree')
        names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard']).decode().split('\0')
        paths = {root / n for n in names if n}
    else:
        paths = set(root.rglob('*'))
        paths = {p for p in paths if '__pycache__' not in p.relative_to(root).parts and '.git' not in p.relative_to(root).parts}
    for name in extra:
        p = Path(name)
        require(not p.is_absolute() and '..' not in p.parts, 'extra inputs must be relative paths inside source root')
        paths.add(root / p)
        require((root / p).exists(), f'extra input missing: {name}')
    entries = []
    for p in sorted(paths):
        require(not p.is_symlink(), f'symlink needs explicit external validation; unsupported input: {p.relative_to(root)}')
        require(p.resolve().is_relative_to(root), 'input escapes source root')
        if not p.exists():  # tracked deletion participates by its absence
            continue
        if p.is_dir():
            require(git.returncode != 0, f'submodule/directory input requires separate validation: {p}')
            continue
        mode = p.stat().st_mode
        require(stat.S_ISREG(mode), f'unsupported input type: {p}')
        entries.append([str(p.relative_to(root)), stat.S_IMODE(mode), file_hash(p)])
    require(entries, 'source snapshot is empty')
    return digest(entries)


def load_candidate(run):
    c = read(run / 'candidate.json')
    claim = c.pop('id')
    require(digest(c) == claim, 'candidate metadata changed')
    c['id'] = claim
    validate_plan(c['plan'])
    return c


def fresh(c):
    require(snapshot(c['root'], c['extra_inputs']) == c['source'], 'source changed: freeze a new candidate')


def freeze(root, plan_path, run, authors, previous=None, extra=()):
    root = Path(root).resolve(strict=True)
    run = Path(run).resolve()
    require(not run.is_relative_to(root) and not root.is_relative_to(run), 'evidence and source directories must be separate')
    plan = read(plan_path)
    validate_plan(plan)
    require(authors and all(words(a) for a in authors), 'actual author IDs required')
    c = {'root': str(root), 'plan': plan, 'extra_inputs': list(extra), 'authors': sorted(set(authors)),
         'source': snapshot(root, extra), 'created_at': time.time(), 'round': 1, 'previous': None}
    if previous:
        previous = Path(previous).resolve(strict=True)
        pc = load_candidate(previous)
        pr = read(previous / 'review.json')
        require(pc['plan'] == plan and pc['root'] == str(root) and pc['extra_inputs'] == list(extra), 'plan/root/inputs changed: start a new task and explain scope change')
        require(pr.get('candidate_id') == pc['id'], 'previous review refers to wrong candidate')
        keyed(pr.get('findings'), 'previous finding')
        c['authors'] = sorted(set(c['authors'] + pc['authors']))
        c['round'] = pc['round'] + 1
        c['previous'] = {'path': str(previous), 'candidate_hash': file_hash(previous / 'candidate.json'), 'review_hash': file_hash(previous / 'review.json')}
    c['id'] = digest(c)
    run.mkdir(parents=True, exist_ok=False)
    write_new(run / 'candidate.json', c)
    return {'candidate_id': c['id'], 'round': c['round'], 'run': str(run)}


def check(run, check_id, artifacts=(), note=None, outcome=None):
    c = load_candidate(run)
    fresh(c)
    _, checks = validate_plan(c['plan'])
    require(check_id in checks, 'check was not planned')
    spec = checks[check_id]
    record_path = run / f'{check_id}.json'
    require(not record_path.exists(), 'check record exists: preserve it and freeze another candidate for a retry')
    record = {'id': check_id, 'candidate_id': c['id'], 'spec': spec, 'started_at': time.time(), 'kind': spec['kind']}
    if spec['kind'] == 'observation':
        require(artifacts and words(note) and outcome in ('pass', 'fail'), 'observation requires artifacts, note, and pass/fail outcome')
        evidence = []
        for name in artifacts:
            p = Path(name).resolve(strict=True)
            require(p.is_file() and p.stat().st_size > 0, 'artifact must be a nonempty file')
            evidence.append({'path': str(p), 'sha256': file_hash(p)})
        record.update(artifacts=evidence, note=note, outcome=outcome, provenance='operator_observation')
    else:
        require(not artifacts and note is None and outcome is None, 'observation flags cannot be used for commands')
        output = bytearray()
        total = 0
        timed_out = False
        started = time.monotonic()
        with subprocess.Popen(spec['argv'], cwd=c['root'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              stdin=subprocess.DEVNULL, start_new_session=True) as proc:
            try:
                with selectors.DefaultSelector() as sel:
                    sel.register(proc.stdout, selectors.EVENT_READ)
                    while sel.get_map() or proc.poll() is None:
                        if time.monotonic() - started >= spec['timeout_seconds']:
                            timed_out = True
                            break
                        for key, _ in sel.select(min(.1, spec['timeout_seconds'])):
                            block = os.read(key.fd, 65536)
                            if not block:
                                sel.unregister(key.fileobj)
                            else:
                                total += len(block)
                                output.extend(block[:max(0, LIMIT - len(output))])
            finally:
                # Also clean up background children after their parent exits.
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
        log = run / f'{check_id}.log'
        with log.open('xb') as f:
            f.write(output)
        record.update(exit_code=proc.returncode, timed_out=timed_out, truncated=total > LIMIT,
                      output_bytes=total, log_sha256=file_hash(log),
                      outcome='pass' if proc.returncode == 0 and not timed_out else 'fail', provenance='executed_command')
    record['finished_at'] = time.time()
    record['source_after'] = snapshot(c['root'], c['extra_inputs'])
    if record['source_after'] != c['source']:
        record['outcome'] = 'fail'
    write_new(record_path, record)
    return record


def evidence_refs(item, checks):
    refs = item.get('evidence')
    require(isinstance(refs, list) and refs and all(isinstance(r, str) and r in checks for r in refs), 'evidence must reference recorded check IDs')
    require(words(item.get('rationale')), 'evidence rationale required')


def gate(run):
    c = load_candidate(run)
    fresh(c)
    criteria, checks = validate_plan(c['plan'])
    review = read(run / 'review.json')
    require(review.get('candidate_id') == c['id'], 'review is stale')
    reviewer = review.get('reviewer', {})
    require(words(reviewer.get('id')) and reviewer['id'] not in c['authors'], 'reviewer must differ from every implementation author')
    require(reviewer.get('independent') is True and words(reviewer.get('model')), 'independent reviewer and model required')
    require(isinstance(review.get('check_hashes'), dict) and set(review['check_hashes']) == set(checks), 'review must bind every check record')
    failures = []
    for cid, spec in checks.items():
        p = run / f'{cid}.json'
        require(file_hash(p) == review['check_hashes'][cid], f'check changed after review: {cid}')
        r = read(p)
        require(r.get('candidate_id') == c['id'] and r.get('spec') == spec and r.get('id') == cid, f'wrong check record: {cid}')
        require(r.get('source_after') == c['source'], f'check modified source: {cid}')
        if spec['kind'] == 'command':
            require(r.get('provenance') == 'executed_command' and r.get('kind') == 'command', 'command provenance missing')
            require(file_hash(run / f'{cid}.log') == r.get('log_sha256'), f'log changed: {cid}')
            if type(r.get('exit_code')) is not int or r['exit_code'] != 0 or r.get('timed_out') is not False:
                failures.append(f'command failed: {cid}')
        else:
            require(r.get('provenance') == 'operator_observation' and words(r.get('note')) and r.get('artifacts'), 'observation evidence missing')
            for a in r['artifacts']:
                require(file_hash(a['path']) == a['sha256'], f'observation artifact changed: {cid}')
        if r.get('outcome') != 'pass':
            failures.append(f'check not passed: {cid}')
    specialists = review.get('specialists', [])
    require(isinstance(specialists, list), 'specialists must be a list')
    seen_reviewers = {reviewer['id']}
    for specialist in specialists:
        require(isinstance(specialist, dict) and words(specialist.get('id')), 'specialist identity required')
        require(specialist['id'] not in c['authors'] and specialist['id'] not in seen_reviewers, 'specialist must be a distinct non-author')
        seen_reviewers.add(specialist['id'])
        require(specialist.get('independent') is True and words(specialist.get('model')) and words(specialist.get('focus')), 'specialist model, focus, and independence required')
        require(specialist.get('candidate_id') == c['id'] and specialist.get('check_hashes') == review['check_hashes'], 'specialist evidence is stale')
        evidence_refs(specialist, checks)
        if specialist.get('status') != 'pass':
            failures.append('specialist review not passed')
    if c['plan']['risk'] == 'high':
        require(specialists, 'high-risk work requires a second distinct specialist')
    reviewed = keyed(review.get('criteria'), 'reviewed criterion')
    require(set(reviewed) == set(criteria), 'review must cover exactly the planned criteria')
    for cid, item in reviewed.items():
        evidence_refs(item, checks)
        require(all(cid in checks[e]['criteria'] for e in item['evidence']), f'criterion cites unrelated check: {cid}')
        if item.get('status') != 'met':
            failures.append(f'criterion unverified: {cid}')
    findings = keyed(review.get('findings'), 'finding')
    for f in findings.values():
        require(f.get('severity') in ('critical', 'high', 'medium', 'low') and type(f.get('must_fix')) is bool, 'invalid finding severity/must_fix')
        require(f.get('status') in ('open', 'resolved', 'dismissed') and words(f.get('description')), 'invalid finding')
        evidence_refs(f, checks)
        if f['status'] == 'open' and (f['must_fix'] or f['severity'] in ('critical', 'high')):
            failures.append(f'open finding: {f["id"]}')
    if c['previous']:
        prev = c['previous']
        pp = Path(prev['path'])
        require(file_hash(pp / 'candidate.json') == prev['candidate_hash'] and file_hash(pp / 'review.json') == prev['review_hash'], 'previous evidence changed')
        old = keyed(read(pp / 'review.json')['findings'], 'previous finding')
        require(set(old) <= set(findings), 'previous finding disappeared')
        for fid, f in old.items():
            require(all(findings[fid].get(k) == f.get(k) for k in ('severity', 'must_fix', 'description')), 'finding identity/severity changed')
    dimensions = review.get('dimensions')
    require(isinstance(dimensions, dict) and set(dimensions) == set(RUBRIC), 'all six dimensions required')
    total = 0
    for name, (weight, floor) in RUBRIC.items():
        d = dimensions[name]
        evidence_refs(d, checks)
        score = d.get('score')
        require(type(score) in (int, float) and math.isfinite(score) and 0 <= score <= 10, f'invalid score: {name}')
        total += weight * score
        if score < floor:
            failures.append(f'{name} below {floor}')
    if total + 1e-9 < 9:
        failures.append('weighted score below 9')
    fresh(c)
    return {'status': 'NEEDS_REPAIR' if failures else 'PASS', 'weighted_score': round(total, 3),
            'candidate_id': c['id'], 'round': c['round'], 'failures': failures,
            'limitation': 'Consistency validation only; reviewer identity, observation truth, and check quality need human/agent verification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    f = sub.add_parser('freeze')
    f.add_argument('--root', required=True, type=Path)
    f.add_argument('--plan', required=True, type=Path)
    f.add_argument('--run', required=True, type=Path)
    f.add_argument('--author', required=True, action='append')
    f.add_argument('--previous', type=Path)
    f.add_argument('--extra-input', action='append', default=[])
    ck = sub.add_parser('check')
    ck.add_argument('--run', required=True, type=Path)
    ck.add_argument('--id', required=True)
    ck.add_argument('--artifact', action='append', default=[])
    ck.add_argument('--note')
    ck.add_argument('--outcome', choices=['pass', 'fail'])
    g = sub.add_parser('gate')
    g.add_argument('--run', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'freeze':
            result = freeze(args.root, args.plan, args.run, args.author, args.previous, args.extra_input)
        elif args.action == 'check':
            result = check(args.run, args.id, args.artifact, args.note, args.outcome)
        else:
            result = gate(args.run)
        print(json.dumps(result, indent=2))
        return 1 if result.get('status') == 'NEEDS_REPAIR' or result.get('outcome') == 'fail' else 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as e:
        print(json.dumps({'status': 'BLOCKED', 'reason': str(e)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
