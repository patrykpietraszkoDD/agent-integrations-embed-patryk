from __future__ import annotations

from typing import Any, Dict, List
import psutil

from .base import Check, CheckContext
from ..metrics import MetricPoint, MetricSeries, now_ts


class SystemCheck(Check):
    name = "system"

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.disk_paths = config.get("disk_paths", ["/"])

    def configure(self) -> None:
        # Prime CPU percent so the next call reflects interval usage
        psutil.cpu_percent(interval=None)

    def run(self, ctx: CheckContext) -> List[MetricSeries]:
        ts = now_ts()

        cpu_pct = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()

        series: List[MetricSeries] = [
            MetricSeries(
                metric="miniagent.system.cpu.pct",
                points=[MetricPoint(ts, float(cpu_pct))],
                tags=ctx.base_tags,
                host=ctx.hostname,
                type="gauge",
            ),
            MetricSeries(
                metric="miniagent.system.mem.used_pct",
                points=[MetricPoint(ts, float(mem.percent))],
                tags=ctx.base_tags,
                host=ctx.hostname,
                type="gauge",
            ),
        ]

        for path in self.disk_paths:
            du = psutil.disk_usage(path)
            series.append(
                MetricSeries(
                    metric="miniagent.system.disk.used_pct",
                    points=[MetricPoint(ts, float(du.percent))],
                    tags=ctx.base_tags + [f"mount:{path}"],
                    host=ctx.hostname,
                    type="gauge",
                )
            )

        return series