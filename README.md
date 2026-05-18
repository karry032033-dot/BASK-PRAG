# Supplemental Data S1: BASK source data, core code, and reconstruction notes

This package is prepared for the PeerJ Computer Science submission:

**Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation**

It is designed as a compact supplemental package for review. It provides the machine-readable source data needed to inspect the manuscript tables and figures, plus only the core code needed to audit the BASK mechanisms. It does not redistribute original benchmark datasets, pretrained models, generated adapters, or large experiment logs.

## PeerJ upload description

Use the following description in the PeerJ `Describe the data or code files you are uploading as supplementary files` field:

> The supplemental package contains aggregate source data for the reported tables and figures, metric scripts, bootstrap scripts, configuration templates, prompt templates, reconstruction notes, and a core-code excerpt for the BASK experiments. The original third-party benchmark datasets are not redistributed; source benchmark files should be obtained from their original providers according to their licenses.

## Contents

- `DATASET_LINKS.md`: official or provider-facing download links for HotpotQA, 2WikiMultihopQA, PopQA, ComplexWebQuestions, DPR Wikipedia passages, Elasticsearch, base models, and the public PRAG baseline repository.
- `tables/`: CSV source data for the manuscript tables.
- `figures/`: CSV source data for the manuscript figures where numeric values are reported.
- `scripts/`: reusable QA metric and bootstrap confidence-interval scripts.
- `code_core/bask_core_minimal.py`: dependency-light reference implementation of the core BASK logic: coverage-aware passage selection, route-preserving sparse replacement, rerouting probes, residual synergy, QA metrics, and bootstrap CIs.
- `code_core/original_framework_core/`: selected core files from the implementation package, including grouped generation, sparse route-aware invocation, structured generation helpers, and pair-cache audit tooling. The vendored BEIR copy, `__pycache__` files, raw datasets, model weights, adapters, and large logs are intentionally omitted.
- `configs/`, `prompts/`: placeholders and selected templates for the protocol used by the authors.
- `predictions/`, `retrieval_logs/`, `adapter_logs/`: expected locations for per-query prediction, retrieval, and adapter-selection logs if the authors choose to release those larger records in a repository.
- `CITATION.cff` and `zenodo_metadata_template.json`: metadata templates for optional archival release.

## What is not included

To respect third-party data licenses and keep the PeerJ upload small, this package does not include:

- raw benchmark datasets;
- Wikipedia passage dumps;
- generated question-answer or rewriting outputs derived from restricted passages;
- pretrained model weights;
- LoRA adapter checkpoints;
- full retrieval indexes;
- full archived run directories.

Download external resources using `DATASET_LINKS.md` and reconstruct experiments using the provided identifiers, configuration notes, aggregate records, and scripts.

## Minimal smoke test

From the package root:

```bash
python code_core/bask_core_minimal.py
python scripts/compute_qa_metrics.py --help
python scripts/bootstrap_ci.py --help
```

The smoke test does not require external datasets or model weights.

## Main manuscript consistency note

The manuscript reports that Supplemental Data S1 includes aggregate source data, metric scripts, bootstrap scripts, configuration templates, prompt templates, and reconstruction notes. This package follows that scope and adds a compact core-code excerpt while keeping dataset access external via official links.
