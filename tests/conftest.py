import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_network.dataio import DevData  # noqa: E402
from agent_network.scoring import compute_scores  # noqa: E402


@pytest.fixture(scope="session")
def data() -> DevData:
    return DevData()


@pytest.fixture(scope="session")
def embeddings(data):
    """Session-wide BGE scores, cached next to the package after first run."""
    return compute_scores(data, cache_path=ROOT / ".score_cache.npz")
