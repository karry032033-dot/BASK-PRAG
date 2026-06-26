# BASK-PRAG

## 1. Title

**BASK-PRAG: Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation**

This repository is the code and reproducibility package for the manuscript:

**Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation**

The repository corresponds to the associated data and code package for the PeerJ Computer Science AI Application submission.

---

## 2. Description

BASK-PRAG is a resource-aware experimental framework for studying **Parametric Retrieval-Augmented Generation (PRAG)** under explicit construction, routing, and inference-cost accounting.

The project evaluates **Budget-Aware Structured Knowledge Injection (BASK)**, a controlled intervention layer over an adapter-based retrieval-augmented generation pipeline. BASK is designed to make the following components inspectable and reproducible:

* offline construction cost for reusable passage-level adapters;
* online route-preserving adapter invocation;
* text-only, parameter-only, and combined evidence modes;
* routing-boundary diagnostics;
* two-passage complementarity audits;
* answer-level evaluation metrics and bootstrap confidence intervals.

The repository provides compact, auditable materials for reconstructing the reported analyses. It includes code excerpts, metric scripts, bootstrap scripts, configuration templates, prompt templates, table source data, figure source data, and reconstruction notes.

This repository does **not** redistribute third-party benchmark datasets, Wikipedia passage dumps, pretrained model weights, generated LoRA adapter checkpoints, full Elasticsearch indexes, or large experiment logs. Those resources must be obtained from their original providers or regenerated locally according to their own licenses and terms of use.

---

## 3. PeerJ AI Application README Checklist

This README explicitly addresses the PeerJ AI Application reproducibility items.

| PeerJ README item | Where addressed |
| --- | --- |
| Title | Section 1 |
| Description | Section 2 |
| Dataset information | Sections 5 and 6 |
| Code information | Sections 4 and 7 |
| Usage instructions | Sections 9, 10, and 11 |
| Requirements | Section 8 |
| Methodology | Section 12 |
| Citations | Section 15 |
| License and contribution guidelines | Sections 16 and 17 |

---

## 4. Repository Contents

```text
.
├── DATASET_LINKS.md                  # External dataset, model, DPR, Elasticsearch, and baseline links
├── tables/                           # CSV source data for manuscript tables
├── figures/                          # CSV source data for numeric figure values
├── scripts/                          # QA metric and bootstrap confidence-interval scripts
├── configs/                          # Configuration templates for controlled runs
├── prompts/                          # Prompt templates used by the protocol
├── code_core/
│   ├── bask_core_minimal.py           # Dependency-light reference implementation of core BASK logic
│   └── original_framework_core/       # Selected core implementation files from the full framework
├── predictions/                       # Optional location for released or regenerated per-query predictions
├── retrieval_logs/                    # Optional location for released or regenerated retrieval traces
├── adapter_logs/                      # Optional location for released or regenerated adapter-selection logs
├── requirements.txt                   # Minimal Python dependencies for smoke tests and metric scripts
├── CITATION.cff                       # Citation metadata template
├── zenodo_metadata_template.json      # Optional archival metadata template
├── LICENSE                            # Repository license
└── README.md                          # Repository overview and reconstruction instructions
```

---

## 5. Dataset Information

The study uses four public third-party question-answering benchmark datasets. These datasets are not redistributed in this repository.

| Dataset | Role in the manuscript | Original source / download link | Expected local path |
| --- | --- | --- | --- |
| HotpotQA | Main multi-hop QA benchmark; includes HotpotQA Real-300 and diagnostic subsets | `https://hotpotqa.github.io/` and `http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json` | `data/hotpotqa/hotpot_dev_distractor_v1.json` |
| 2WikiMultihopQA | Same-source controlled multi-hop comparison | `https://github.com/Alab-NII/2wikimultihop` and `https://www.dropbox.com/s/ms2m13252h6xubs/data_ids_april7.zip?e=1` | `data/2wikimultihopqa/` |
| PopQA | Long-tail factual QA comparison | `https://github.com/AlexTMallen/adaptive-retrieval` | `data/popqa/popQA.tsv` |
| ComplexWebQuestions | Compositional QA comparison | `https://github.com/yuancu/complex-web-questions-dataset` and `https://www.dropbox.com/scl/fo/nqujvpg2gc4y0ozkw3wgr/AOzjVEsdUhv2Fx2pamfJlSw?rlkey=746t7xehfqxf1zr867nxiq8aq&e=1` | `data/complexwebquestions/ComplexWebQuestions_dev.json` |

