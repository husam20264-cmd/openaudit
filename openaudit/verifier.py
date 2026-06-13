"""
OpenAudit Verifier
==================
Verifies evidence integrity by recomputing SHA-256 hashes from external proof files.
"""

import hashlib
import json
from pathlib import Path


def verify_evidence(event, evidence_dir=None):
    """Verify evidence_hash against an external proof file.

    Returns (ok: bool, message: str).
    """
    expected_hash = event.get("evidence_hash")
    if not expected_hash:
        return False, "No evidence_hash field"

    if "evidence_location" in event:
        evidence_path = Path(event["evidence_location"])
    elif evidence_dir:
        evidence_path = Path(evidence_dir) / f"{event['event_id']}.proof"
    else:
        return False, "No evidence location provided"

    if not evidence_path.exists():
        return False, f"Evidence file not found: {evidence_path}"

    content = evidence_path.read_bytes()
    actual_hash = hashlib.sha256(content).hexdigest()

    if actual_hash != expected_hash:
        return False, f"Hash mismatch: expected {expected_hash}, got {actual_hash}"
    return True, "OK"
