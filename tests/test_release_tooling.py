"""Exercise source, artifact and receipt boundaries without a Docker daemon."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from types import ModuleType

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def release() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "portable_release", ROOT / "template/docker/release.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def source_file(root: Path, character: str = "a") -> None:
    (root / "coverage").mkdir(exist_ok=True)
    (root / "coverage/source.json").write_text(
        json.dumps({"commit": None, "dirty": True, "contentSha256": character * 64})
    )


def plan_file(root: Path, checks: list[str], scope: str = "full") -> None:
    (root / "coverage/ci-plan.json").write_text(
        json.dumps({"scope": scope, "checks": checks})
    )


def test_receipt_checks_and_stale_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, release: ModuleType
) -> None:
    monkeypatch.chdir(tmp_path)
    source_file(tmp_path)
    plan_file(tmp_path, ["check"])
    runner = CliRunner()
    assert runner.invoke(release.app, ["receipt", "init"]).exit_code == 0
    args = [
        "receipt",
        "record",
        "--name",
        "check",
        "--command",
        "make check",
        "--exit-code",
        "0",
    ]
    assert runner.invoke(release.app, args).exit_code == 0
    assert runner.invoke(release.app, args).exit_code != 0
    source_file(tmp_path, "b")
    result = runner.invoke(release.app, ["receipt", "finish", "--status", "passed"])
    assert result.exit_code != 0
    assert (
        json.loads((tmp_path / "coverage/ci-local.json").read_text())["status"]
        == "failed"
    )


@pytest.mark.parametrize("exit_code", [0, 7])
def test_receipt_failure_is_not_relabelled_passed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, release: ModuleType, exit_code: int
) -> None:
    monkeypatch.chdir(tmp_path)
    source_file(tmp_path)
    plan_file(tmp_path, ["test"])
    runner = CliRunner()
    assert runner.invoke(release.app, ["receipt", "init"]).exit_code == 0
    assert (
        runner.invoke(
            release.app,
            [
                "receipt",
                "record",
                "--name",
                "test",
                "--command",
                "make test",
                "--exit-code",
                str(exit_code),
            ],
        ).exit_code
        == 0
    )
    result = runner.invoke(release.app, ["receipt", "finish", "--status", "passed"])
    assert (result.exit_code == 0) == (exit_code == 0)
    data = json.loads((tmp_path / "coverage/ci-local.json").read_text())
    assert data["checks"][0]["exitCode"] == exit_code
    assert "schemaVersion" in data and "startedAt" in data


def test_package_metadata_agreement_and_stale_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, release: ModuleType
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="demo-lib"\nversion="0.4.0.dev2"\n'
    )
    dist = tmp_path / "dist"
    dist.mkdir()
    metadata = b"Name: demo_lib\nVersion: 0.4.0.dev2\n"
    wheel = dist / "demo_lib-0.4.0.dev2-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("demo_lib-0.4.0.dev2.dist-info/METADATA", metadata)
    with tarfile.open(dist / "demo_lib-0.4.0.dev2.tar.gz", "w:gz") as archive:
        member = tarfile.TarInfo("demo_lib-0.4.0.dev2/PKG-INFO")
        member.size = len(metadata)
        archive.addfile(member, io.BytesIO(metadata))
    runner = CliRunner()
    assert runner.invoke(release.app, ["release-check"]).exit_code != 0
    source_file(tmp_path)
    (tmp_path / "coverage/build-source.json").write_bytes(
        (tmp_path / "coverage/source.json").read_bytes()
    )
    assert runner.invoke(release.app, ["capture-build"]).exit_code == 0
    assert runner.invoke(release.app, ["release-check"]).exit_code == 0
    source_file(tmp_path, "b")
    assert runner.invoke(release.app, ["release-check"]).exit_code != 0
    source_file(tmp_path)
    assert len(release.checked_artifacts()) == 2
    wheel.write_bytes(b"changed")
    with pytest.raises(ValueError, match="checksum"):
        release.checked_artifacts()
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="demo-lib"\nversion="not a version"\n'
    )
    assert runner.invoke(release.app, ["version"]).exit_code != 0


def test_bundle_is_reproducible_and_content_checked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, release: ModuleType
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "VERSION").write_text("0.2.0\n")
    (tmp_path / "README.md").write_text("# Bundle\n")
    (tmp_path / ".env").write_text("SYNTHETIC_SECRET=not-published\n")
    subprocess.run(
        ["bash", str(ROOT / "template/docker/source_identity.sh")],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "coverage/build-source.json").write_bytes(
        (tmp_path / "coverage/source.json").read_bytes()
    )
    runner = CliRunner()
    assert runner.invoke(release.app, ["bundle-build"]).exit_code == 0
    first = next((tmp_path / "dist").glob("*.tar.gz")).read_bytes()
    assert runner.invoke(release.app, ["bundle-build"]).exit_code == 0
    assert next((tmp_path / "dist").glob("*.tar.gz")).read_bytes() == first
    assert runner.invoke(release.app, ["capture-build"]).exit_code == 0
    assert runner.invoke(release.app, ["release-check"]).exit_code == 0
    with tarfile.open(next((tmp_path / "dist").glob("*.tar.gz"))) as archive:
        assert ".env" not in archive.getnames()
    (tmp_path / "README.md").write_text("# Changed\n")
    assert runner.invoke(release.app, ["bundle-verify"]).exit_code != 0


def test_source_identity_git_and_unversioned_boundaries(tmp_path: Path) -> None:
    script = ROOT / "template/docker/source_identity.sh"
    (tmp_path / "input.txt").write_text("one")

    def identity() -> dict[str, object]:
        subprocess.run(["bash", str(script)], cwd=tmp_path, check=True)
        return json.loads((tmp_path / "coverage/source.json").read_text())

    first = identity()
    assert first["commit"] is None and first["dirty"] is True
    assert identity() == first
    subprocess.run(["git", "init", "--quiet"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text("coverage/\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)

    def commit() -> None:
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "--quiet",
                "--allow-empty",
                "-m",
                "fixture",
            ],
            cwd=tmp_path,
            check=True,
        )

    commit()
    second = identity()
    assert second["dirty"] is False
    commit()
    assert identity()["contentSha256"] == second["contentSha256"]
    assert identity()["commit"] != second["commit"]
    (tmp_path / "input.txt").unlink()
    assert identity()["contentSha256"] != second["contentSha256"]
    (tmp_path / "input.txt").symlink_to("/outside/source-not-read")
    assert identity()["dirty"] is True


def test_make_prepare_failure_leaves_blocked_receipt(tmp_path: Path) -> None:
    docker = tmp_path / "docker"
    docker.mkdir()
    (docker / "source_identity.sh").write_bytes(
        (ROOT / "template/docker/source_identity.sh").read_bytes()
    )
    (tmp_path / "Makefile").write_text(
        f"DOCKER := false\ninclude {ROOT}/template/docker/quality.mk\n"
    )
    result = subprocess.run(
        ["make", "ci-local"], cwd=tmp_path, capture_output=True, text=True
    )
    assert result.returncode != 0
    receipt = json.loads((tmp_path / "coverage/ci-local.json").read_text())
    assert receipt["status"] == "blocked"
    assert receipt["checks"] == []
    assert receipt["source"]["commit"] is None


def test_actual_quality_build_error_is_failed(tmp_path: Path) -> None:
    docker = tmp_path / "docker"
    docker.mkdir()
    (docker / "source_identity.sh").write_bytes(
        (ROOT / "template/docker/source_identity.sh").read_bytes()
    )
    stub = tmp_path / "docker-stub"
    stub.write_text('#!/bin/sh\nif test "$1" = info; then exit 0; fi\nexit 7\n')
    stub.chmod(0o755)
    (tmp_path / "Makefile").write_text(
        f"DOCKER := ./docker-stub\ninclude {ROOT}/template/docker/quality.mk\n"
    )
    result = subprocess.run(
        ["make", "ci-local", "REPORT_DIR=coverage/matrix"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    receipt = json.loads((tmp_path / "coverage/matrix/ci-local.json").read_text())
    assert receipt["status"] == "failed"
    assert receipt["checks"][0]["exitCode"] != 0
    assert not (tmp_path / "coverage/ci-local.json").exists()


def test_explicit_bundle_name_and_ignored_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, release: ModuleType
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "VERSION").write_text("0.2.1\n")
    (tmp_path / "README.md").write_text("# Public bundle\n")
    private = tmp_path / ".aws"
    private.mkdir()
    (private / "credentials").write_text("SYNTHETIC_DO_NOT_PACKAGE\n")
    subprocess.run(
        ["bash", str(ROOT / "template/docker/source_identity.sh")], check=True
    )
    runner = CliRunner()
    result = runner.invoke(release.app, ["version", "--name", "docs-fixture"])
    assert json.loads(result.stdout)["name"] == "docs-fixture"
    assert (
        runner.invoke(release.app, ["bundle-build", "--name", "docs-fixture"]).exit_code
        == 0
    )
    with tarfile.open(tmp_path / "dist/docs-fixture-0.2.1.tar.gz") as archive:
        assert archive.getnames() == ["README.md", "VERSION"]


@pytest.mark.parametrize("scope", ["full", "scoped"])
@pytest.mark.parametrize("complete", [True, False])
def test_receipt_requires_the_complete_ordered_plan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    release: ModuleType,
    scope: str,
    complete: bool,
) -> None:
    monkeypatch.chdir(tmp_path)
    source_file(tmp_path)
    plan_file(tmp_path, ["check", "coverage"], scope)
    runner = CliRunner()
    assert runner.invoke(release.app, ["receipt", "init"]).exit_code == 0
    for name in ["check", "coverage"] if complete else ["check"]:
        assert (
            runner.invoke(
                release.app,
                [
                    "receipt",
                    "record",
                    "--name",
                    name,
                    "--command",
                    "make " + name,
                    "--exit-code",
                    "0",
                ],
            ).exit_code
            == 0
        )
    result = runner.invoke(release.app, ["receipt", "finish", "--status", "passed"])
    assert (result.exit_code == 0) is complete
    receipt = json.loads((tmp_path / "coverage/ci-local.json").read_text())
    assert receipt["scope"] == scope
    assert receipt["plannedChecks"] == ["check", "coverage"]
    assert (receipt["status"] == "passed") is complete
    assert (
        f"scope: **{scope}**" in (tmp_path / "coverage/ci-local-summary.md").read_text()
    )


@pytest.mark.parametrize(
    "name,code", [("coverage", 0), ("unplanned", 0), ("check", -1), ("check", 256)]
)
def test_receipt_refuses_unplanned_order_and_invalid_codes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    release: ModuleType,
    name: str,
    code: int,
) -> None:
    monkeypatch.chdir(tmp_path)
    source_file(tmp_path)
    plan_file(tmp_path, ["check", "coverage"])
    runner = CliRunner()
    assert runner.invoke(release.app, ["receipt", "init"]).exit_code == 0
    assert (
        runner.invoke(
            release.app,
            [
                "receipt",
                "record",
                "--name",
                name,
                "--command",
                "make " + name,
                "--exit-code",
                str(code),
            ],
        ).exit_code
        != 0
    )


@pytest.mark.parametrize(
    "checks", [[], ["check", "check"], ["offline-preflight"], ["bad target"]]
)
def test_receipt_refuses_invalid_plan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    release: ModuleType,
    checks: list[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    source_file(tmp_path)
    plan_file(tmp_path, checks)
    assert CliRunner().invoke(release.app, ["receipt", "init"]).exit_code != 0


def test_receipt_offline_preflight_and_plan_change(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, release: ModuleType
) -> None:
    monkeypatch.chdir(tmp_path)
    source_file(tmp_path)
    plan_file(tmp_path, ["check"])
    runner = CliRunner()
    assert runner.invoke(release.app, ["receipt", "init"]).exit_code == 0
    for name in ["offline-preflight", "check"]:
        assert (
            runner.invoke(
                release.app,
                [
                    "receipt",
                    "record",
                    "--name",
                    name,
                    "--command",
                    "make " + name,
                    "--exit-code",
                    "0",
                ],
            ).exit_code
            == 0
        )
    assert (
        runner.invoke(
            release.app, ["receipt", "finish", "--status", "passed"]
        ).exit_code
        == 0
    )
    assert runner.invoke(release.app, ["receipt", "init"]).exit_code == 0
    plan_file(tmp_path, ["coverage"])
    assert (
        runner.invoke(
            release.app, ["receipt", "finish", "--status", "passed"]
        ).exit_code
        != 0
    )


@pytest.mark.parametrize("override", [False, True])
def test_make_plan_marks_explicit_subsets_scoped(
    tmp_path: Path, override: bool
) -> None:
    docker = tmp_path / "docker"
    docker.mkdir()
    (docker / "source_identity.sh").write_bytes(
        (ROOT / "template/docker/source_identity.sh").read_bytes()
    )
    (tmp_path / "Makefile").write_text(
        f"DOCKER := false\ninclude {ROOT}/template/docker/quality.mk\n"
    )
    command = ["make", "ci-local"]
    if override:
        command.append("CI_LOCAL_TARGETS=check coverage")
    assert subprocess.run(command, cwd=tmp_path, capture_output=True).returncode != 0
    plan = json.loads((tmp_path / "coverage/ci-plan.json").read_text())
    assert plan["scope"] == ("scoped" if override else "full")
    assert plan["checks"] == (
        ["check", "coverage"]
        if override
        else ["check", "coverage", "build", "verify", "release-check"]
    )
