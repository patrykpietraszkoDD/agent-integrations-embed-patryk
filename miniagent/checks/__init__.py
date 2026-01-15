from __future__ import annotations

from typing import Dict, Type
from .base import Check
from .system import SystemCheck
from .uptime import UptimeCheck


CHECKS: Dict[str, Type[Check]] = {
    SystemCheck.name: SystemCheck,
    UptimeCheck.name: UptimeCheck,
}
