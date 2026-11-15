#!/usr/bin/env python3
"""Student-built local final-state validator. Not the teacher's official validator."""
import argparse,hashlib,json,re
from pathlib import Path
CITE=re.compile(r'\[(S\d+):L(\d+)(?:-L(\d+))?\]')

def validate(run_dir,root,max_steps=None):
    run_dir=Path(run_dir);root=Path(root)
    index=json.loads((root/'source-pack/index.json').read_text(encoding='utf-8'))
    sources={x['source_id']:x for x in index['sources']}
    if max_steps is None:
        name=run_dir.name
        max_steps=int(name.rsplit('_',1)[-1]) if name.rsplit('_',1)[-1].isdigit() else 6
    trace_file=run_dir/'trajectory.jsonl';results_file=run_dir/'tool-results.jsonl';brief_file=run_dir/'final-brief.md'
    def jsonl(path):
        if not path.exists():return []
        return [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    trace=jsonl(trace_file);results=jsonl(results_file)
    actions=[x for x in trace if x.get('event')=='tool_call']
    pairs=len(actions)==len(results) and len(actions)>0
    if pairs:
        for i,(a,b) in enumerate(zip(actions,results),1):
            if a.get('step')!=i or b.get('step')!=i or a.get('observation_ref')!=b.get('observation_id') or a.get('tool')!=b.get('tool') or not a.get('success'):
                pairs=False;break
    read_ids=set()
    reads_valid=True
    for a,b in zip(actions,results):
        if a.get('tool')=='read_source':
            sid=a.get('arguments',{}).get('source_id')
            r=b.get('result',{})
            if sid not in sources or r.get('source_id')!=sid or r.get('status')!='ok':reads_valid=False;continue
            source_text=(root/'source-pack'/sources[sid]['file']).read_bytes()
            if r.get('sha256')!=hashlib.sha256(source_text).hexdigest():reads_valid=False
            else:read_ids.add(sid)
    brief=brief_file.read_text(encoding='utf-8') if brief_file.exists() else ''
    cites=list(CITE.finditer(brief));cited_ids=set();refs_valid=True
    for m in cites:
        sid=m.group(1);a=int(m.group(2));b=int(m.group(3) or m.group(2))
        if sid not in sources or sid not in read_ids:refs_valid=False;continue
        lines=(root/'source-pack'/sources[sid]['file']).read_text(encoding='utf-8').splitlines()
        if not (1<=a<=b<=len(lines)) or not any(x.strip() for x in lines[a-1:b]):refs_valid=False
        else:cited_ids.add(sid)
    written=[(a,b) for a,b in zip(actions,results) if a.get('tool')=='write_brief']
    write_recorded=len(written)==1 and written[0][1].get('result',{}).get('output')=='final-brief.md'
    if write_recorded:
        write_recorded=written[0][1]['result'].get('chars')==len(brief)
    checks={
      'brief_nonempty':bool(brief.strip()) and 350<=len(brief)<=1800,
      'brief_has_research_question_and_conclusion':'研究問題' in brief and '結論' in brief,
      'three_unique_citations':len(cited_ids)>=3 and len(cites)>=3,
      'citations_from_read_sources':refs_valid,
      'three_distinct_sources_read':len(read_ids)>=3 and reads_valid,
      'action_count_within_budget':len(actions)<=max_steps,
      'five_actions_for_success':len(actions)==5,
      'tool_observation_matching':pairs,
      'search_and_write_recorded':any(a.get('tool')=='search_sources' for a in actions) and write_recorded,
      'allowed_tool_names':all(a.get('tool') in {'search_sources','read_source','write_brief'} for a in actions),
      'output_path_safety':brief_file.parent.resolve()==run_dir.resolve(),
      'source_pack_non_official_disclosed':index.get('official_w11_pack') is False,
    }
    status='PASS' if all(checks.values()) else 'FAIL'
    return {'validator':'student-built-W11-lecture-aligned-v3','official_teacher_validator':False,'status':status,
            'checks':checks,'max_steps':max_steps,'action_count':len(actions),'read_sources':sorted(read_ids),
            'cited_sources':sorted(cited_ids),'citation_count':len(cites),'brief_chars':len(brief),
            'caveat':'checks verify structural provenance and line validity, not semantic entailment of every claim'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);ap.add_argument('--root');ap.add_argument('--max-steps',type=int);a=ap.parse_args()
    root=Path(a.root) if a.root else Path(__file__).resolve().parents[1]
    result=validate(Path(a.run),root,a.max_steps)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)
if __name__=='__main__':main()
