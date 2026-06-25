# OpenAudit

Open standard and CLI for verifiable, approval-first AI agent audit logs.

It helps teams record what an AI agent attempted, what was approved, what evidence was produced, and how risk was assessed — in a format that can be validated offline and verified independently.

## Quick example

Install OpenAudit:

```bash
pip install openaudit
```

Validate an audit log:

```bash
openaudit validate audit.json
```

Verify the audit log against local evidence:

```bash
openaudit verify audit.json --evidence-dir ./proofs
```

Expected output:

```
✓ audit.json is valid
✓ evidence files verified
✓ risk assessment present
✓ approval decision recorded
```

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
