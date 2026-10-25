#!/usr/bin/env python3
"""Build an art-free standalone; optional explicit --atlas creates a PRIVATE demo."""
import argparse, base64, re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--atlas',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
html=(root/'index.html').read_text(encoding='utf-8');js=(root/'tester.js').read_text(encoding='utf-8')
if a.atlas:
    if not a.output or a.output.resolve() == (root/'standalone.html').resolve():
        raise SystemExit('Private embedding requires --output separate from public standalone.html')
    raw=a.atlas.read_bytes()
    if len(raw)>20*1024*1024:raise SystemExit('Atlas exceeds 20 MiB')
    import json
    js+='\n// Private user demo; never include this generated file in public skill exports.\n'
    js+='const embeddedBytes=Uint8Array.from(atob('+json.dumps(base64.b64encode(raw).decode())+'),c=>c.charCodeAt(0));load(new File([embeddedBytes],'+json.dumps(a.atlas.name)+',{type:"image/png"}));\n'
html=html.replace('<script src="tester.js"></script>','<script>'+re.sub(r'</script', lambda match: '<\\/' + match.group()[2:], js, flags=re.IGNORECASE)+'</script>')
out=a.output or root/'standalone.html';out.write_text(html,encoding='utf-8');print(out)
