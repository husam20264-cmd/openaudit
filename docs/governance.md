# OpenAudit Governance Guide

## Policy Integration

OpenAudit events are designed to be consumed by policy engines. Each event carries
enough context to evaluate whether the action should proceed.

### Decision Flow

```
Agent Action
    ↓
RiskEngine.score() → risk_score + risk_level
    ↓
AuditLogger.log() → event with approval_state=pending
    ↓
PolicyEngine.evaluate(event) → approved / blocked / escalated
    ↓
ApprovalActor responds → event with final approval_state
    ↓
Executor runs / skips → status = completed / failed / cancelled
```

## Compliance

### Evidence Chain

Each event's `evidence_hash` binds it to the previous event in the trace:

```
evt-001 (root)  ──hash──→  evt-002  ──hash──→  evt-003
   trace_id=abc                abc                  abc
```

A verifier can detect:
- Missing events (gap in chain)
- Tampered events (hash mismatch)
- Broken traces (trace_id mismatch)

### Audit Trail for Regulations

OpenAudit maps to common regulatory requirements:

| Requirement | OpenAudit Field |
|-------------|-----------------|
| Who acted? | `agent_id`, `approval_actor` |
| What was done? | `action_type`, `action_details` |
| When? | `timestamp` |
| Why was it allowed/blocked? | `approval_reason` |
| Was evidence preserved? | `evidence_hash` |
| Full trace? | `trace_id`, `parent_event_id` |
