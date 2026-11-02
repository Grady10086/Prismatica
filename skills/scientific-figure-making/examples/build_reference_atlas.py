"""Render a local, searchable atlas of inspected paper figures.

Requires PyMuPDF and locally supplied PDFs named as in the catalog. No network
requests. Published excerpts are reference evidence, not new experimental results.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
import json
import math
from pathlib import Path
import re
from urllib.parse import urlparse


def validate(catalog):
    seen = set()
    for e in catalog['entries']:
        if not re.fullmatch(r'[a-z0-9-]+',e['id']) or e['id'] in seen:
            raise ValueError('Catalog IDs must be unique lowercase slugs')
        seen.add(e['id'])
        if Path(e['pdf_file']).name != e['pdf_file']:
            raise ValueError('PDF filenames must not escape the supplied PDF directory')
        if not isinstance(e['page'],int) or e['page'] < 1:
            raise ValueError('Page must be a positive integer')
        crop=e['crop']
        if len(crop)!=4 or not all(isinstance(n,(int,float)) and math.isfinite(n) for n in crop):
            raise ValueError('Crop must contain four finite normalized coordinates')
        x0,y0,x1,y1=crop
        if not (0<=x0<x1<=1 and 0<=y0<y1<=1):raise ValueError('Invalid normalized crop')
        for url in [e['source_url']]+([e['award']['source_url']] if e['award'] else []):
            if urlparse(url).scheme not in {'https','http'}:raise ValueError('Expected a web source URL')
        if e['selection']=='award' and not e['award']:raise ValueError('Award selections require an official award source')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog',type=Path,default=Path(__file__).parents[1]/'references/recent-paper-figures.json')
    p.add_argument('--pdf-dir',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();catalog=json.loads(args.catalog.read_text());validate(catalog)
    # Check source-file availability before writing output.
    for e in catalog['entries']:
        if not (args.pdf_dir/e['pdf_file']).is_file():raise ValueError(f"Missing local PDF: {e['pdf_file']}")
    import pymupdf
    records=[];cards=[]
    args.out.mkdir(parents=True,exist_ok=True)
    for e in catalog['entries']:
        path=args.pdf_dir/e['pdf_file']
        with pymupdf.open(path) as doc:
            if e['page']>len(doc):raise ValueError(f"Page exceeds document: {e['id']}")
            page=doc[e['page']-1];w,h=page.rect.width,page.rect.height
            x0,y0,x1,y1=e['crop'];clip=pymupdf.Rect(x0*w,y0*h,x1*w,y1*h)
            image=e['id']+'.png';page.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=clip,alpha=False).save(args.out/image)
        record=dict(e,pdf_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    transform='Original PDF figure region rasterized at 144 dpi; no content edits')
        records.append(record)
        title=escape(e['title']);url=escape(e['source_url'],quote=True)
        if e['award']:
            badge=f'<a href="{escape(e["award"]["source_url"],quote=True)}">{escape(e["award"]["label"])}</a>'
        else:badge='Representative model report · no award claimed'
        tags=' '.join(e['tags']);search=escape(' '.join([e['title'],e['venue'],tags,e['mode']]).lower(),quote=True)
        cards.append(f'''<article id="{e['id']}" data-search="{search}" data-mode="{e['mode']}">
          <div class="meta">{escape(e['venue'])} {e['year']} · {badge}</div>
          <h2>{title}</h2><a href="{image}"><img loading="lazy" src="{image}" alt="{title}: {escape(e['figure'],quote=True)}"></a>
          <div class="links"><a href="{url}#page={e['page']}">Original paper · p. {e['page']} · {escape(e['figure'])}</a></div>
          <p><b>Observed</b> {escape(e['observed'])}</p><p><b>Adaptation</b> {escape(e['adaptation'])}</p>
          <p class="caution">{escape(e['avoid'])}</p><small>{escape(tags)}</small></article>''')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Recent paper figure references · Beautify</title><style>
    *{box-sizing:border-box}body{margin:0;background:#f4f5f7;color:#202126;font:16px/1.5 Arial,sans-serif}
    header,main{max-width:1440px;margin:auto;padding:32px}header{padding-bottom:12px}h1{font-size:36px;margin:0 0 10px}
    header p{max-width:1000px;color:#626671}input,select{padding:12px;border:1px solid #cdd0d6;border-radius:6px;background:white;font:inherit}
    input{width:min(65%,640px)}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
    article{background:white;border:1px solid #dfe2e7;border-radius:10px;padding:24px;overflow:hidden}
    article[hidden]{display:none}h2{font-size:21px;line-height:1.3;margin:10px 0 20px}.meta,small,.links{font-size:13px}
    .meta{color:#656a75}a{color:#332288}img{width:100%;height:350px;object-fit:contain;background:white;display:block}
    .links{margin:12px 0 20px}article p{font-size:14px;margin:10px 0}article b{display:block}.caution{color:#666b75}
    @media(max-width:850px){main{grid-template-columns:1fr}header,main{padding:20px}h1{font-size:28px}img{height:auto}}
    </style><header><h1>Recent paper figure references</h1><p>2025–2026 conference editions · __COUNT__ inspected papers · Published reference images, not new results.
    Award labels link to official announcements. “Adaptation” is editorial guidance, not a claim made by the paper.</p>
    <input id="search" aria-label="Search references" placeholder="Search: video, 3D, robotics, material, CVPR…">
    <select id="mode" aria-label="Reference type"><option value="all">All figure types</option><option value="teaser">Teaser / visual results</option><option value="analysis">Quantitative analysis</option></select>
    <p><small>Original authors retain their image rights. Local study excerpts are not a redistributable asset library.</small></p></header><main>'''+''.join(cards)+'''</main>
    <script>const q=document.querySelector('#search'),m=document.querySelector('#mode');
    function filter(){document.querySelectorAll('article').forEach(a=>{a.hidden=!a.dataset.search.includes(q.value.trim().toLowerCase())||(m.value!=='all'&&a.dataset.mode!==m.value)})}
    q.addEventListener('input',filter);m.addEventListener('change',filter);</script></html>'''
    (args.out/'index.html').write_text(html.replace('__COUNT__',str(len(records))))
    (args.out/'provenance.json').write_text(json.dumps({'verified_at':catalog['verified_at'],'entries':records},indent=2)+'\n')
    print(f"Rendered {len(records)} inspected figures to {args.out/'index.html'}")


if __name__=='__main__':main()