The manuscript reports controlled subset identifiers, retrieval or passage identifiers, model outputs, aggregate table values, and figure values. Source benchmark files should be obtained from their original providers according to the corresponding licenses and terms of use.

### Optional download commands

```bash
# HotpotQA
mkdir -p data/hotpotqa
wget -P data/hotpotqa/ http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json

# PopQA
mkdir -p data/popqa
wget -O data/popqa/popQA.tsv https://raw.githubusercontent.com/AlexTMallen/adaptive-retrieval/main/data/popQA.tsv
```

For 2WikiMultihopQA and ComplexWebQuestions, download the files manually from the links above, unzip them if needed, and place the required files under the expected local paths.

Additional dataset and reconstruction links are provided in `DATASET_LINKS.md`.

---

## 6. Retrieval Corpus and Index Information

The experiments use **BM25 retrieval** over Wikipedia passages following the DPR Wikipedia split. The DPR passage corpus should be downloaded from its original public source and indexed locally with Elasticsearch.

```bash
mkdir -p data/dpr
wget -O data/dpr/psgs_w100.tsv.gz https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz

pushd data/dpr
gzip -d psgs_w100.tsv.gz
popd
```

After downloading the passage file, build a local Elasticsearch index using the local configuration files in `configs/`.

The full Wikipedia passage dump and Elasticsearch index are not included in this repository because of size and redistribution constraints.

---

## 7. Code Information

The repository contains code for inspecting the BASK workflow and recomputing reported evaluation metrics.

| Path | Purpose |
| --- | --- |
| `code_core/bask_core_minimal.py` | Dependency-light reference implementation of the main BASK logic. It illustrates coverage-aware grouping, sparse route-preserving invocation, rerouting probes, residual two-passage synergy, QA metrics, and bootstrap confidence intervals. |
| `code_core/original_framework_core/` | Selected core implementation files from the full experimental framework. These files document how the manuscript-level experiments were structured. |
| `scripts/compute_qa_metrics.py` | Computes normalized word-level F1, exact match, precision, and recall for compatible prediction files. |
| `scripts/bootstrap_ci.py` | Computes bootstrap confidence intervals over query-level prediction records. |
| `scripts/compute_qa_metrics.py --help` | Shows the required input format for metric recomputation. |
| `scripts/bootstrap_ci.py --help` | Shows the required input format for bootstrap confidence intervals. |
| `configs/` | Configuration templates for controlled reconstruction runs, including benchmark/model/retrieval settings. |
| `prompts/` | Prompt templates used in the controlled protocol. |
| `tables/` | CSV source data for manuscript tables. |
| `figures/` | CSV source data for numeric figure values. |
| `predictions/` | Optional directory for released or regenerated per-query prediction records. |
| `retrieval_logs/` | Optional directory for released or regenerated retrieval traces. |
| `adapter_logs/` | Optional directory for released or regenerated adapter-selection logs. |

The included code is intended to support transparent reconstruction and auditing. Full model-based experiments additionally require external datasets, a local retrieval index, pretrained base models, adapter-generation or adapter-training resources, and GPU hardware.

---

## 8. Requirements

### 8.1 Minimal requirements for repository checks

A minimal Python environment is sufficient for the smoke test, metric script, and bootstrap script.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The minimal environment supports:

* checking the repository structure;
* running `code_core/bask_core_minimal.py`;
* inspecting metric-script command-line interfaces;
* recomputing metrics from compatible prediction or aggregate records.

### 8.2 Full experiment requirements

Full model-based reconstruction requires a larger environment. The manuscript reports the following main implementation environment for the controlled experiments:

| Component | Reported setting |
| --- | --- |
| Operating system | Ubuntu 20.04 |
| Python | Python 3.8 |
| Deep-learning framework | PyTorch 2.0.0 |
| CUDA | CUDA 11.8 |
| Model libraries | Hugging Face `transformers`, `peft` |
| Retrieval system | Elasticsearch with BM25 |
| Main GPU setting | One 32 GB GPU |
| Same-protocol DyPRAG reference | Two 48 GB GPUs |

Because CUDA, PyTorch, and model dependencies are hardware-specific, install the full deep-learning stack according to your local GPU driver, CUDA version, and model family.

---

## 9. Minimal Smoke Test

Run the following commands from the repository root:

```bash
python code_core/bask_core_minimal.py
python scripts/compute_qa_metrics.py --help
python scripts/bootstrap_ci.py --help
```

