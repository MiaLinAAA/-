
Evidence-grounded research briefing: an offline reproducibility study
This repository is the experimental accompaniment to paper.pdf (AT4 final report).
Provenance first
- W07: teacher-provided 6-dimensional handcrafted embedding fixture, not MiniLM/E5/LLM performance.
- W11: deterministic fixed workflow, not an LLM-driven dynamic agent. The source pack is constructed from the W03 student literature worksheet, W07 fixture, and W11 lecture.
- Validator: student-built local implementation; the official W11 student kit and official validator were not available.
- No GPU, API, network, trained model, participant study, or physical intervention.
Reproduce
python --version   # Python >= 3.10
python -m src.reproduce
python -m unittest discover -s tests -v
A successful run regenerates results/retrieval_summary.csv, results/retrieval_details.json, evaluation.csv, results/validator_probes.csv, and runs/ with trajectory.jsonl, tool-results.jsonl, local-validation.json, and final-state.json for both step budgets. Execution uses only standard-library modules.
Empirical findings (fixture, not model benchmark)
1. W07 Q01 river bank: financial passage T07 enters top-3 at 0.690192. W07 Q02 disambiguated query: it remains rank 3 but drops to 0.168371. Precision@3 remains 2/3 under the annotations provided in W07.
2. W11 max_steps=3: search plus 2 reads, 3 actions, no brief, FAIL. max_steps=6: search plus 3 reads plus write, 5 actions, local PASS. Validator is executed after the run and is not counted as an action.
3. Negative controls: deleting the brief, tampering a citation to S99, or removing a tool-result entry should each produce FAIL.
Repository map
- src/agent.py: deterministic action loop and trace writer.
- src/validator.py: locally developed gate checks; does not judge semantic entailment.
- src/analyze.py: W07 retrieval analytics.
- src/probes.py: local validator negative controls.
- src/reproduce.py: one-command reproducer.
- data/w07_fixture/: original supplied compact W07 fixture results and inputs.
- source-pack/: W11 derived source texts and index, with source IDs S01–S03.
- supplementary/: source notes and provenance from the W11 submission.
- results/: machine-readable generated outcomes and paper figures.
- paper.pdf: report (8–10 pages).
Scope and limitations
The experiment demonstrates a dependency chain among retrieval, source reading, citation writing and final-state checks within a controlled teaching fixture. It does not establish LLM agent efficacy, statistical generalization, retrieval model performance, semantic truth of all claims, or official teacher acceptance. The source pack includes secondary student notes; no external transmission is performed.
Attributions
See paper.pdf and supplementary/ for original coursework context and bibliography. Names and grades are intentionally omitted from this public-facing reproduction repository. No GitHub remote was created; upload the repository folder to a GitHub repository if your course requires a URL.
