
# Evidence-Grounded Research Briefing with Verifiable Offline Workflows

**AT4 Final Project | DDS001 — Advanced Research in Data Science**

This repository contains the research paper, source code, experimental datasets, evaluation results, and reproducibility materials for the AT4 final project.

The project investigates how retrieval quality, tool-use budgets, and final-state validation affect the reliability of evidence-grounded research brief generation.

## 1. Project Overview

Reliable AI-assisted research requires more than generating fluent text. A research workflow must retrieve relevant information, verify its sources, produce properly cited conclusions, and confirm that the requested output has actually been created.

This project integrates three components:

- **W03 — Literature Review:** Responsible AI, factuality, transparency, reliability, and trustworthy foundation models.
- **W07 — Technical Reproduction:** Text retrieval and semantic similarity analysis using a teacher-provided embedding fixture.
- **W11 — Agent Workflow:** Offline source retrieval, evidence collection, research brief generation, and final-state validation.

The study focuses on two research questions:

**RQ1:** How does query ambiguity affect retrieval relevance and evidence quality?

**RQ2:** How do different tool-use budgets affect workflow completion and final-state validation?

## 2. Research Methodology

### 2.1 Retrieval Reliability

The W07 experiment uses a teacher-provided dataset containing handcrafted six-dimensional text embeddings.

Two queries are examined:

- Q01: An ambiguous query involving the term "river bank".
- Q02: A more specific query intended to clarify the information need.

The experiment compares retrieval rankings, cosine similarity scores, and Precision@3.

### 2.2 Offline Research Agent Workflow

The W11 experiment implements a deterministic, tool-based workflow consisting of the following steps:

1. Search the offline source collection.
2. Identify relevant source IDs.
3. Read the selected source documents.
4. Extract evidence and prepare citations.
5. Generate a research brief.
6. Validate the final output against the task requirements.

The workflow uses three offline sources and records tool calls, tool responses, execution states, and validation results.

### 2.3 Controlled Comparison

Two tool-use budgets are compared:

- **Condition A:** `max_steps = 3`
- **Condition B:** `max_steps = 6`

The task, source collection, tool definitions, and local validator remain unchanged.

Only the maximum number of permitted actions is modified.

## 3. Experimental Results

### 3.1 Retrieval Experiment

| Metric | Q01 | Q02 |
|---|---:|---:|
| Precision@3 | 0.6667 | 0.6667 |
| Irrelevant passage T07 rank | 3 | 3 |
| T07 similarity score | 0.690192 | 0.168371 |

The results show that query clarification substantially reduces the similarity score of an irrelevant financial passage.

However, the passage remains among the top three retrieved results, and Precision@3 does not improve.

This demonstrates that improved similarity separation does not necessarily produce better ranking-based retrieval metrics.

### 3.2 Workflow Completion Experiment

| Metric | max_steps=3 | max_steps=6 |
|---|---:|---:|
| Tool actions | 3 | 5 |
| Sources read | 2 | 3 |
| Research brief generated | No | Yes |
| Local validator | FAIL | PASS |

With three permitted actions, the workflow stops before collecting sufficient evidence and generating the final brief.

With six permitted actions, the workflow completes after five actions and passes the local final-state validator.

The validator executes after the workflow and is not counted as a tool action.

### 3.3 Validator Robustness Tests

Three negative-control experiments were conducted:

1. **Missing brief:** Remove the generated research brief.
2. **Invalid citation:** Replace a valid citation with an unknown source ID.
3. **Missing tool result:** Remove a required tool observation.

All three modified cases were rejected by the local validator.

These tests demonstrate that the implemented validator can detect selected structural and execution-record failures.

They do not establish that every statement in the generated brief is semantically correct.

## 4. Repository Structure

```text
repository/
├── README.md
├── requirements.txt
├── paper.pdf
├── paper.docx
├── run_all.py
├── src/
│   ├── agent.py
│   ├── analyze.py
│   ├── reproduce.py
│   ├── validator.py
│   └── probes.py
├── data/
│   ├── w07_fixture/
│   └── w11_source_pack/
├── source-pack/
├── results/
│   ├── retrieval_summary.csv
│   ├── retrieval_details.json
│   ├── validator_probes.csv
│   └── experiment figures
├── runs/
│   ├── max_steps_3/
│   └── max_steps_6/
├── supplementary/
├── tests/
├── evaluation.csv
└── provenance.json
```

## 5. Environment Requirements

- Python 3.10 or later
- Windows, macOS, or Linux
- No GPU required
- No external API key required
- No network connection required
- No third-party Python packages required

The core implementation uses the Python standard library.

## 6. Reproducing the Experiments

### Step 1: Download the Repository

Download the repository and extract its contents, or clone the repository using Git.

Open a terminal in the project root directory containing `run_all.py`.

### Step 2: Check Python

```bash
python --version
```

Python 3.10 or later is recommended.

### Step 3: Run All Experiments

```bash
python -m src.reproduce
```

This command reproduces the retrieval analysis, tool-budget comparison, and validator negative-control experiments.

### Step 4: Run Automated Tests

```bash
python -m unittest discover -s tests -v
```

The tests check the workflow implementation and validation behavior.

### Step 5: Inspect Results

The generated outputs include:

- `results/retrieval_summary.csv`
- `results/retrieval_details.json`
- `results/validator_probes.csv`
- `evaluation.csv`
- `runs/max_steps_3/`
- `runs/max_steps_6/`

Each workflow directory contains execution trajectories, tool observations, final-state information, and local validation results.

## 7. Research Paper

The complete AT4 research paper is available in the repository:

- [Read the final paper (PDF)](paper.pdf)
- [Editable manuscript (Word)](paper.docx)

**Paper Title:** Evidence-Grounded Research Briefing with Verifiable Offline Workflows

The paper includes:

- Abstract
- Introduction
- Related Work
- Methodology
- Experimental Design
- Results and Discussion
- Conclusion
- References

## 8. Limitations

The following limitations are explicitly acknowledged:

1. The W07 embeddings are handcrafted teaching fixtures, not outputs from a pretrained embedding model.
2. The W11 system is a deterministic fixed workflow rather than a dynamically reasoning LLM agent.
3. The W11 source collection was constructed from available course materials rather than the official student-kit source collection.
4. The final-state validator was implemented locally. The official course validator was not available or executed.
5. Structural validation does not guarantee that all generated claims are factually supported.
6. The findings are limited to the supplied teaching fixtures and cannot be generalized to real-world LLM agent performance.

No trained language model, external API, or online service was used in the core experiments.

## 9. Reproducibility and Academic Integrity

The repository includes execution traces, experimental configurations, source materials, evaluation files, and provenance information.

All reported numerical results are derived from the documented offline experiments.

Teacher-provided fixtures are clearly distinguished from model-generated outputs.

The project does not claim that the experiments evaluate the performance of a deployed large language model or establish generalizable model benchmarks.

## 10. Conclusion

This project demonstrates the importance of combining retrieval evaluation, evidence tracking, controlled tool execution, and final-state validation.

The experiments illustrate that:

- Ambiguous retrieval queries can introduce irrelevant evidence.
- Query clarification may improve similarity separation without changing top-ranked retrieval precision.
- Insufficient tool-use budgets can prevent task completion.
- Final-state validation can detect selected workflow and citation errors.

Overall, the study provides a reproducible offline framework for examining the reliability of evidence-grounded research workflows.

---

**Course:** DDS001 — Advanced Research in Data Science

**Assignment:** AT4 Final Integrated Report
