"""Check the self-contained distributable boundary; not a privacy or rights audit."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def validate(root):
    root = Path(root).resolve()
    errors = []
    policy = json.loads((root / 'public-export-allowlist.json').read_text())
    allowed = set(policy['allowed_roots'])
    binaries = set(policy['allowed_binary_assets'])
    count = 0
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part in {'.venv', '__pycache__', '.git', '.cache', 'node_modules'} for part in relative.parts):
            errors.append(f'private/cache path: {relative}')
            continue
        if path.is_symlink():
            errors.append(f'symlink not permitted: {relative}')
            continue
        if relative.parts[0] not in allowed:
            errors.append(f'unlisted package root: {relative}')
        if not path.is_file():
            continue
        count += 1
        media = {'.png', '.gif', '.jpg', '.jpeg', '.webp', '.mp4', '.mov', '.zip', '.svg'}
        synthetic = binaries | {'assets/workflow.zh-CN.svg', 'assets/language-en.svg', 'assets/language-zh-CN.svg', 'tools/line-art-rig/rest.svg', 'tools/line-art-rig/microgesture.svg'}
        if path.suffix.lower() in media and relative.as_posix() not in synthetic:
            errors.append(f'non-synthetic media: {relative}')
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            if relative.as_posix() not in binaries:
                errors.append(f'unlisted binary: {relative}')
            continue
        if path.suffix.lower() != '.md':
            continue
        # Fenced code examples are templates, not rendered navigation links.
        content = re.sub(r'```.*?```', '', content, flags=re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', content):
            href = match.group(1).strip('<>')
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root):
                errors.append(f'link escapes package: {relative}: {href}')
            elif not target.exists():
                errors.append(f'missing link: {relative}: {href}')
    for required in ['SKILL.md', 'VERSION', 'requirements.txt', 'scripts/preflight.py']:
        if not (root / required).is_file():
            errors.append(f'missing required file: {required}')
    return {'ok': not errors, 'files_checked': count, 'errors': errors,
            'scope': 'local package paths, binary allowlist and Markdown file targets; not host discovery, privacy certification or native integration'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    result = validate(parser.parse_args().root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
