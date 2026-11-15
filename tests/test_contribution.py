"""Exercise the branch route guard as Bash without checking out PR code."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_contribution_snapshot_keeps_its_source_identity() -> None:
    record = json.loads((ROOT / ".github/engineering-source.json").read_text())[
        "files"
    ][".github/workflows/contribution.yml"]
    source = (ROOT / record["source"]).read_bytes()
    assert (ROOT / ".github/workflows/contribution.yml").read_bytes() == source
    assert record["sha256"] == hashlib.sha256(source).hexdigest()


@pytest.mark.parametrize(
    ("head", "base", "head_repo", "accepted"),
    [
        ("refactorG01TemplateQuality", "test", "owner/sample", True),
        ("fixTimeout", "test", "fork/sample", True),
        ("test", "dev", "owner/sample", True),
        ("dev", "main", "owner/sample", True),
        ("refactorG01TemplateQuality", "main", "owner/sample", False),
        ("test", "main", "owner/sample", False),
        ("dev", "test", "owner/sample", False),
        ("refactor/task", "test", "owner/sample", False),
        ("RefactorTask", "test", "owner/sample", False),
        ("test", "dev", "fork/sample", False),
        ("dev", "main", "fork/sample", False),
        ("fixTimeout", "unknown", "owner/sample", False),
    ],
)
def test_contribution_routes_and_lower_camel_case(
    head: str, base: str, head_repo: str, accepted: bool
) -> None:
    for source in [".github", "template/.github"]:
        path = ROOT / source / "workflows/contribution.yml"
        workflow = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        step = workflow["jobs"]["contribution"]["steps"][0]
        result = subprocess.run(
            ["bash", "--noprofile", "--norc", "-euo", "pipefail", "-c", step["run"]],
            env={
                "PATH": os.environ["PATH"],
                "HEAD_REF": head,
                "BASE_REF": base,
                "HEAD_REPO": head_repo,
                "BASE_REPO": "owner/sample",
                "GITHUB_REPOSITORY": "owner/sample",
                "PR_TITLE": "fix(template): preserve CI event checks",
                "LEGACY_BRANCH": "",
            },
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        assert (result.returncode == 0) is accepted, (source, result.stderr)
