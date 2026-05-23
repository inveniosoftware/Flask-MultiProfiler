# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-License-Identifier: MIT
from flask import current_app
from werkzeug.local import LocalProxy

current_multiprofiler = LocalProxy(lambda: current_app.extensions["multiprofiler"])
"""Proxy for the multi-profiler extension."""
