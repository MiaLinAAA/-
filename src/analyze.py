"""Analyze actual provided W07 teacher-fixture results and W11 run evidence.
No inference model is called; no external data or internet is required.
"""
import csv, json, hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def read_json(p):return json.loads(p.read_text(encoding="utf-8"))
def analyze():
    d=BASE/"data/w07_fixture"
    a=read_json(d/"retrieval_top3_Q01.json")
    b=read_json(d/"retrieval_top3_Q02.json")
    rows=[]
    for q,data in [("Q01",a),("Q02",b)]:
        ids=[r["passage_id"] for r in data]
        scores={r["passage_id"]:float(r["score"]) for r in data}
        assert ids[:2]==(["T08","T09"] if q=="Q01" else ["T09","T08"])
        assert ids[2]=="T07"
        rows.append({"query_id":q,"relevant_in_top3":2,"retrieved":3,
          "precision_at_3":round(2/3,6),"irrelevant_T07_rank":3,
          "irrelevant_T07_score":scores["T07"],
          "mean_relevant_score":round((scores["T08"]+scores["T09"])/2,6)})
    w=BASE/"results/retrieval_summary.csv"
    with w.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    combined={"fixture_type":"handcrafted_teacher_vectors_not_model_output","q01":rows[0],"q02":rows[1],
      "T07_score_delta_Q02_minus_Q01":round(rows[1]["irrelevant_T07_score"]-rows[0]["irrelevant_T07_score"],6),
      "caveat":"only two queries on ten teacher-authored passages; no inferential statistics"}
    (BASE/"results/retrieval_details.json").write_text(json.dumps(combined,indent=2)+"\n",encoding="utf-8")
    return combined
if __name__=="__main__":print(json.dumps(analyze(),indent=2))
