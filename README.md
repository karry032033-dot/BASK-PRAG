# BASK-PRAG

**Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation**

BASK-PRAG is a resource-aware experimental framework for studying **Parametric Retrieval-Augmented Generation (PRAG)** under explicit construction, routing, and inference-cost accounting. The project focuses on reusable passage-level adapter construction, route-preserving sparse adapter invocation, and posterior diagnostics for routing and evidence complementarity.

This repository provides source data, configuration templates, metric scripts, reconstruction notes, and compact core-code excerpts for reproducing and auditing the reported BASK experiments. It does **not** redistribute third-party benchmark datasets, pretrained model weights, generated adapters, full retrieval indexes, or large experiment logs.

---

## Highlights

- **Coverage-aware grouped construction**: reduces repeated supervision-generation calls by constructing reusable passage-level knowledge units.
- **Route-preserving sparse invocation**: reuses adapters while keeping selected parameters aligned with the retrieved evidence order.
- **Routing-boundary diagnostics**: evaluates rerouting behavior and two-passage complementarity without using oracle choices in the online route.
- **Reproducibility-first package**: includes aggregate source data, scripts, configuration templates, prompts, and reconstruction notes.
- **External-data compliant**: benchmark datasets and Wikipedia passages are obtained from their official providers rather than redistributed.

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
├── CITATION.cff                       # Citation metadata template
└── zenodo_metadata_template.json      # Optional archival metadata template
```

---

## Benchmark Dataset Download Links

BASK-PRAG follows the PRAG-style evaluation setting and uses four public question-answering benchmark datasets. Please download the original benchmark files from their official or provider-facing sources and follow the corresponding licenses and terms of use.

| Dataset | Download / Source Link | Expected Local Path |
|---|---|---|
| 2WikiMultihopQA | https://www.dropbox.com/s/ms2m13252h6xubs/data_ids_april7.zip?e=1 | `data/2wikimultihopqa/` |
| HotpotQA | http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json | `data/hotpotqa/hotpot_dev_distractor_v1.json` |
| PopQA | https://github.com/AlexTMallen/adaptive-retrieval/blob/main/data/popQA.tsv | `data/popqa/popQA.tsv` |
| ComplexWebQuestions | https://www.dropbox.com/scl/fo/nqujvpg2gc4y0ozkw3wgr/AOzjVEsdUhv2Fx2pamfJlSw?rlkey=746t7xehfqxf1zr867nxiq8aq&e=1 | `data/complexwebquestions/ComplexWebQuestions_dev.json` |

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

---

## External Retrieval Corpus

The experiments use BM25 retrieval over Wikipedia passages following the DPR Wikipedia split. Download the DPR passage corpus and build an Elasticsearch index locally.

```bash
mkdir -p data/dpr
wget -O data/dpr/psgs_w100.tsv.gz https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz

pushd data/dpr
gzip -d psgs_w100.tsv.gz
popd
```

Then index the passages with Elasticsearch according to your local setup and the scripts/configuration files provided in this repository.

---

## Environment

A minimal Python environment is sufficient for the included smoke tests and metric scripts.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For full model-based experiments, install the required deep-learning stack separately according to your hardware, CUDA version, model family, and adapter-training setup.

---

## Minimal Smoke Test

Run the following commands from the repository root:

```bash
python code_core/bask_core_minimal.py
python scripts/compute_qa_metrics.py --help
python scripts/bootstrap_ci.py --help
```

These tests do not require external datasets, pretrained models, LoRA adapters, or retrieval indexes.

---

## What Is Not Included

To keep the repository lightweight and compliant with third-party data and model licenses, this repository does not include:

- raw benchmark datasets;
- Wikipedia passage dumps;
- generated question-answer or rewriting outputs derived from benchmark passages;
- pretrained model weights;
- LoRA adapter checkpoints;
- full Elasticsearch indexes;
- full archived experiment run directories;
- large per-query prediction or retrieval logs unless explicitly released separately.

Use `DATASET_LINKS.md` and the instructions above to obtain external resources from their original providers.

---

## Reproducibility Notes

The repository is organized to support transparent reconstruction rather than one-click redistribution of all external resources. The recommended workflow is:

1. Download the required public datasets and DPR Wikipedia passages.
2. Build the BM25 retrieval index locally.
3. Review the configuration templates in `configs/`.
4. Run the metric and bootstrap scripts on the provided aggregate source data.
5. Use `code_core/bask_core_minimal.py` to inspect the core logic for coverage-aware grouping, sparse route-preserving invocation, rerouting probes, residual synergy, QA metrics, and bootstrap confidence intervals.
6. Add large run artifacts such as predictions, retrieval traces, and adapter logs only if you choose to release them separately.

---

## Relationship to PRAG

BASK-PRAG builds on the Parametric RAG research direction and follows the same broad benchmark setting. The main focus of this repository is not to redistribute the original PRAG implementation or datasets, but to provide a compact, auditable package for BASK-specific resource accounting, route preservation, and diagnostic analysis.

Public PRAG baseline repository:

```text
https://github.com/oneal2000/PRAG
```

---

## Citation

If you use this repository, please cite the accompanying paper and the original benchmark datasets. A `CITATION.cff` template is included and can be updated with the final publication metadata.

```bibtex
@misc{bask_prag,
  title  = {Budget-Aware Structured Knowledge Injection for Resource-Efficient Parametric Retrieval-Augmented Generation},
  author = {Yang, Chengyong and Yuan, Kairui and Li, Qiuyan and Liu, Xin},
  year   = {2026},
  note   = {Repository and reproducibility package}
}
```

---

## Contact

For questions about the repository or reconstruction package, please open a GitHub issue or contact the repository maintainers.
