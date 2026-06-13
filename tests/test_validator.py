"""Tests for OpenAudit Validator."""

import json
import pytest
from openaudit.validator import validate_event, validate_file


def test_valid_event():
    event = {
        "event_id": "123e4567-e89b-12d3-a456-426614174000",
        "trace_id": "trace-1",
        "parent_event_id": None,
        "root_event_id": "123e4567-e89b-12d3-a456-426614174000",
        "timestamp": "2025-01-15T10:00:00Z",
        "agent_id": "test_agent",
        "session_id": "test_session",
        "action_type": "tool_call",
        "action_details": {"tool": "test"},
        "risk_score": 0.5,
        "risk_level": "medium",
        "approval_state": "approved",
        "approval_reason": "auto",
        "execution_status": "success",
        "evidence_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }
    ok, _ = validate_event(event)
    assert ok


def test_missing_required():
    event = {}
    ok, err = validate_event(event)
    assert not ok
    assert "'event_id' is a required property" in err


def test_invalid_risk_score_range():
    event = {
        "event_id": "123e4567-e89b-12d3-a456-426614174001",
        "trace_id": "trace-2",
        "parent_event_id": None,
        "root_event_id": "123e4567-e89b-12d3-a456-426614174001",
        "timestamp": "2025-01-15T10:00:00Z",
        "agent_id": "test_agent",
        "session_id": "test_session",
        "action_type": "tool_call",
        "action_details": {"tool": "test"},
        "risk_score": 1.5,
        "risk_level": "medium",
        "approval_state": "approved",
        "approval_reason": "auto",
        "execution_status": "success",
        "evidence_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }
    ok, err = validate_event(event)
    assert not ok
    assert "1.5 is greater than the maximum" in err


def test_validate_example_files():
    import pathlib
    examples = pathlib.Path(__file__).resolve().parent.parent / "examples"
    for path in sorted(examples.glob("*.json")):
        ok, err = validate_file(path)
        assert ok, f"{path.name}: {err}"
