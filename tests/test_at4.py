import csv,json,tempfile,unittest
from pathlib import Path
from src.agent import run
from src.validator import validate
from src.analyze import analyze
ROOT=Path(__file__).resolve().parents[1]
class AT4Tests(unittest.TestCase):
 def test_retrieval(self):
  v=analyze();self.assertEqual(v['q01']['precision_at_3'],round(2/3,6));self.assertEqual(v['q02']['irrelevant_T07_score'],0.168371)
 def test_budget(self):
  with tempfile.TemporaryDirectory() as d:
   a=run(3,Path(d)/'a');b=run(6,Path(d)/'b')
   self.assertEqual(a['status'],'FAIL');self.assertEqual(b['status'],'PASS')
 def test_negative_cases(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);run(6,p);(p/'final-brief.md').unlink();self.assertEqual(validate(p,ROOT,6)['status'],'FAIL')
if __name__=='__main__':unittest.main()