These commands verify that the core reference code and evaluation scripts are accessible. They do not require raw benchmark datasets, pretrained models, LoRA adapters, retrieval indexes, or large experiment logs.

---

## 10. Usage Instructions: Loading Data and Code

### Step 1: Clone the repository

```bash
git clone https://github.com/karry032033-dot/BASK-PRAG.git
cd BASK-PRAG
```

### Step 2: Create the minimal Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Download external benchmark data

Download the required public benchmark datasets listed in Section 5 and place them under the expected local paths.

### Step 4: Download and index the retrieval corpus

Download the DPR Wikipedia passage corpus listed in Section 6 and build a local Elasticsearch BM25 index.

### Step 5: Review experiment configuration templates

Review the files in:

```text
configs/
prompts/
```

Use these files to align dataset paths, retrieval settings, prompt templates, decoding settings, and evaluation settings.

### Step 6: Run the lightweight BASK reference implementation

```bash
python code_core/bask_core_minimal.py
```

### Step 7: Recompute QA metrics or confidence intervals

```bash
python scripts/compute_qa_metrics.py --help
python scripts/bootstrap_ci.py --help
```

Use compatible prediction files or released aggregate records as inputs.

### Step 8: Reconstruct full model-based runs

Full reconstruction requires the external resources listed in Section 11. After obtaining those resources, use the configuration templates and prompt templates to reproduce the controlled evaluation protocol.

---

## 11. Reproducing Reported Analyses

The repository supports several levels of reconstruction.

### 11.1 Inspect core BASK logic

```bash
python code_core/bask_core_minimal.py
```

This reference script illustrates:

* coverage-aware grouped construction;
* sparse route-preserving invocation;
* lexical rerouting probes;
* residual two-passage synergy auditing;
* normalized QA metric computation;
* bootstrap confidence-interval computation.

### 11.2 Recompute QA metrics

```bash
python scripts/compute_qa_metrics.py --help
```

Use this script on compatible prediction files or released aggregate records.

### 11.3 Recompute bootstrap confidence intervals

```bash
python scripts/bootstrap_ci.py --help
```

Use this script on query-level records when available.

### 11.4 Reconstruct full model-based experiments

Full model-based reconstruction requires resources that are not redistributed here:

* third-party benchmark datasets;
* DPR Wikipedia passages;
* a local Elasticsearch BM25 index;
* pretrained base models;
* tokenizer files for the selected base models;
* adapter-generation or adapter-training environment;
* generated LoRA adapter checkpoints or regenerated adapters;
* local GPU environment;
* compatible per-query prediction and retrieval-record formats.

After obtaining these resources, review the configuration templates in `configs/` and prompt templates in `prompts/`.

---

## 12. Methodology

The repository implements and documents the high-level methodology reported in the manuscript.

### 12.1 Fixed evaluation protocol

All controlled comparisons keep the following components fixed unless otherwise stated:

* base model;
* retriever;
* online retrieval depth;
* adapter mechanism;
* prompt family;
* decoding configuration;
* answer normalization;
* evaluation scripts.

The compared components are the evidence mode, adapter-construction policy, and adapter-routing policy.

### 12.2 Construct: coverage-aware grouped adapter construction

BASK changes the adapter-construction unit from repeated query-passage events to reusable passage-level units. It builds a passage-query coverage map over deeper retrieval candidates, selects high-reuse passages under an explicit construction budget, and generates reusable passage-level adapter materials.

In the HotpotQA Real-300 setting reported in the manuscript, the grouped construction procedure reduced measured offline supervision-generation calls from 900 query-passage events to 271 passage-level calls, corresponding to approximately 30% of the classical construction cost.

### 12.3 Invoke: route-preserving sparse adapter invocation

During inference, BASK reuses adapters only when their source passages remain aligned with the query's local top-k retrieval route. Sparse replacement avoids invoking adapters from deeper construction candidates unless their source passages also appear in the online retrieval list.

The main invocation variants include:

* `PRAG-PerQuery`: event-level construction baseline;
* `BASK-MergeFlat`: flat reuse boundary condition;
* `BASK-SparseFirst`: route-preserving first-slot replacement;
* `BASK-SparseAdaptive`: route-preserving sparse replacement based on construction-side support.

### 12.4 Diagnose: routing-boundary and two-passage complementarity audit

BASK uses diagnostic probes to identify routing boundaries rather than to create an oracle selector.

