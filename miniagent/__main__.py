from __future__ import annotations

import argparse
import sys
from typing import List

from .config import load_config, get_api_key
from .sender import DatadogSender
from .scheduler import Scheduler
from .checks import CHECKS
from .checks.base import CheckContext


def main() -> int:
    parser = argparse.ArgumentParser(description="mini-agent")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    api_key = get_api_key(cfg.agent.api_key_env)

    sender = DatadogSender(api_key=api_key, site=cfg.agent.site)
    ctx = CheckContext(hostname=cfg.agent.hostname, base_tags=cfg.agent.tags)

    scheduler = Scheduler()

    for c in cfg.checks:
        if not c.enabled:
            continue
        if c.name not in CHECKS:
            raise RuntimeError(f"Unknown check: {c.name}. Known: {sorted(CHECKS.keys())}")

        check = CHECKS[c.name](c.config)
        check.configure()

        def make_runner(check_name: str, check_obj):
            def _run():
                series = check_obj.run(ctx)
                sender.submit(series)
                print(f"[ok] ran {check_name}: submitted {len(series)} series")
            return _run

        scheduler.add_job(name=c.name, interval_seconds=c.interval_seconds, run=make_runner(c.name, check))

    if not scheduler.jobs:
        raise RuntimeError("No enabled checks configured.")

    print(f"mini-agent starting (site={cfg.agent.site}, hostname={cfg.agent.hostname})")
    scheduler.run_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
