# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-License-Identifier: MIT
from abc import ABC, abstractmethod
from typing import Optional


#
# Base Profiler Classes
#
class BaseProfiler(ABC):
    """Abstract base class for profilers."""

    @abstractmethod
    def start(self):
        """Start profiling."""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop profiling."""
        raise NotImplementedError

    @abstractmethod
    def collect_report(self) -> Optional[str]:
        """Collect and return profiling report."""
        raise NotImplementedError

    def cleanup(self):
        """Clean up resources. Override if needed."""
        pass
