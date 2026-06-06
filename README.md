# BASK-PRAG

**Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation**

This repository provides the code, source-data tables, configuration templates, metric scripts, prompt templates, and reconstruction notes for the manuscript:

**“Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation”**

BASK-PRAG is a resource-aware experimental framework for studying **Parametric Retrieval-Augmented Generation (PRAG)** under explicit construction, routing, and inference-cost accounting. The project focuses on reusable passage-level adapter construction, route-preserving sparse adapter invocation, and posterior diagnostics for routing behavior and evidence complementarity.

This repository is intended as the reproducibility package for the reported **AI Application** study. It provides compact, auditable materials for reconstructing the reported experiments and checking the main resource-accounting claims. It does **not** redistribute third-party benchmark datasets, Wikipedia passage dumps, pretrained model weights, generated adapters, full Elasticsearch retrieval indexes, or large experiment logs. Third-party data and retrieval resources must be obtained from their original public sources according to their own licenses and terms of use.

---

## AI Application Reproducibility Summary

This repository supports the AI Application reporting requirements by documenting:

* the algorithms and code used to implement the BASK workflow;
* the third-party benchmark datasets used in the evaluation;
* the external retrieval corpus used for BM25 retrieval;
* the local environment and dependency setup;
* the evaluation protocol, answer-normalization scripts, and bootstrap confidence-interval scripts;
* the source-data tables and figure-data files used to audit reported results;
* the repository limitations, including materials that are not redistributed for licensing, size, or reproducibility-scope reasons.

The repository is organized for **transparent reconstruction** rather than one-click redistribution of all external resources.

---

## Highlights

* **Coverage-aware grouped construction**: reduces repeated supervision-generation calls by constructing reusable passage-level knowledge units.
* **Route-preserving sparse invocation**: reuses adapters while keeping selected parameters aligned with the retrieved evidence order.
* **Routing-boundary diagnostics**: evaluates rerouting behavior and two-passage complementarity without using oracle choices in the online route.
* **Evaluation-protocol transparency**: reports fixed retrieval depth, evidence modes, answer normalization, QA metrics, and bootstrap confidence intervals.
* **Reproducibility-first package**: includes aggregate source data, metric scripts, configuration templates, prompt templates, and reconstruction notes.
* **External-data compliance**: benchmark datasets and Wikipedia passages are obtained from their official or provider-facing sources rather than redistributed.

---

## Repository Contents

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
│   └── original_framework_core/       # Selected core implementation files
├── predictions/                       # Optional location for released per-query predictions
├── retrieval_logs/                    # Optional location for retrieval traces
├── adapter_logs/                      # Optional location for adapter-selection logs
├── requirements.txt                   # Minimal Python dependencies for smoke tests and metric scripts
├── CITATION.cff                       # Citation metadata template
├── zenodo_metadata_template.json      # Optional archival metadata template
└── README.md                          # Repository overview and reconstruction instructions
```

---

## Third-Party Benchmark Datasets

BASK-PRAG follows a PRAG-style evaluation setting and uses four public question-answering benchmark datasets. Please download the original benchmark files from their official or provider-facing sources and follow the corresponding licenses and terms of use.

This repository does not redistribute the raw benchmark datasets.

| Dataset             | Original Source / Download Link                                                                                  | Expected Local Path                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 2WikiMultihopQA     | https://www.dropbox.com/s/ms2m13252h6xubs/data_ids_april7.zip?e=1                                                | `data/2wikimultihopqa/`                                 |
| HotpotQA            | http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json                                           | `data/hotpotqa/hotpot_dev_distractor_v1.json`           |
| PopQA               | https://github.com/AlexTMallen/adaptive-retrieval/blob/main/data/popQA.tsv                                       | `data/popqa/popQA.tsv`                                  |
| ComplexWebQuestions | https://www.dropbox.com/scl/fo/nqujvpg2gc4y0ozkw3wgr/AOzjVEsdUhv2Fx2pamfJlSw?rlkey=746t7xehfqxf1zr867nxiq8aq&e=1 | `data/complexwebquestions/ComplexWebQuestions_dev.json` |

Additional dataset and reconstruction links are provided in `DATASET_LINKS.md`.

### Optional Download Commands

```bash
# HotpotQA
mkdir -p data/hotpotqa
wget -P data/hotpotqa/ http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json

# PopQA
mkdir -p data/popqa
wget -O data/popqa/popQA.tsv https://raw.githubusercontent.com/AlexTMallen/adaptive-retrieval/main/data/popQA.tsv
```

For 2WikiMultihopQA and ComplexWebQuestions, download the files manually from the links above, unzip them if needed, and place the required files under the expected local paths.

---

## External Retrieval Corpus

The experiments use BM25 retrieval over Wikipedia passages following the DPR Wikipedia split. Download the DPR passage corpus from its original public source and build an Elasticsearch index locally.

```bash
mkdir -p data/dpr
wget -O data/dpr/psgs_w100.tsv.gz https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz

