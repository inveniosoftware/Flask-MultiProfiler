# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.0 - 2026-04-29

Initial release.

### Added

- Flask extension (`MultiProfiler`) coordinating per-request profiling sessions
  stored as SQLite databases under `MULTIPROFILER_STORAGE`.
- Code profiling via `pyinstrument` (CPU/wall-time function profiling).
- SQL profiling via `sqltap` (query timings, frequency, and statements).
- Search profiling: a custom profiler that intercepts `opensearchpy.trace`
  (configurable via `MULTIPROFILER_SEARCH_TRACE_LOGGER`) to capture request /
  response pairs from OpenSearch / Elasticsearch clients, with stack-frame
  capture for code context.
- Web blueprint for managing profiling sessions and viewing stored reports.
- Configuration: `MULTIPROFILER_STORAGE`, `MULTIPROFILER_SEARCH_TRACE_LOGGER`,
  `MULTIPROFILER_IGNORED_ENDPOINTS`, `MULTIPROFILER_PERMISSION`.
- Optional extras: `opensearch` (`opensearch-py ~= 2.1`) and `elasticsearch`
  (`elasticsearch ~= 7.17`).
