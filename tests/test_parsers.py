import logging
from pathlib import Path

import pytest

from dash_license_scan.parsers import parse, parse_pypi


def test_parse_requirements_txt_lock(tmp_path: Path):
    lockfile = tmp_path / "requirements.txt.lock"
    lockfile.write_text(
        "basedpyright==1.35.0 \\\n"
        "    --hash=sha256:2a7e0bd476623d48499e2b18ff6ed19dc28c51909cf9e1152ad355b5809049ad\n"
        "    # via -r requirements.in\n"
        "iniconfig==2.3.0\n",
        encoding="utf-8",
    )
    deps = parse(lockfile)
    assert deps == [
        "pypi/pypi/-/basedpyright/1.35.0",
        "pypi/pypi/-/iniconfig/2.3.0",
    ]


def test_parse_pypi_extras_and_comments(tmp_path: Path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text(
        "# Header comment\n"
        "-r other_requirements.txt\n"
        "--extra-index-url https://example.com/pypi\n"
        "uv[standard]==0.8.9 \\\n"
        "    --hash=sha256:1111111111111111111111111111111111111111111111111111111111111111 \\\n"
        "    --hash=sha256:2222222222222222222222222222222222222222222222222222222222222222\n"
        "importlib-metadata==8.5.0; python_version < '3.10' # inline comment\n",
        encoding="utf-8",
    )
    deps = parse_pypi(req_file)
    assert deps == [
        "pypi/pypi/-/uv/0.8.9",
        "pypi/pypi/-/importlib-metadata/8.5.0",
    ]


def test_parse_pypi_unsupported_line_warning(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("pytest>=9.0.0\n", encoding="utf-8")
    with caplog.at_level(logging.WARNING):
        deps = parse_pypi(req_file)
    assert deps == []
    assert "Skipping unsupported pip requirement line: pytest>=9.0.0" in caplog.text


def test_parse_generic_lock_file_detection(tmp_path: Path):
    pypi_lock = tmp_path / "custom.lock"
    pypi_lock.write_text("requests==2.32.3\n", encoding="utf-8")
    assert parse(pypi_lock) == ["pypi/pypi/-/requests/2.32.3"]

    cargo_lock = tmp_path / "custom_cargo.lock"
    cargo_lock.write_text(
        '[[package]]\nname = "foo"\nversion = "1.0.0"\nsource = "registry+https://github.com/rust-lang/crates.io-index"\n',
        encoding="utf-8",
    )
    assert parse(cargo_lock) == ["crate/cratesio/-/foo/1.0.0"]
