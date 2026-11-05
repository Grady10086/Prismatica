"""Package the dependency-free site with revisioned module URLs for GitHub Pages."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'site'

def build(out,revision):
    if not re.fullmatch(r'[A-Za-z0-9._-]{1,64}',revision):
        raise ValueError('Revision must be a short alphanumeric identifier.')
    if out.resolve()==SOURCE.resolve() or SOURCE.resolve() in out.resolve().parents:
        raise ValueError('Choose an output directory outside site/.')
    if out.exists() and any(out.iterdir()):
        raise ValueError('Output directory must be empty.')
    shutil.copytree(SOURCE,out,dirs_exist_ok=True)
    for p in out.glob('*.js'):
        p.write_text(re.sub(r'''(\bfrom\s+['"])(\./[^'"]+\.js)(['"])''',lambda m:m[1]+m[2]+'?v='+revision+m[3],p.read_text()))
    p=out/'index.html'
    html=p.read_text().replace('./styles.css','./styles.css?v='+revision).replace('./app.js','./app.js?v='+revision).replace('./studio.css','./studio.css?v='+revision).replace('./atmosphere.css','./atmosphere.css?v='+revision)
    html=html.replace('</head>','<meta name="prismatica-version" content="'+revision+'">\n</head>')
    p.write_text(html)
    (out/'.nojekyll').touch()
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--revision',default=None)
    args=parser.parse_args()
    revision=args.revision or subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=ROOT,text=True).strip()
    print(build(args.out,revision))
