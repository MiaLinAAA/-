import csv,json,tempfile,unittest
from pathlib import Path
from src.agent import run
from src.validator import validate
ROOT=Path(__file__).resolve().parents[1]
class W11Tests(unittest.TestCase):
    def test_core_artifacts(self):
        for name in ('final-brief.md','task-contract.json','tool-schema.json','trajectory.jsonl','tool-results.jsonl','evaluation.csv','error-note.md','provenance.json','analysis.md'):
            self.assertTrue((ROOT/name).is_file(),name)
    def test_comparison(self):
        with (ROOT/'evaluation.csv').open(encoding='utf-8-sig') as f:
            r={int(x['max_steps']):x for x in csv.DictReader(f)}
        self.assertEqual(r[3]['local_validator_status'],'FAIL')
        self.assertEqual(r[6]['local_validator_status'],'PASS')
        self.assertEqual(r[3]['action_calls'],'3')
        self.assertEqual(r[6]['action_calls'],'5')
        self.assertEqual(r[6]['validator_post_run'],'1')
    def test_reproducible(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(run(3,Path(t)/'a')['status'],'FAIL')
            self.assertEqual(run(6,Path(t)/'b')['status'],'PASS')
    def test_validator_rejects_missing_brief(self):
        with tempfile.TemporaryDirectory() as t:
            run(6,Path(t))
            (Path(t)/'final-brief.md').unlink()
            self.assertEqual(validate(Path(t),ROOT,6)['status'],'FAIL')
    def test_validator_rejects_fake_citation(self):
        with tempfile.TemporaryDirectory() as t:
            run(6,Path(t))
            p=Path(t)/'final-brief.md'
            p.write_text(p.read_text(encoding='utf-8').replace('[S01:L04-L07]','[S99:L04-L07]'),encoding='utf-8')
            self.assertEqual(validate(Path(t),ROOT,6)['status'],'FAIL')
    def test_validator_rejects_trace_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            run(6,Path(t))
            p=Path(t)/'tool-results.jsonl';p.write_text('\n'.join(p.read_text(encoding='utf-8').splitlines()[:-1])+'\n',encoding='utf-8')
            self.assertEqual(validate(Path(t),ROOT,6)['status'],'FAIL')
if __name__=='__main__':unittest.main()
