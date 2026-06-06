# Dataset and External Resource Links

This file lists the external resources needed to reconstruct the BASK-PRAG experiments. The repository does **not** redistribute third-party datasets, Wikipedia passage dumps, pretrained model weights, LoRA adapter checkpoints, full Elasticsearch indexes, or large experiment logs.

Users should download each resource from its original public or provider-facing source and follow the corresponding license and terms of use.

## Benchmark datasets

| Resource | Purpose | Original source / download link | Expected local path |
|---|---|---|---|
| HotpotQA | Multi-hop QA benchmark | https://hotpotqa.github.io/ | `data/hotpotqa/` |
| HotpotQA dev distractor file | Controlled HotpotQA evaluation | http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json | `data/hotpotqa/hotpot_dev_distractor_v1.json` |
| 2WikiMultihopQA | Multi-hop QA benchmark | https://github.com/Alab-NII/2wikimultihop | `data/2wikimultihopqa/` |
| 2WikiMultihopQA data archive | Controlled 2Wiki evaluation | https://www.dropbox.com/s/ms2m13252h6xubs/data_ids_april7.zip?e=1 | `data/2wikimultihopqa/` |
| PopQA | Long-tail factual QA benchmark | https://github.com/AlexTMallen/adaptive-retrieval | `data/popqa/` |
| PopQA TSV file | Controlled PopQA evaluation | https://raw.githubusercontent.com/AlexTMallen/adaptive-retrieval/main/data/popQA.tsv | `data/popqa/popQA.tsv` |
| ComplexWebQuestions | Compositional QA benchmark | https://github.com/yuancu/complex-web-questions-dataset | `data/complexwebquestions/` |
| ComplexWebQuestions archive | Controlled CWQ evaluation | https://www.dropbox.com/scl/fo/nqujvpg2gc4y0ozkw3wgr/AOzjVEsdUhv2Fx2pamfJlSw?rlkey=746t7xehfqxf1zr867nxiq8aq&e=1 | `data/complexwebquestions/ComplexWebQuestions_dev.json` |

## Retrieval corpus and index

| Resource | Purpose | Original source / download link | Expected local path |
|---|---|---|---|
| DPR Wikipedia passage split | BM25 retrieval corpus | https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz | `data/dpr/psgs_w100.tsv` |
| Elasticsearch | Local BM25 index | https://www.elastic.co/elasticsearch/ | local installation |

Suggested commands:

```bash
mkdir -p data/dpr
wget -O data/dpr/psgs_w100.tsv.gz https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz
gzip -d data/dpr/psgs_w100.tsv.gz
```

Build the Elasticsearch index locally according to your environment and the configuration templates in `configs/`.

## Baseline and related repositories

| Resource | Purpose | Link |
|---|---|---|
| PRAG baseline repository | Public baseline direction followed by BASK-PRAG | https://github.com/oneal2000/PRAG |
| Adaptive retrieval / PopQA repository | PopQA source | https://github.com/AlexTMallen/adaptive-retrieval |

## Notes

- The paths above are suggested local reconstruction paths.
- The repository stores aggregate source data, configuration templates, prompt templates, and metric scripts, but not restricted or large third-party artifacts.
- If a link changes, use the corresponding project page to locate the official replacement source.
