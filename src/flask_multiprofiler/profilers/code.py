# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-License-Identifier: MIT
from typing import Optional

import pyinstrument

from .base import BaseProfiler


class CodeProfiler(BaseProfiler):
    """Profiler for code execution using pyinstrument."""

    def __init__(self):
        self.profiler = None

    def start(self):
        """Start code profiling."""
        self.profiler = pyinstrument.Profiler()
        self.profiler.start()

    def stop(self):
        """Stop code profiling."""
        if self.profiler:
            self.profiler.stop()

    def collect_report(self) -> Optional[str]:
        """Collect HTML report from pyinstrument."""
        if self.profiler:
            return self.profiler.output_html()
        return None
