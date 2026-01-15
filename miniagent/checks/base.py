from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from ..metrics import MetricSeries


@dataclass
class CheckContext:
    hostname: str
    base_tags: List[str]


class Check:
    """
    A minimal “integration” interface.

    - configure() is called once at startup
    - run() is called on schedule and returns MetricSeries
    """
    name: str = "base"

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def configure(self) -> None:
        pass

    def run(self, ctx: CheckContext) -> List[MetricSeries]:
        raise NotImplementedError