pushd data/dpr
gzip -d psgs_w100.tsv.gz
popd
```

Then index the passages with Elasticsearch according to your local setup and the configuration files provided in this repository.

The full Wikipedia passage dump and Elasticsearch index are not included in this repository because of size and redistribution constraints.

---

## Environment

A minimal Python environment is sufficient for the included smoke tests, metric scripts, and bootstrap scripts.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For full model-based experiments, install the required deep-learning stack separately according to your hardware, CUDA version, model family, and adapter-training setup. The manuscript reports the main software and hardware environment used for the controlled experiments.

---

## Minimal Smoke Test

Run the following commands from the repository root:

```bash
python code_core/bask_core_minimal.py
python scripts/compute_qa_metrics.py --help
python scripts/bootstrap_ci.py --help
```

These tests are intended to verify the repository structure and core scripts. They do not require external datasets, pretrained models, LoRA adapters, retrieval indexes, or large experiment logs.

---

## Evaluation Protocol

The controlled evaluation follows the same high-level protocol reported in the manuscript.

1. **Retrieval setup**
   BM25 retrieval is performed over a locally built Elasticsearch Wikipedia index. Online inference uses the top-three retrieved passages. Deeper retrieval candidates are used only for grouped construction when required by the corresponding experiment.

2. **Evidence modes**
   The main evidence modes are:

   * **ICL**: textual evidence only;
   * **PRAG**: parametric evidence through selected adapters;
   * **Combine**: textual evidence plus selected parametric adapters;
   * **DyPRAG reference**: same-protocol dynamic-parameter reference used for cost-latency comparison.

3. **BASK construction and invocation variants**
   The repository documents and provides compact code for:

   * coverage-aware grouped adapter construction;
   * route-preserving sparse adapter invocation;
   * flat reuse as a boundary condition;
   * lexical rerouting probes;
   * posterior two-passage complementarity auditing.

4. **Metrics**
   The primary reported metric is normalized word-level F1. Exact match, precision, recall, and bootstrap confidence intervals are computed where per-sample records are available.

5. **Reproducibility materials**
   The repository includes aggregate table data, figure source data, metric scripts, bootstrap scripts, configuration templates, prompts, and reconstruction notes. Large run artifacts are not redistributed by default.

---

## Reproducing Reported Analyses

The repository supports several levels of reconstruction.

### 1. Inspect Core BASK Logic

```bash
python code_core/bask_core_minimal.py
```

This dependency-light reference script illustrates the core logic for:

* coverage-aware grouping;
* sparse route-preserving invocation;
* rerouting probes;
* residual two-passage synergy;
* QA metric computation;
* bootstrap confidence intervals.

### 2. Recompute QA Metrics

Use the metric script on compatible prediction files or released aggregate records:

```bash
python scripts/compute_qa_metrics.py --help
```

### 3. Recompute Bootstrap Confidence Intervals

```bash
python scripts/bootstrap_ci.py --help
```

### 4. Reconstruct Full Model-Based Runs

Full model-based reconstruction requires external resources that are not redistributed here:

* third-party benchmark datasets;
* DPR Wikipedia passages;
* local Elasticsearch index;
* pretrained base models;
* adapter-training environment;
* generated adapter checkpoints or regenerated adapters;
* local GPU environment.

After obtaining those resources, review the configuration templates in `configs/` and the prompt templates in `prompts/`.

---

## What Is Not Included

To keep the repository lightweight and compliant with third-party data and model licenses, this repository does not include:

* raw benchmark datasets;
* Wikipedia passage dumps;
* generated question-answer or rewriting outputs derived from benchmark passages;
* pretrained model weights;
* LoRA adapter checkpoints;
* full Elasticsearch indexes;
* full archived experiment run directories;
* large per-query prediction files unless explicitly released separately;
* large retrieval traces unless explicitly released separately;
* large adapter-selection logs unless explicitly released separately.

Use `DATASET_LINKS.md` and the instructions above to obtain external resources from their original providers.

---

## Data and Code Availability

The code and reproducibility package are available in this GitHub repository:

```text
https://github.com/karry032033-dot/BASK-PRAG
```

The repository contains source-data tables, figure-data files, metric scripts, bootstrap scripts, configuration templates, prompt templates, compact core-code excerpts, and reconstruction notes.

Third-party benchmark datasets and Wikipedia retrieval resources are not redistributed. They should be obtained from their original sources as listed in this README and in `DATASET_LINKS.md`.

---

## Reproducibility Notes

The recommended workflow is:

1. Download the required public datasets and DPR Wikipedia passages from their original sources.
2. Build the BM25 retrieval index locally with Elasticsearch.
3. Review the configuration templates in `configs/`.
4. Run the metric and bootstrap scripts on the provided aggregate source data.
5. Use `code_core/bask_core_minimal.py` to inspect the core logic for coverage-aware grouping, sparse route-preserving invocation, rerouting probes, residual synergy, QA metrics, and bootstrap confidence intervals.
6. Reconstruct full model-based runs only after obtaining the required external datasets, pretrained models, retrieval resources, and local GPU environment.
7. Add large run artifacts such as predictions, retrieval traces, and adapter logs only if you choose to release them separately.

---

## Relationship to PRAG

BASK-PRAG builds on the Parametric RAG research direction and follows the same broad benchmark setting. The main focus of this repository is not to redistribute the original PRAG implementation or datasets, but to provide a compact, auditable package for BASK-specific resource accounting, route preservation, and diagnostic analysis.

Public PRAG baseline repository:

```text
https://github.com/oneal2000/PRAG
```

---

## License

Please see the repository license file for terms governing the code and documentation in this repository.

Third-party datasets, pretrained models, Wikipedia passages, and external baseline repositories are governed by their own licenses and terms of use. Users are responsible for complying with those external terms.

If a license file has not yet been added to this repository, please add one before final archival or publication. A standard open-source license such as MIT or Apache-2.0 may be appropriate, subject to agreement by all authors and any institutional requirements.

---

## Citation

If you use this repository, please cite the accompanying paper and the original benchmark datasets. A `CITATION.cff` template is included and can be updated with the final publication metadata.

```bibtex
@misc{bask_prag,
  title  = {Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation},
  author = {Yang, Chengyong and Yuan, Kairui and Li, Qiuyan and Liu, Xin},
  year   = {2026},
  note   = {Repository and reproducibility package},
  url    = {https://github.com/karry032033-dot/BASK-PRAG}
}
```

---

## Contact

For questions about the repository or reconstruction package, please open a GitHub issue or contact the repository maintainers.