The diagnostic procedures include:

* lexical evidence-priority rerouting;
* margin-gated rerouting;
* posterior two-passage complementarity auditing;
* cross-task evidence-mode comparison.

The posterior two-passage audit is used only after inference. It is not fed back into the online route-selection policy.

### 12.5 Evidence modes and metrics

The main evidence modes are:

* **ICL**: textual evidence only;
* **PRAG**: parametric evidence through selected adapters;
* **Combine**: textual evidence plus selected parametric adapters;
* **DyPRAG reference**: same-protocol dynamic-parameter reference for cost-latency comparison.

The main evaluation metric is normalized word-level F1. Exact match, precision, recall, and bootstrap confidence intervals are reported where per-sample records are available.

---

## 13. What Is Included

This repository includes:

* source-data tables for reported manuscript tables;
* source-data CSV files for numeric figure values;
* metric scripts;
* bootstrap confidence-interval scripts;
* compact core-code excerpts;
* configuration templates;
* prompt templates;
* dataset and reconstruction links;
* citation metadata template;
* optional archival metadata template;
* reconstruction notes.

---

## 14. What Is Not Included

To keep the repository lightweight and compliant with third-party licenses and model-use restrictions, this repository does not include:

* raw benchmark datasets;
* Wikipedia passage dumps;
* generated question-answer or rewriting outputs derived from benchmark passages;
* pretrained model weights;
* generated LoRA adapter checkpoints;
* full Elasticsearch indexes;
* full archived experiment run directories;
* large per-query prediction files unless explicitly released separately;
* large retrieval traces unless explicitly released separately;
* large adapter-selection logs unless explicitly released separately.

Use `DATASET_LINKS.md` and the instructions in this README to obtain external resources from their original providers.

---

## 15. Citations

If you use this repository, please cite the accompanying manuscript and the original datasets or baseline methods used in your work.

### 15.1 Repository citation

A `CITATION.cff` template is included and can be updated with the final publication metadata.

```bibtex
@misc{bask_prag,
  title  = {Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation},
  author = {Yang, Chengyong and Yuan, Kairui and Li, Qiuyan and Liu, Xin},
  year   = {2026},
  note   = {Repository and reproducibility package},
  url    = {https://github.com/karry032033-dot/BASK-PRAG}
}
```

### 15.2 External resources to cite as applicable

Please cite the original sources for:

* HotpotQA;
* 2WikiMultihopQA;
* PopQA;
* ComplexWebQuestions;
* DPR Wikipedia passage corpus;
* PRAG baseline repository;
* pretrained base models used in reconstruction;
* any additional adapter, retrieval, or serving baselines used in follow-up experiments.

Public PRAG baseline repository:

```text
https://github.com/oneal2000/PRAG
```

---

## 16. License

The code and documentation in this repository are governed by the license file included in this repository:

```text
LICENSE
```

Third-party datasets, pretrained models, Wikipedia passages, and external baseline repositories are governed by their own licenses and terms of use. Users are responsible for complying with all external licenses and provider terms.

---

## 17. Contribution Guidelines

Contributions are welcome through GitHub issues and pull requests.

Before contributing, please follow these guidelines:

1. Open an issue to describe the proposed bug fix, documentation change, or reproducibility improvement.
2. Keep changes focused and clearly documented.
3. Do not commit raw benchmark datasets, Wikipedia passage dumps, pretrained model weights, generated LoRA adapter checkpoints, full Elasticsearch indexes, or other restricted large artifacts.
4. Use small synthetic examples or aggregate records for tests when possible.
5. Make sure new scripts include command-line help or clear usage comments.
6. Update this README when adding new reconstruction steps, configuration files, or external-resource requirements.
7. Respect the licenses and terms of use of all third-party datasets, models, and baseline repositories.

---

## 18. Data and Code Availability Statement

The code and reproducibility package are available at:

```text
https://github.com/karry032033-dot/BASK-PRAG
```

The repository contains source-data tables, figure-data files, metric scripts, bootstrap scripts, configuration templates, prompt templates, compact core-code excerpts, citation metadata, and reconstruction notes.

Third-party benchmark datasets and Wikipedia retrieval resources are not redistributed. They should be obtained from their original sources as listed in this README and in `DATASET_LINKS.md`.

---

## 19. Contact

For questions about the repository or reconstruction package, please open a GitHub issue or contact the repository maintainers listed in the accompanying manuscript.
