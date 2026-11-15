#!/usr/bin/env python3
"""Fixed offline workflow fixture, NOT an LLM/dynamic agent. No network or packages."""
import argparse,hashlib,json,re
from pathlib import Path
from .validator import validate
ROOT=Path(__file__).resolve().parents[1]
QUERY='Agent workflow 安全 證據 檢索'

def sources():return json.loads((ROOT/'source-pack/index.json').read_text(encoding='utf-8'))['sources']

def search_sources(query):
    tokens=query.lower().split()
    hits=[]
    for s in sources():
        hay=(s['title']+' '+' '.join(s['keywords'])).lower()
        score=sum(t in hay for t in tokens)
        if score:
            lines=(ROOT/'source-pack'/s['file']).read_text(encoding='utf-8').splitlines()
            hits.append({'source_id':s['source_id'],'title':s['title'],'score':score,'preview':lines[3][:130]})
    hits.sort(key=lambda x:(-x['score'],x['source_id']))
    return {'query':query,'hits':hits,'hit_count':len(hits)}

def read_source(source_id):
    s=next((x for x in sources() if x['source_id']==source_id),None)
    if s is None:raise ValueError('source_not_found: use a source_id returned by search_sources')
    text=(ROOT/'source-pack'/s['file']).read_text(encoding='utf-8')
    return {'source_id':source_id,'title':s['title'],'sha256':hashlib.sha256(text.encode()).hexdigest(),
            'numbered_text':'\n'.join(f'L{i:02d} {line}' for i,line in enumerate(text.splitlines(),1)),
            'line_count':len(text.splitlines()),'status':'ok'}

BRIEF="""# Agent與固定Workflow的差異：證據鏈、驗收與安全邊界

**研究問題：** 固定Workflow與動態Agent如何決定下一步？怎樣證明其工作完成且未越過安全邊界？

## 核心比較與證據

**決策方式。** 固定Workflow按預先定義的流程調用工具；動態Agent則依state和observation由模型選擇下一步。動態性並不自動帶來更高可靠性，兩者都需要清楚的task contract、授權與最終驗收。[S01:L04-L07]

**安全與有效性。** W03對GAF-Guard的二手文獻整理描述了Agent式風險識別、工具啟動和持續監控，但也指出大規模對比實驗不足。因此，不能僅憑「使用Agent」就宣稱更安全。[S02:L03-L07]

**檢索證據風險。** W07手工fixture中，不相關金融句T07在「river bank」查詢時排第3（0.690192），查詢改寫後仍第3（0.168371）。Top-3命中不等於可引用證據，必須讀取來源並核對主張。[S03:L03-L07]

## 受控實驗與結論

本次使用同一離線來源包、固定工具和本地validator，只改`max_steps`：3步完成搜尋及兩次閱讀，無簡報，驗證FAIL；6步預算下實際使用5次action（搜尋1＋閱讀3＋寫入1），生成含三來源引用的簡報，驗證PASS。驗證不計入action。[S01:L08-L10]

**結論：** 本實驗證明工具預算和來源核查會影響固定流程的完成狀態，不能推論動態LLM Agent的能力優劣。結構化驗證能檢查檔案與引文形式，語意支持仍需人工核對。[S01:L07-L10]

**限制與下一步：** 來源包與validator為本地自建，並非教師W11官方套件；W03是二手筆記，W07是手工fixture。下一步應以教師指定來源包重跑，並加入引文對應主張的人工評閱。
"""

def write_brief(run_dir,reads):
    if len(reads)!=3:raise RuntimeError('need three distinct read sources')
    for sid,a,b in re.findall(r'\[(S\d+):L(\d+)(?:-L(\d+))?\]',BRIEF):
        if sid not in reads:raise RuntimeError('citation source not read: '+sid)
        s=next(x for x in sources() if x['source_id']==sid)
        lines=(ROOT/'source-pack'/s['file']).read_text(encoding='utf-8').splitlines()
        if not 1<=int(a)<=int(b or a)<=len(lines):raise ValueError('invalid citation line range')
    target=run_dir/'final-brief.md'
    target.write_text(BRIEF,encoding='utf-8')
    return {'output':'final-brief.md','chars':len(BRIEF),'citations':len(re.findall(r'\[S\d+:L',BRIEF)),'status':'ok'}

def run(max_steps,run_dir):
    if max_steps<1:raise ValueError('max_steps must be positive')
    run_dir=Path(run_dir);run_dir.mkdir(parents=True,exist_ok=True)
    for name in ['final-brief.md','trajectory.jsonl','tool-results.jsonl','local-validation.json','final-state.json']:
        p=run_dir/name
        if p.exists():p.unlink()
    state={'searched':False,'candidates':[],'reads':{},'written':False}
    trace=[];results=[]
    for step in range(1,max_steps+1):
        if not state['searched']:
            tool='search_sources';args={'query':QUERY};why='先搜尋離線來源清單，取得合法ID'
            result=search_sources(**args);state['searched']=True;state['candidates']=[x['source_id'] for x in result['hits']]
        elif len(state['reads'])<3:
            sid=next((x for x in state['candidates'] if x not in state['reads']),None)
            if sid is None:break
            tool='read_source';args={'source_id':sid};why='只有讀取全文後才可引用其證據'
            result=read_source(**args);state['reads'][sid]=result
        elif not state['written']:
            tool='write_brief';args={'source_ids':sorted(state['reads'])};why='已讀三來源，寫入指定一頁簡報'
            result=write_brief(run_dir,state['reads']);state['written']=True
        else:break
        ref=f'obs-{step:02d}'
        trace.append({'event':'tool_call','step':step,'tool':tool,'arguments':args,'action_reason':why,'observation_ref':ref,'success':True,
                      'state_after':{'sources_read':sorted(state['reads']),'brief_written':state['written'],'remaining_budget':max_steps-step}})
        results.append({'observation_id':ref,'step':step,'tool':tool,'result':result})
    (run_dir/'trajectory.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in trace),encoding='utf-8')
    (run_dir/'tool-results.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in results),encoding='utf-8')
    # Post-run final-state validation: NOT a counted tool action (W11 lecture p43).
    outcome=validate(run_dir,ROOT,max_steps=max_steps)
    (run_dir/'local-validation.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state_out={'max_steps':max_steps,'action_count':len(trace),'sources_read':sorted(state['reads']),
               'brief_written':state['written'],'validator_counts_as_action':False,
               'local_validator_status':outcome['status'],'halt_reason':'success' if outcome['status']=='PASS' else 'max_steps_exhausted'}
    (run_dir/'final-state.json').write_text(json.dumps(state_out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return outcome

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-steps',type=int,required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    print(json.dumps(run(a.max_steps,Path(a.out)),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
