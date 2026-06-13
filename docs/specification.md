# OpenAudit Specification v0.1

**Approval-First · Verifiable Evidence · Offline-First · Risk-Native**

## Principles

### 1. Approval-First Governance
Every event must include `approval_state` and `approval_reason`. The approval decision is
independent from execution status — an action can be **approved but fail**, or **blocked
before execution**.

```
approval_state ∈ {pending, approved, blocked, escalated}
status         ∈ {pending, running, completed, failed, cancelled}
```

### 2. Verifiable Evidence
Every event includes `evidence_hash` (SHA-256 hex). Anyone can recompute the hash from the
event payload and verify integrity. Optional `evidence_location` points to external proof
files (logs, screenshots, network captures).

### 3. Offline-First
Audit logs are plain JSON Lines (`.audit.jsonl`) or single JSON arrays (`.audit.json`).
No mandatory network calls. The CLI runs entirely offline.

### 4. Risk-Native
`risk_score` [0..1] and `risk_level` {low, medium, high, critical} are required fields,
not metadata. This enables risk trend analysis without an external scoring system.

## Schema

Defined in `schema/open_audit_schema.json`. Key fields:

| Field | Required | Description |
|-------|----------|-------------|
| `event_id` | ✅ | Unique event identifier |
| `trace_id` | ✅ | End-to-end trace identifier |
| `parent_event_id` | ❌ | Immediate parent for decision chains |
| `root_event_id` | ❌ | Root event for full replay |
| `action_type` | ✅ | One of `tool_call`, `data_access`, `approval_request`, `approval_response`, `blocked_action` |
| `risk_score` | ✅ | Float [0.0, 1.0] |
| `risk_level` | ✅ | `low`, `medium`, `high`, `critical` |
| `approval_state` | ✅ | `pending`, `approved`, `blocked`, `escalated` |
| `status` | ❌ | `pending`, `running`, `completed`, `failed`, `cancelled` |
| `evidence_hash` | ✅ | SHA-256 hex digest |

## File Format

- **Extension**: `.audit.json` (single event or array) or `.audit.jsonl` (one event per line)
- **Encoding**: UTF-8
- **Multiple events**: JSONL is preferred for streaming / append-only logs

## CLI

```bash
openaudit validate <file>          # Validate event structure
openaudit verify <file>             # Verify evidence integrity
openaudit batch-validate <dir>      # Batch validate directory
openaudit trace <trace_id>          # Trace event chain
```

## Versioning

This specification uses `v0.1` (pre-release). The schema URL follows:
`https://openaudit.dev/schemas/audit_event_v{MAJOR}.{MINOR}.json`
