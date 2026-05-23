# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-License-Identifier: MIT
from .ext import MultiProfiler
from .proxies import current_multiprofiler

__all__ = ("MultiProfiler", "current_multiprofiler")
