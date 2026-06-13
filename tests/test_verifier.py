"""Tests for OpenAudit Verifier."""

import tempfile
from pathlib import Path

from openaudit.verifier import verify_evidence


def test_verify_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        evidence_file = Path(tmpdir) / "ev.proof"
        content = b"test evidence"
        evidence_file.write_bytes(content)
        expected_hash = "d3212848da94be5ccf76cc161a59ab8039406bd87585e4a4b166e47fca7b1109"

        event = {
            "event_id": "abc",
            "evidence_hash": expected_hash,
            "evidence_location": str(evidence_file),
        }
        ok, msg = verify_evidence(event)
        assert ok
        assert msg == "OK"


def test_verify_hash_mismatch():
    with tempfile.TemporaryDirectory() as tmpdir:
        evidence_file = Path(tmpdir) / "ev.proof"
        evidence_file.write_bytes(b"different")
        event = {
            "event_id": "abc",
            "evidence_hash": "36bbe50ed96841d10443bcb670d6554f0a34b761be67ec9c4a8ad2c0c44ca42c",
            "evidence_location": str(evidence_file),
        }
        ok, msg = verify_evidence(event)
        assert not ok
        assert "mismatch" in msg


def test_verify_missing_hash():
    event = {"event_id": "abc"}
    ok, msg = verify_evidence(event)
    assert not ok
    assert "No evidence_hash" in msg


def test_verify_no_location():
    event = {"event_id": "abc", "evidence_hash": "0" * 64}
    ok, msg = verify_evidence(event)
    assert not ok
    assert "No evidence location" in msg
