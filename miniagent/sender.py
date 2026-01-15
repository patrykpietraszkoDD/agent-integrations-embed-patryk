from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import requests

from .metrics import MetricSeries


@dataclass
class DatadogSender:
    api_key: str
    site: str = "datadoghq.com"
    timeout_seconds: int = 5

    def submit(self, series: List[MetricSeries]) -> None:
        if not series:
            return

        url = f"https://api.{self.site}/api/v1/series"
        payload = {
            "series": [
                {
                    "metric": s.metric,
                    "points": [[p.ts, p.value] for p in s.points],
                    "type": s.type,
                    "tags": s.tags,
                }
                for s in series
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "DD-API-KEY": self.api_key,
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout_seconds)
        if resp.status_code >= 300:
            raise RuntimeError(f"Datadog submit failed: {resp.status_code} {resp.text}")
