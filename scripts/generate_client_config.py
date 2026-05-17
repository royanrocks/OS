#!/usr/bin/env python3
"""Generate client-side runtime config for static deployment."""

from __future__ import annotations

import json
import os
from pathlib import Path


config = {
    "MAKE_WEBHOOK_URL": os.getenv("MAKE_WEBHOOK_URL", ""),
    "MAKE_API_KEY": os.getenv("MAKE_API_KEY", ""),
}

output = "window.OS_CONFIG = " + json.dumps(config, separators=(",", ":")) + ";\n"
Path("config.js").write_text(output, encoding="utf-8")

