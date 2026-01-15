from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List
import time


@dataclass
class ScheduledJob:
    name: str
    interval_seconds: int
    next_run: float
    run: Callable[[], None]


class Scheduler:
    def __init__(self) -> None:
        self.jobs: List[ScheduledJob] = []

    def add_job(self, name: str, interval_seconds: int, run: Callable[[], None]) -> None:
        now = time.time()
        self.jobs.append(
            ScheduledJob(name=name, interval_seconds=interval_seconds, next_run=now, run=run)
        )

    def run_forever(self) -> None:
        while True:
            now = time.time()
            due = [j for j in self.jobs if j.next_run <= now]

            for job in due:
                try:
                    job.run()
                finally:
                    job.next_run = now + job.interval_seconds

            # Sleep until next due job (bounded)
            next_run = min(j.next_run for j in self.jobs) if self.jobs else now + 1
            time.sleep(max(0.1, min(1.0, next_run - time.time())))
