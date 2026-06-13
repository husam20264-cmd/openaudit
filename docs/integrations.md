# OpenAudit Integrations

## LangChain

```python
from openaudit.validator import OpenAuditValidator
from openaudit.verifier import OpenAuditVerifier

# Before running a tool
event = {
    "event_id": "evt-...",
    "trace_id": "trace-...",
    "agent_id": "langchain_agent",
    "action_type": "tool_call",
    "action_details": {"tool": "search", "query": "..."},
    "risk_score": risk_score,
    "risk_level": risk_level,
    "approval_state": "pending",
    "approval_reason": "pending review",
    "evidence_hash": OpenAuditVerifier.compute_hash(event),
}

# Validate before sending
errors = OpenAuditValidator().validate_event(event)
if errors:
    raise ValueError(f"Invalid audit event: {errors}")
```

## AutoGen

Add a callback to the AutoGen agent that writes `.audit.jsonl` entries for every tool call:

```python
def audit_hook(sender, message, *args, **kwargs):
    event = {
        "event_id": f"evt-{uuid4().hex[:8]}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": sender.name,
        "action_type": "tool_call",
        ...
    }
    with open("audit.audit.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
```

## CrewAI

Add OpenAudit as a custom tool wrapper:

```python
class AuditedTool:
    def __init__(self, tool, audit_logger):
        self.tool = tool
        self.logger = audit_logger

    def run(self, **kwargs):
        event = self.logger.build_event(self.tool.name, kwargs)
        self.logger.write(event)
        return self.tool.run(**kwargs)
```

## OpenTelemetry

Events can be exported to OpenTelemetry via a bridge that maps `trace_id` → OpenTelemetry
span context, enabling visual tracing in Jaeger / Grafana.
