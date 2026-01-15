from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import time


@dataclass(frozen=True)
class MetricPoint:
    ts: int
    value: float


@dataclass
class MetricSeries:
    metric: str
    points: List[MetricPoint]
    type: str = "gauge"  # Datadog accepts gauge/count/rate
    tags: List[str] = field(default_factory=list)
    host: Optional[str] = None


def now_ts() -> int:
    return int(time.time())
