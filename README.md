# OpenAudit

Open standard for AI agent audit logs.  
**Approval-First · Verifiable Evidence · Offline-First · Risk-Native**

## CLI

```bash
openaudit validate audit.json
openaudit batch-validate ./logs/
openaudit verify audit.json --evidence-dir ./proofs
```

## Install

```bash
pip install openaudit
```

## Community Validators

| Language | Repository | Maintainer |
|----------|------------|------------|
| TypeScript | validators/typescript/ | (open for contribution) |
| Go | validators/go/ | (open for contribution) |
| Rust | validators/rust/ | (open for contribution) |

To add a validator, submit a PR adding a row above and link your implementation.

## License

MIT
