"""
OpenAudit CLI
=============
Commands: validate, verify, batch-validate
"""

import sys
import json
from pathlib import Path

import click

from .validator import validate_file
from .verifier import verify_evidence


@click.group()
def cli():
    pass


@cli.command()
@click.argument("audit_file", type=click.Path(exists=True))
def validate(audit_file):
    """Validate audit file against OpenAudit schema."""
    ok, err = validate_file(Path(audit_file))
    if ok:
        click.echo("✓ Valid")
        sys.exit(0)
    else:
        click.echo(f"✗ Invalid: {err}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("audit_file", type=click.Path(exists=True))
@click.option("--evidence-dir", type=click.Path(exists=True), required=True)
def verify(audit_file, evidence_dir):
    """Verify evidence hashes in audit file against external proof files."""
    with open(audit_file) as f:
        data = json.load(f)
        events = data if isinstance(data, list) else [data]

    all_ok = True
    for event in events:
        ok, msg = verify_evidence(event, Path(evidence_dir))
        if not ok:
            click.echo(f"Failed for event {event.get('event_id')}: {msg}", err=True)
            all_ok = False
    if all_ok:
        click.echo("✓ All evidence verified")
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
@click.argument("audit_dir", type=click.Path(exists=True))
def batch_validate(audit_dir):
    """Validate all .audit.json and .audit.jsonl files in directory."""
    path = Path(audit_dir)
    files = list(path.glob("*.audit.json")) + list(path.glob("*.audit.jsonl")) + list(path.glob("*.json"))
    if not files:
        click.echo("No audit files found", err=True)
        sys.exit(1)

    failed = []
    for f in files:
        ok, err = validate_file(f)
        if not ok:
            failed.append((f.name, err))
            click.echo(f"✗ {f.name}: {err}")
        else:
            click.echo(f"✓ {f.name}")

    if failed:
        sys.exit(1)
    else:
        click.echo(f"All {len(files)} files valid")
        sys.exit(0)


if __name__ == "__main__":
    cli()
