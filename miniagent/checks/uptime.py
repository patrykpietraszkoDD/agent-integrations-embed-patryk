from __future__ import annotations

from typing import Any, Dict, List
import time

from .base import Check, CheckContext
from ..metrics import MetricPoint, MetricSeries, now_ts


class UptimeCheck(Check):
    name = "uptime"

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.metric_name = config.get("metric_name", "miniagent.uptime_seconds")
        self.start = time.time()

    def run(self, ctx: CheckContext) -> List[MetricSeries]:
        ts = now_ts()
        uptime_s = time.time() - self.start

        return [
            MetricSeries(
                metric=self.metric_name,
                points=[MetricPoint(ts, float(uptime_s))],
                tags=ctx.base_tags,
                host=ctx.hostname,
                type="gauge",
            )
        ]