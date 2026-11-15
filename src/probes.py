"""Controlled local validator negative probes; genuine deterministic executions."""
import csv, json, tempfile
from pathlib import Path
from src.agent import run
from src.validator import validate
ROOT=Path(__file__).resolve().parents[1]
def main():
    records=[]
    with tempfile.TemporaryDirectory() as td:
        for case in ["intact","missing_brief","invalid_citation","missing_tool_result"]:
            d=Path(td)/case
            run(6,d)
            if case=="missing_brief": (d/"final-brief.md").unlink()
            if case=="invalid_citation":
                p=d/"final-brief.md";p.write_text(p.read_text(encoding="utf-8").replace("[S01:L04-L07]","[S99:L04-L07]"),encoding="utf-8")
            if case=="missing_tool_result":
                p=d/"tool-results.jsonl";p.write_text("\n".join(p.read_text(encoding="utf-8").splitlines()[:-1])+"\n",encoding="utf-8")
            a=validate(d,ROOT,6)
            failed=sorted(k for k,v in a["checks"].items() if not v)
            records.append({"condition":case,"status":a["status"],"failed_checks":";".join(failed) if failed else "none"})
    with (ROOT/"results/validator_probes.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    for r in records: print(r)
    assert [x["status"] for x in records]==["PASS","FAIL","FAIL","FAIL"]
if __name__=="__main__":main()
