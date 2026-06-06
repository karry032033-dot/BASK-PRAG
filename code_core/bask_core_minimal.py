#!/usr/bin/env python3
"""Dependency-light reference implementation of core BASK logic.

This script is a compact, auditable implementation for smoke testing and
review. It illustrates:
  - coverage-aware grouped construction;
  - sparse route-preserving adapter invocation;
  - normalized QA metrics;
  - bootstrap confidence intervals;
  - posterior two-passage synergy auditing.

It does not train LoRA adapters, load pretrained models, build Elasticsearch
indexes, or redistribute third-party benchmark data.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random
import re
import string
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


PassageId = str
QueryId = str
AdapterId = str


@dataclass(frozen=True)
class QueryRecord:
    """A query and its ordered retrieved passage identifiers."""

    query_id: QueryId
    retrieved_passages: Tuple[PassageId, ...]


@dataclass(frozen=True)
class AdapterCacheEntry:
    """A reusable passage-level adapter with its source passage identifier."""

    passage_id: PassageId
    adapter_id: AdapterId
    covered_queries: Tuple[QueryId, ...]


def coverage_map(records: Sequence[QueryRecord], depth: Optional[int] = None) -> Dict[PassageId, set]:
    """Map each passage to the set of queries that retrieved it."""

    gamma: Dict[PassageId, set] = defaultdict(set)
    for record in records:
        passages = record.retrieved_passages[:depth] if depth is not None else record.retrieved_passages
        for passage_id in passages:
            gamma[passage_id].add(record.query_id)
    return gamma


def greedy_coverage_selection(
    records: Sequence[QueryRecord],
    target_coverage: float = 1.0,
    budget: Optional[int] = None,
    depth: Optional[int] = None,
) -> Tuple[List[PassageId], Dict[PassageId, set]]:
    """Select reusable passages by greedy set cover.

    The cost unit is one supervision-generation call per selected passage.
    """

    if not 0 < target_coverage <= 1:
        raise ValueError("target_coverage must be in the interval (0, 1].")

    gamma = coverage_map(records, depth=depth)
    all_queries = {record.query_id for record in records}
    covered_queries = set()
    selected: List[PassageId] = []

    max_selected = budget if budget is not None else len(gamma)
    target_count = max(1, int(len(all_queries) * target_coverage + 0.999999))

    while len(covered_queries) < target_count and len(selected) < max_selected:
        best_passage = None
        best_new_cover = set()

        for passage_id, query_set in gamma.items():
            if passage_id in selected:
                continue
            new_cover = query_set - covered_queries
            if len(new_cover) > len(best_new_cover):
                best_passage = passage_id
                best_new_cover = new_cover

        if best_passage is None or not best_new_cover:
            break

        selected.append(best_passage)
        covered_queries.update(best_new_cover)

    return selected, gamma


def build_adapter_cache(selected: Sequence[PassageId], gamma: Mapping[PassageId, Iterable[QueryId]]) -> Dict[PassageId, AdapterCacheEntry]:
    """Create a lightweight adapter cache from selected passages."""

    cache: Dict[PassageId, AdapterCacheEntry] = {}
    for passage_id in selected:
        cache[passage_id] = AdapterCacheEntry(
            passage_id=passage_id,
            adapter_id=f"adapter::{passage_id}",
            covered_queries=tuple(sorted(gamma.get(passage_id, []))),
        )
    return cache


def sparse_first_route(record: QueryRecord, cache: Mapping[PassageId, AdapterCacheEntry], backbone: Sequence[AdapterId]) -> List[AdapterId]:
    """Replace only the first slot when the first retrieved passage has a grouped adapter."""

    route = list(backbone)
    if record.retrieved_passages and record.retrieved_passages[0] in cache:
        route[0] = cache[record.retrieved_passages[0]].adapter_id
    return route


def sparse_adaptive_route(
    record: QueryRecord,
    cache: Mapping[PassageId, AdapterCacheEntry],
    gamma: Mapping[PassageId, Iterable[QueryId]],
    backbone: Sequence[AdapterId],
) -> List[AdapterId]:
    """Replace one eligible slot using construction-side support size."""

    route = list(backbone)
    eligible: List[Tuple[int, PassageId, int]] = []

    for index, passage_id in enumerate(record.retrieved_passages[: len(route)]):
        if passage_id in cache:
            eligible.append((index, passage_id, len(set(gamma.get(passage_id, [])))))

    if not eligible:
        return route

    index, passage_id, _support = max(eligible, key=lambda item: (item[2], -item[0]))
    route[index] = cache[passage_id].adapter_id
    return route


def normalize_answer(text: str) -> str:
    """Normalize short answers for exact-match and token-overlap metrics."""

    text = text.lower()
    text = "".join(ch for ch in text if ch not in string.punctuation)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def f1_score(prediction: str, gold: str) -> float:
    """Compute normalized word-level F1."""

    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(gold).split()

    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0

    common = defaultdict(int)
    for token in gold_tokens:
        common[token] += 1

    overlap = 0
    for token in pred_tokens:
        if common[token] > 0:
            overlap += 1
            common[token] -= 1

    if overlap == 0:
        return 0.0

    precision = overlap / len(pred_tokens)
    recall = overlap / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def bootstrap_mean_ci(values: Sequence[float], n_boot: int = 1000, seed: int = 13, alpha: float = 0.05) -> Tuple[float, float, float]:
    """Return mean and percentile bootstrap confidence interval."""

    if not values:
        raise ValueError("values must not be empty.")

    rng = random.Random(seed)
    sample_size = len(values)
    means = []

    for _ in range(n_boot):
        sample = [values[rng.randrange(sample_size)] for _ in range(sample_size)]
        means.append(sum(sample) / sample_size)

    means.sort()
    lower = means[int((alpha / 2) * n_boot)]
    upper = means[int((1 - alpha / 2) * n_boot) - 1]
    mean = sum(values) / sample_size
    return mean, lower, upper


def residual_synergy(single_scores: Mapping[int, float], pair_scores: Mapping[Tuple[int, int], float]) -> float:
    """Post hoc residual synergy: best pair score minus best single-route score."""

    if not single_scores or not pair_scores:
        raise ValueError("single_scores and pair_scores must not be empty.")

    best_single = max(single_scores.values())
    best_pair = max(pair_scores.values())
    return best_pair - best_single


def demo() -> None:
    """Run a small deterministic smoke test."""

    records = [
        QueryRecord("q1", ("p1", "p2", "p3")),
        QueryRecord("q2", ("p1", "p4", "p5")),
        QueryRecord("q3", ("p2", "p1", "p6")),
        QueryRecord("q4", ("p7", "p1", "p2")),
    ]

    selected, gamma = greedy_coverage_selection(records, target_coverage=1.0, budget=3, depth=3)
    cache = build_adapter_cache(selected, gamma)
    backbone = ["prag_slot_1", "prag_slot_2", "prag_slot_3"]

    print("Selected reusable passages:", selected)
    print("Realized construction calls:", len(selected))

    for record in records:
        print(record.query_id, "SparseFirst:", sparse_first_route(record, cache, backbone))
        print(record.query_id, "SparseAdaptive:", sparse_adaptive_route(record, cache, gamma, backbone))

    example_f1 = f1_score("the capital of France is Paris", "Paris")
    print("Example normalized F1:", round(example_f1, 4))

    mean, low, high = bootstrap_mean_ci([0.2, 0.3, 0.4, 0.5], n_boot=200, seed=7)
    print("Example bootstrap mean/CI:", round(mean, 4), round(low, 4), round(high, 4))

    synergy = residual_synergy({0: 0.25, 1: 0.30, 2: 0.10}, {(0, 1): 0.42, (0, 2): 0.31, (1, 2): 0.28})
    print("Example residual synergy:", round(synergy, 4))


if __name__ == "__main__":
    demo()
