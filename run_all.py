#!/usr/bin/env python3
"""Re-run both controlled conditions; uses Python standard library only."""
import csv,json,hashlib,platform,shutil
from pathlib import Path
from src.agent import run
ROOT=Path(__file__).resolve().parent

def main():
    records=[]
    for budget in (3,6):
        folder=ROOT/'runs'/f'max_steps_{budget}'
        assessment=run(budget,folder)
        calls=[json.loads(x) for x in (folder/'trajectory.jsonl').read_text(encoding='utf-8').splitlines()]
        names=[x['tool'] for x in calls]
        state=json.loads((folder/'final-state.json').read_text(encoding='utf-8'))
        records.append({'run_id':f'max_steps_{budget}','max_steps':budget,'action_calls':len(calls),
          'search_calls':names.count('search_sources'),'read_calls':names.count('read_source'),
          'write_calls':names.count('write_brief'),'validator_post_run':1,
          'sources_read':len(assessment['read_sources']),'cited_sources':len(assessment['cited_sources']),
          'brief_exists':int((folder/'final-brief.md').exists()),
          'local_validator_status':assessment['status'],'official_validator_status':'NOT_RUN',
          'halt_reason':state['halt_reason']})
        print(f'budget={budget}: {assessment["status"]}, actions={len(calls)}, reads={len(assessment["read_sources"])}')
    for name in ('final-brief.md','trajectory.jsonl','tool-results.jsonl','final-state.json','local-validation.json'):
        shutil.copy2(ROOT/'runs/max_steps_6'/name,ROOT/name)
    with (ROOT/'evaluation.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    index=json.loads((ROOT/'source-pack/index.json').read_text(encoding='utf-8'))
    prov={'artifact_id':'AT3-W11-lecture-aligned-v3','experiment_type':'deterministic_offline_fixed_workflow_fixture',
      'agent_model_used':False,'api_used':False,'network_used':False,'gpu_used':False,
      'teacher_lecture_used':True,'teacher_designated_source_pack_available':False,
      'official_validator_available':False,'official_validator_executed':False,
      'local_validator_executed':True,'python_version':platform.python_version(),
      'comparison_variable':'max_steps','conditions':[3,6],
      'fixed_task_sources_tools_validator_rubric':True,
      'validator_counts_as_action':False,'source_pack_id':index['pack_id'],
      'source_records':[{'source_id':s['source_id'],'origin_file':s['origin_file'],'source_level':s['source_level'],'sha256':s['sha256']} for s in index['sources']],
      'results':records,'caveat':'教師課堂講義已核對；但指定W11 student-kit及官方final-state validator仍未提供。自建來源包與validator不能替代官方驗收；W07為手工fixture。'}
    (ROOT/'provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files=[p for p in ROOT.rglob('*') if p.is_file() and 'manifest.sha256' not in str(p) and '__pycache__' not in str(p)]
    (ROOT/'manifest.sha256').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}\n' for p in sorted(files)),encoding='utf-8')
if __name__=='__main__':main()
