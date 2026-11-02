"""Prepare six local composition studies from inspected published PDF editions.

No download or redistribution of paper images. Supply the cited PDFs locally.
Version signatures fail closed if an edition rearranges its embedded figures.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import pymupdf


class Extractor:
    def __init__(self, path, out, prefix):
        self.doc = pymupdf.open(path)
        self.hash = hashlib.sha256(path.read_bytes()).hexdigest()
        self.out, self.prefix, self.assets = out, prefix, {}

    def get(self, key, page, index, size):
        info = self.doc[page-1].get_image_info(xrefs=True)[index]
        if [info['width'], info['height']] != list(size):
            raise ValueError(f'{self.prefix}: unexpected figure signature at page {page}, image {index}')
        image = self.doc.extract_image(info['xref'])
        masked = bool(image.get('smask'))
        if masked:
            pix = pymupdf.Pixmap(self.doc, info['xref'])
            if pix.alpha: pix = pymupdf.Pixmap(pix, 0)
            pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(self.doc, image['smask']))
            payload, extension = pix.tobytes('png'), 'png'
        else:
            payload, extension = image['image'], image['ext']
        name = f'{self.prefix}-{key}.{extension}'
        (self.out/name).write_bytes(payload)
        self.assets[key] = {'file': name, 'size': list(size), 'source_page': page,
            'source_image_index': index, 'source_bbox': list(info['bbox']),
            'source_pdf_sha256': self.hash,
            'extraction': 'PDF color image plus original soft alpha mask, lossless PNG' if masked else 'Original embedded raster bytes'}
        return {'asset': key}


def manifest(layout, title, category, label, url, assets, **fields):
    return {'layout': layout, 'title': title, 'category': category,
        'kind': 'PUBLISHED REFERENCE STUDY', 'source_label': label, 'source_url': url,
        'rights_note': 'Published reference composition; no new inference. Retain asset-specific credits and reuse terms. Extracted assets are local studies, not bundled in the skill.',
        'assets': assets, **fields}


def five_samples(asset, size):
    """Editorial crops retain the five shown panels, in original left-to-right order.

    Omit existing player controls at the bottom, not scene content. No fabricated
    timestamps: the paper does not establish equal temporal spacing.
    """
    w, h = size
    return [{'asset': asset, 'sample_order': i+1,
             'crop': [round(i*w/5)+20, 0, round((i+1)*w/5)-round(i*w/5)-40, int(h*.88)]}
            for i in range(5)]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dynamicrafter', type=Path, required=True, help='ECCV 2024 proceedings PDF, 06298.pdf')
    p.add_argument('--wonder3d', type=Path, required=True, help='CVPR 2024 open-access proceedings PDF')
    p.add_argument('--pi0', type=Path, required=True, help='Physical Intelligence original pi0.pdf, Fig. 6 and 10')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    video = Extractor(args.dynamicrafter, args.out, 'dynamicrafter')
    # Figure 4: rows preserve the original paper method and left-to-right samples.
    methods = [('PikaLabs', [1, 15, 16, 2]), ('SVD', [3, 10, 11, 4]),
               ('DynamiCrafter', [6, 9, 7, 8])]
    rows = []
    for name, indices in methods:
        refs = [video.get(f'{name.lower()}-{j+1}', 10, idx, [1024, 576]) for j,idx in enumerate(indices)]
        rows.append({'label': name, 'highlight': name == 'DynamiCrafter', 'frames': refs})
    source_input = video.get('input', 10, 5, [629, 354])
    label = 'DynamiCrafter · ECCV 2024 · Fig. 4'
    url = 'https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06298.pdf'
    movie = rows[-1]['frames']
    studies = [manifest('video-cinema', 'A still image, set in motion', 'VIDEO GENERATION', label, url,
                       video.assets, input=source_input, frames=movie,
                       detail={'asset': movie[-1]['asset'], 'crop': [450, 40, 550, 282]}),
               manifest('video-proofsheet', 'One condition. Three motion results.', 'VIDEO COMPARISON', label, url,
                        video.assets, rows=rows)]

    shape = Extractor(args.wonder3d, args.out, 'wonder3d')
    source_input = shape.get('input', 1, 6, [627,636])
    geometry = shape.get('geometry', 1, 37, [556,560])
    hero = shape.get('textured', 1, 39, [538,577])
    normals = [shape.get('normal-front',1,8,[256,256]),shape.get('normal-back',1,10,[256,256])]
    colors = [shape.get('color-front',1,9,[256,256]),shape.get('color-back',1,7,[256,256])]
    gallery = [shape.get('lion',1,52,[515,497]),shape.get('chair',1,55,[562,545]),
               shape.get('burger',1,48,[471,421]),shape.get('rock',1,42,[661,639])]
    url = 'https://openaccess.thecvf.com/content/CVPR2024/papers/Long_Wonder3D_Single_Image_to_3D_using_Cross-Domain_Diffusion_CVPR_2024_paper.pdf'
    studies.append(manifest('object-stage','One image, multiple 3D views','SINGLE-IMAGE 3D',
        'Wonder3D · CVPR 2024 · Fig. 1',url,shape.assets,
        input=source_input,geometry=geometry,hero=hero,normals=normals,colors=colors,gallery=gallery))
    grid = Extractor(args.wonder3d, args.out, 'wonder3d-comparison')
    grid.get('figure',6,30,[3444,1942])
    # Preserve the original geometry/texture sheet as a unit: some neighboring
    # object rows overlap, so slicing individual objects could clip real surfaces.
    studies.append(manifest('geometry-comparison','Reconstructed surfaces, side by side','3D RESULT COMPARISON',
        'Wonder3D · CVPR 2024 · Fig. 5 · geometry and texture',url,grid.assets,
        columns=['Input','Wonder3D','SyncDreamer','One-2345','Shap-E'],
        column_centers=[.067,.255,.47,.68,.895],
        overview={'asset':'figure','crop':[0,0,3444,1845]}))

    robot = Extractor(args.pi0,args.out,'pi0')
    tasks = {}
    specs = [('Fold a shirt',7,0,[3680,558]),('Bag groceries',7,2,[3262,412]),
             ('Stack bowls',9,1,[4835,720]),('Load a microwave',9,3,[4975,576]),
             ('Pack a drawer',9,5,[4400,630]),('Replace paper towel',9,4,[3405,367])]
    for i,(label,page,index,size) in enumerate(specs):
        key=f'task-{i+1}';robot.get(key,page,index,size)
        tasks[label]={'label':label,'frames':five_samples(key,size)}
    url='https://www.physicalintelligence.company/download/pi0.pdf'
    studies.append(manifest('robot-diptych','Manipulation, across two tasks','ROBOT MANIPULATION',
        'Physical Intelligence · pi0 · Figs. 6 & 10',url,robot.assets,
        tasks=[tasks[n] for n in ['Fold a shirt','Load a microwave']]))
    studies.append(manifest('task-mosaic','Everyday objects. Different manipulations.','ROBOT TASK COLLECTION',
        'Physical Intelligence · pi0 · Figs. 6 & 10',url,robot.assets,
        tasks=[tasks[n] for n in ['Stack bowls','Pack a drawer','Replace paper towel','Bag groceries']]))
    for m in studies:
        # Keep each manifest minimal: only referenced assets, no unused source pictures.
        referenced=set()
        def visit(v):
            if isinstance(v,dict):
                if 'asset' in v: referenced.add(v['asset'])
                for k,c in v.items():
                    if k!='assets': visit(c)
            elif isinstance(v,list):
                for c in v:visit(c)
        visit(m);m['assets']={k:v for k,v in m['assets'].items() if k in referenced}
        (args.out/(m['layout']+'.json')).write_text(json.dumps(m,indent=2)+'\n')
        print('Prepared',m['layout'])


if __name__=='__main__':main()
