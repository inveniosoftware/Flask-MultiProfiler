# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Flask-MultiProfiler is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
from bs4 import BeautifulSoup

from flask_multiprofiler.models import ProfileSessions
from tests.helpers import disable_profiling, enable_profiling, get_profiler_report


def test_all_profilers_together(app, client):
    """Test all profiler types work together."""
    enable_profiling(client, ["code", "sql", "search"])

    response = client.get("/dashboard")
    assert response.status_code == 200

    sessions = ProfileSessions.get_all_sessions()
    assert len(sessions) == 1

    session_id = list(sessions.keys())[0]
    session_entries = sessions[session_id]
    assert len(session_entries) == 1

    session_data = session_entries[0]

    # All three profiler types must generate reports
    assert session_data.has_code_report
    assert session_data.has_sql_report
    assert session_data.has_search_report

    # Validate that each report exists and is non-empty
    code_report = ProfileSessions.get_request_report(
        session_id, session_data.id, "code"
    )
    sql_report = ProfileSessions.get_request_report(session_id, session_data.id, "sql")
    search_report = ProfileSessions.get_request_report(
        session_id, session_data.id, "search"
    )

    assert code_report is not None
    assert len(code_report) > 1000  # Should be substantial HTML content

    assert sql_report is not None
    assert len(sql_report) > 1000  # Should be substantial HTML content

    assert search_report is not None
    assert len(search_report) > 10  # Should contain at least some content


def test_selective_enabling(app, client):
    """Test that profiler configuration controls which profilers are active."""
    # Clear any existing sessions first
    if ProfileSessions.storage_dir.exists():
        ProfileSessions.clear_sessions()

    # Test: Enable code and SQL profilers, but not search
    enable_profiling(client, ["code", "sql"])

    response = client.get("/queries")  # Endpoint that triggers SQL queries
    assert response.status_code == 200

    sessions = ProfileSessions.get_all_sessions()
    assert len(sessions) == 1

    session_id = list(sessions.keys())[0]
    session_entries = sessions[session_id]
    assert len(session_entries) == 1

    session_data = session_entries[0]

    # Code and SQL profilers were enabled and should generate reports
    assert session_data.has_code_report
    assert session_data.has_sql_report

    # Search profiler behavior - validate search report content
    if session_data.has_search_report:
        search_report = ProfileSessions.get_request_report(
            session_id, session_data.id, "search"
        )
        # Should contain "no search queries" message since no search operations occurred
        assert "no search queries recorded" in search_report.lower()


def test_report_independence(app, client):
    """Test each profiler generates independent data."""
    # Clear any existing sessions first
    if ProfileSessions.storage_dir.exists():
        ProfileSessions.clear_sessions()

    enable_profiling(client, ["code", "sql", "search"])

    # Use endpoint that triggers both SQL and code operations
    response = client.get("/dashboard")
    assert response.status_code == 200

    code_report = get_profiler_report(app, "code")
    sql_report = get_profiler_report(app, "sql")
    search_report = get_profiler_report(app, "search")

    # All reports must exist
    assert code_report is not None
    assert sql_report is not None
    assert search_report is not None

    # Code report must be substantial content
    assert len(code_report) > 1000

    # SQL report must be substantial and contain SQL query data
    assert len(sql_report) > 1000
    sql_text = BeautifulSoup(sql_report, "html.parser").get_text()
    assert any(
        keyword in sql_text.upper() for keyword in ["SELECT", "FROM", "WHERE", "COUNT"]
    )

    # Search report must contain search-related content (even if no queries)
    assert len(search_report) > 10
    assert "search" in search_report.lower() or "query" in search_report.lower()


def test_profiler_isolation(app, client):
    """Test profilers track requests independently with different configurations."""
    # Clear any existing sessions first
    if ProfileSessions.storage_dir.exists():
        ProfileSessions.clear_sessions()

    # Test: Multiple requests with different profiler configurations
    code_session_id = enable_profiling(client, ["code"])
    response1 = client.get("/compute")
    assert response1.status_code == 200

    # Session start is not re-entrant: stop first session before changing config.
    disable_profiling(client)

    # Change profiler configuration and make another request
    sql_session_id = enable_profiling(client, ["sql"])
    response2 = client.get("/queries")
    assert response2.status_code == 200

    # Validate session structure
    sessions = ProfileSessions.get_all_sessions()
    assert code_session_id in sessions
    assert sql_session_id in sessions

    code_session_entries = sessions[code_session_id]
    sql_session_entries = sessions[sql_session_id]

    # Code-only session should contain a code report and no SQL report.
    assert any(
        entry.has_code_report and not entry.has_sql_report
        for entry in code_session_entries
    )
    # SQL session should contain at least one SQL report.
    assert any(entry.has_sql_report for entry in sql_session_entries)
