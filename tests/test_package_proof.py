"""Run the rendered package proof in real isolated wheel/editable environments."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from jinja2 import Environment, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class InstalledProject:
    source: Path
    wheel: Path
    python: Path
    env: dict[str, str] = field(repr=False)
    version: str


def run(command: list[str], cwd: Path, env: dict[str, str]) -> str:
    result = subprocess.run(
        command, cwd=cwd, env=env, capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


@pytest.fixture(scope="module", params=["0.4.0.dev2", "0.4.0"])
def installed_project(
    tmp_path_factory: pytest.TempPathFactory, request: pytest.FixtureRequest
) -> InstalledProject:
    root = tmp_path_factory.mktemp("package-proof")
    source = root / "source"
    source.mkdir()
    (source / "pyproject.toml").write_text(
        f'[build-system]\nrequires=["hatchling=={importlib.metadata.version("hatchling")}"]\n'
        'build-backend="hatchling.build"\n'
        f'[project]\nname="proof-fixture"\nversion="{request.param}"\nrequires-python=">=3.12"\n'
        '[tool.hatch.build.targets.wheel]\npackages=["src/proof_fixture"]\n'
    )
    package = source / "src/proof_fixture"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text('"""Installed proof fixture."""\n')
    env = dict(os.environ)
    for key in (
        "TEST_INSTALLED_WHEEL",
        "TEST_EXACT_WHEEL",
        "EXPECTED_WHEEL_PATH",
        "EXPECTED_WHEEL_SHA256",
        "PYTHONPATH",
    ):
        env.pop(key, None)
    env.setdefault("UV_CACHE_DIR", str(root / "uv-cache"))
    dist = root / "distribution with spaces"
    run(
        [
            "uv",
            "build",
            "--offline",
            "--no-build-isolation",
            "--python",
            sys.executable,
            "--wheel",
            "--no-create-gitignore",
            "--out-dir",
            str(dist),
            str(source),
        ],
        root,
        env,
    )
    wheel = next(dist.glob("*.whl"))
    venv = root / "installed"
    run(["uv", "venv", "--offline", "--python", sys.executable, str(venv)], root, env)
    python = venv / "bin/python"
    run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            "--no-deps",
            str(wheel),
            f"packaging=={importlib.metadata.version('packaging')}",
        ],
        root,
        env,
    )
    return InstalledProject(source, wheel, python, env, str(request.param))


def proof(
    tmp_path: Path,
    installed: InstalledProject,
    flags: dict[str, str],
    version: str | None = None,
    python: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    acceptance = tmp_path / "acceptance"
    test = acceptance / "tests/foundation/test_package.py"
    test.parent.mkdir(parents=True, exist_ok=True)
    (acceptance / "pyproject.toml").write_text(
        f'[project]\nname="proof-fixture"\nversion="{version or installed.version}"\n'
    )
    test.write_text(
        Environment(undefined=StrictUndefined, keep_trailing_newline=True)
        .from_string(
            (ROOT / "template/tests/foundation/test_package.py.jinja").read_text()
        )
        .render(packageName="proof_fixture")
    )
    return subprocess.run(
        [
            str(python or installed.python),
            "-I",
            "-B",
            "-c",
            "import runpy,sys;runpy.run_path(sys.argv[1])"
            "['test_installed_distribution_and_public_import']()",
            str(test),
        ],
        cwd=tmp_path,
        env=installed.env | flags,
        capture_output=True,
        text=True,
        timeout=30,
    )


def exact_flags(installed: InstalledProject) -> dict[str, str]:
    return {
        "TEST_INSTALLED_WHEEL": "1",
        "TEST_EXACT_WHEEL": "1",
        "EXPECTED_WHEEL_PATH": str(installed.wheel),
        "EXPECTED_WHEEL_SHA256": hashlib.sha256(
            installed.wheel.read_bytes()
        ).hexdigest(),
    }


@pytest.mark.parametrize("flags", [{}, {"TEST_INSTALLED_WHEEL": "1"}])
def test_legacy_mode_needs_no_new_inputs(
    tmp_path: Path, installed_project: InstalledProject, flags: dict[str, str]
) -> None:
    result = proof(tmp_path, installed_project, flags)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("flags", [{}, {"TEST_INSTALLED_WHEEL": "1"}])
def test_wrong_native_version_is_rejected(
    tmp_path: Path, installed_project: InstalledProject, flags: dict[str, str]
) -> None:
    result = proof(tmp_path, installed_project, flags, version="0.4.1")
    assert result.returncode != 0


def test_exact_wheel_native_origin(
    tmp_path: Path, installed_project: InstalledProject
) -> None:
    result = proof(tmp_path, installed_project, exact_flags(installed_project))
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "missing", ["TEST_INSTALLED_WHEEL", "EXPECTED_WHEEL_PATH", "EXPECTED_WHEEL_SHA256"]
)
def test_exact_mode_requires_all_inputs(
    tmp_path: Path, installed_project: InstalledProject, missing: str
) -> None:
    flags = exact_flags(installed_project)
    del flags[missing]
    assert proof(tmp_path, installed_project, flags).returncode != 0


@pytest.mark.parametrize("checksum", ["0" * 64, "invalid", ""])
def test_exact_mode_rejects_wrong_or_malformed_hash(
    tmp_path: Path, installed_project: InstalledProject, checksum: str
) -> None:
    flags = exact_flags(installed_project) | {"EXPECTED_WHEEL_SHA256": checksum}
    assert proof(tmp_path, installed_project, flags).returncode != 0


def test_exact_mode_rejects_same_bytes_from_another_path(
    tmp_path: Path, installed_project: InstalledProject
) -> None:
    other = tmp_path / installed_project.wheel.name
    other.write_bytes(installed_project.wheel.read_bytes())
    flags = exact_flags(installed_project) | {"EXPECTED_WHEEL_PATH": str(other)}
    assert proof(tmp_path, installed_project, flags).returncode != 0


@pytest.fixture
def direct_url(installed_project: InstalledProject) -> Iterator[Path]:
    filename = run(
        [
            str(installed_project.python),
            "-I",
            "-c",
            "from importlib.metadata import distribution;"
            "d=distribution('proof-fixture');print(next(d.locate_file(f)"
            " for f in d.files if f.name=='direct_url.json'))",
        ],
        installed_project.source.parent,
        installed_project.env,
    )
    path = Path(filename)
    original = path.read_bytes()
    try:
        yield path
    finally:
        path.write_bytes(original)


def test_exact_mode_accepts_uv_metadata_without_optional_archive_hash(
    tmp_path: Path, installed_project: InstalledProject, direct_url: Path
) -> None:
    data = json.loads(direct_url.read_text())
    data["archive_info"] = {}
    direct_url.write_text(json.dumps(data))
    result = proof(tmp_path, installed_project, exact_flags(installed_project))
    assert result.returncode == 0, result.stderr


def test_exact_mode_rejects_conflicting_optional_archive_hash(
    tmp_path: Path, installed_project: InstalledProject, direct_url: Path
) -> None:
    data = json.loads(direct_url.read_text())
    data["archive_info"] = {"hashes": {"sha256": "0" * 64}}
    direct_url.write_text(json.dumps(data))
    assert (
        proof(tmp_path, installed_project, exact_flags(installed_project)).returncode
        != 0
    )


@pytest.mark.parametrize(
    "archive", [{"hash": "sha256:bad"}, {"hashes": {"sha512": "0" * 128}}]
)
def test_exact_mode_rejects_malformed_or_unsupported_archive_hash(
    tmp_path: Path,
    installed_project: InstalledProject,
    direct_url: Path,
    archive: dict[str, object],
) -> None:
    data = json.loads(direct_url.read_text())
    data["archive_info"] = archive
    direct_url.write_text(json.dumps(data))
    assert (
        proof(tmp_path, installed_project, exact_flags(installed_project)).returncode
        != 0
    )


@pytest.mark.parametrize("exact", [False, True])
def test_missing_pep610_is_compatible_only_with_legacy_mode(
    tmp_path: Path, installed_project: InstalledProject, direct_url: Path, exact: bool
) -> None:
    direct_url.unlink()
    flags = exact_flags(installed_project) if exact else {"TEST_INSTALLED_WHEEL": "1"}
    result = proof(tmp_path, installed_project, flags)
    assert (result.returncode == 0) is (not exact)


@pytest.fixture(scope="module")
def editable_python(installed_project: InstalledProject) -> Path:
    root = installed_project.source.parent
    venv = root / "editable"
    run(
        ["uv", "venv", "--offline", "--python", sys.executable, str(venv)],
        root,
        installed_project.env,
    )
    python = venv / "bin/python"
    run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            "--editable",
            str(installed_project.source),
            f"packaging=={importlib.metadata.version('packaging')}",
        ],
        root,
        installed_project.env,
    )
    return python


@pytest.mark.parametrize("exact", [False, True])
def test_native_editable_install_is_rejected_in_installed_mode(
    tmp_path: Path,
    installed_project: InstalledProject,
    editable_python: Path,
    exact: bool,
) -> None:
    flags = exact_flags(installed_project) if exact else {"TEST_INSTALLED_WHEEL": "1"}
    assert (
        proof(tmp_path, installed_project, flags, python=editable_python).returncode
        != 0
    )
