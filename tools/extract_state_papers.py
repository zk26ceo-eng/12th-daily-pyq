#!/usr/bin/env python3
from pathlib import Path
import csv, json, re, subprocess, urllib.request

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'pyq-bank'/'state-boards'
UA='12th-daily-pyq/0.1 official-source-extractor'

def extract_text(pdf):
    try:
        p=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,text=True,timeout=90)
        return re.sub(r'\s+',' ',p.stdout or '').strip()
    except Exception:return ''

def question_chunks(text):
    if not text:return []
    pieces=re.split(r'(?=(?:Q(?:uestion)?\s*)?\d+\s*[.)])',text,flags=re.I)
    out=[]
    for p in pieces:
        p=p.strip(' .')
        if 30<=len(p)<=1000: out.append(p[:900])
    return out[:80]

def main():
    downloaded=0; extracted=0
    for board in sorted(p for p in STATE.iterdir() if p.is_dir() and p.name not in {'others-TODO'}):
        meta=json.loads((board/'sources.json').read_text(encoding='utf-8'))
        rows=list(csv.DictReader((board/'questions.csv').open(encoding='utf-8')))
        for src in meta['pyq_sources']:
            url=src.get('url','')
            if not url: continue
            year=str(src['year']); subject=src['subject']
            safe=re.sub(r'[^A-Za-z0-9.-]+','_',subject)
            pdf=board/'downloads'/f'{year}_{safe}.pdf'; pdf.parent.mkdir(exist_ok=True)
            try:
                if not pdf.exists() or pdf.stat().st_size<500:
                    req=urllib.request.Request(url,headers={'User-Agent':UA})
                    with urllib.request.urlopen(req,timeout=60) as r: pdf.write_bytes(r.read())
                    downloaded+=1
                text=extract_text(pdf); chunks=question_chunks(text)
                if chunks:
                    for chunk in chunks:
                        rows.append({'question':chunk,'year':year,'subject':subject,'topic':'unclassified','board':meta['board'],'source_url':url})
                    extracted+=len(chunks)
            except Exception as e:
                print('download/extract failed',board.name,url,e)
        with (board/'questions.csv').open('w',newline='',encoding='utf-8') as f:
            fields=['question','year','subject','topic','board','source_url']; w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print('downloaded',downloaded,'pdfs; extracted',extracted,'question chunks')

if __name__=='__main__': main()
