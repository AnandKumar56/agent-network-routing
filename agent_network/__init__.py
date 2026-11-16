"""Stage 1 routing core: dedup, binding hard filters, dated evidence, M1 scoring.

Design and measured baselines: docs/DESIGN.md and docs/RESULTS.md.
"""
from .dataio import DevData
from .facets import hard_filter
from .evidence import relationship_hints, rule_hits
from .routing import metric_row, route_post

__all__ = ["DevData", "hard_filter", "rule_hits", "relationship_hints", "route_post", "metric_row"]
