"""Prepare local, attributed design-reference manifests from inspected paper PDFs.

Requires pymupdf. No downloads. Images are extracted unchanged, not generated.
Keep prepared images outside the repository; this is not an asset reuse license.
Expected sources/versions and limitations: references/result-first-teasers.md.
"""
import argparse
import json
from pathlib import Path


def main():
    import pymupdf
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--instruct',type=Path,required=True,help='InstructPix2Pix arXiv v2 PDF')
    p.add_argument('--llava',type=Path,required=True,help='Visual Instruction Tuning arXiv v2 PDF')
    p.add_argument('--robot',type=Path,required=True,help='Official pi0 PDF with six-frame Fig. 2')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    def extract(pdf,page,index,name,expected):
        with pymupdf.open(pdf) as doc:
            images=doc[page].get_images()
            if index>=len(images):raise ValueError('PDF differs from inspected version')
            data=doc.extract_image(images[index][0])
            size=[data['width'],data['height']]
            if size!=expected:raise ValueError(f'{name}: unexpected source dimensions {size}')
            file=f'{name}.{data["ext"]}';(a.out/file).write_bytes(data['image'])
            return {'file':file,'size':size,'source_page':page+1}
    kind='PUBLISHED REFERENCE STUDY'
    cc='Paper is marked CC BY 4.0; third-party depicted material may have separate rights. Local reference specimen; raster assets are not bundled in the skill.'
    edits={}
    for key,index,size in [('input',5,[512,512]),('output',4,[512,512]),
                           ('flowers_input',8,[448,576]),('flowers_output',9,[448,576]),
                           ('weather_input',10,[512,448]),('weather_output',11,[512,448])]:
        edits[key]=extract(a.instruct,0,index,'edit-'+key,size)
    editing={
        'layout':'editing-atlas','kind':kind,'eyebrow':'IMAGE EDITING / PUBLISHED REFERENCE',
        'title':'Image editing through natural instructions','assets':edits,
        'instruction':'Add fireworks to the sky.',
        'note':'The original input is paired with the paper’s edited output. Smaller pairs show different edit categories.',
        'pairs':[{'before':'flowers_input','after':'flowers_output','label':'Flower substitution'},
                 {'before':'weather_input','after':'weather_output','label':'Weather transformation'}],
        'output_note':'Published examples, rearranged for this composition study; no new inference.',
        'source_label':'Brooks, Holynski & Efros · InstructPix2Pix, CVPR 2023 · Fig. 1',
        'source_url':'https://arxiv.org/abs/2211.09800v2','rights_note':cc}
    photo=extract(a.llava,5,0,'llava-input',[1657,1112])
    case={
        'layout':'visual-case','kind':kind,'eyebrow':'MULTIMODAL UNDERSTANDING / PUBLISHED REFERENCE',
        'title':'Visual reasoning in an unusual scene','assets':{'image':photo},
        'detail_crop':[620,85,440,800],
        'response_summary':'The paper’s response recognizes ironing on a vehicle as an unusual activity for this setting.',
        'question':'What is unusual about this image?',
        'note':'The input photo and the benchmark summary are separate evidence items. The chart reports aggregate benchmark scores, not a score for this single image.',
        'metric_label':'LLaVA-Bench (In-the-Wild), All',
        'results':[{'name':'LLaVA','value':67.3,'std':2.0},
                   {'name':'BLIP-2','value':38.1,'std':1.0},
                   {'name':'OpenFlamingo','value':19.1,'std':0.4}],
        'source_label':'Liu et al. · Visual Instruction Tuning, NeurIPS 2023 · Tables 3, 5',
        'source_url':'https://arxiv.org/abs/2304.08485v2','rights_note':cc}
    seq=extract(a.robot,1,0,'pi0-sequence',[3950,540])
    bounds=[(11,793),(811,576),(1394,576),(1977,575),(2562,575),(3146,793)]
    labels=['Initial shown view','Dryer interaction','Transport',
            'At the folding table','Garment manipulation','Final shown view']
    robot={
        'layout':'robot-ribbon','kind':kind,'eyebrow':'LONG-HORIZON MANIPULATION / PUBLISHED REFERENCE',
        'title':'Long-horizon manipulation in everyday environments',
        'assets':{'sequence':seq},'task':'Laundry manipulation',
        'description':'The published sequence follows a mobile manipulator through retrieving laundry, transporting it to a table and manipulating garments. Frames keep their original order.',
        'frames':[{'crop':[x,0,w,540],'label':label} for (x,w),label in zip(bounds,labels)],
        'source_label':'Black et al. / Physical Intelligence · π₀ · Fig. 2',
        'source_url':'https://www.physicalintelligence.company/download/pi0.pdf',
        'rights_note':'Official paper is not an open asset library. Local design-reference specimen; retain original credit and check reuse permission before publishing the raster material.'}
    for name,m in [('editing',editing),('multimodal',case),('robotics',robot)]:
        (a.out/f'{name}.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
    print(f'Prepared three source-attributed manifests in {a.out}')


if __name__=='__main__':main()
