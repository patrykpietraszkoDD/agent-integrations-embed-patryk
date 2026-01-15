from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os
import socket
import yaml


@dataclass
class AgentConfig:
    interval_seconds: int
    site: str
    api_key_env: str
    hostname: str
    tags: List[str]


@dataclass
class CheckConfig:
    name: str
    enabled: bool
    interval_seconds: int
    config: Dict[str, Any]


@dataclass
class Config:
    agent: AgentConfig
    checks: List[CheckConfig]


def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    agent_raw = raw.get("agent", {})
    hostname = agent_raw.get("hostname") or socket.gethostname()

    agent = AgentConfig(
        interval_seconds=int(agent_raw.get("interval_seconds", 10)),
        site=str(agent_raw.get("site", "datadoghq.com")),
        api_key_env=str(agent_raw.get("api_key_env", "DD_API_KEY")),
        hostname=hostname,
        tags=list(agent_raw.get("tags", [])),
    )

    checks: List[CheckConfig] = []
    for c in raw.get("checks", []):
        checks.append(
            CheckConfig(
                name=str(c["name"]),
                enabled=bool(c.get("enabled", True)),
                interval_seconds=int(c.get("interval_seconds", agent.interval_seconds)),
                config=dict(c.get("config", {})),
            )
        )

    return Config(agent=agent, checks=checks)


def get_api_key(env_name: str) -> str:
    v = os.getenv(env_name)
    if not v:
        raise RuntimeError(f"Missing API key env var: {env_name}")
    return v
