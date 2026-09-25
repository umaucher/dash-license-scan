# dash-license-scan

[![PyPI](https://img.shields.io/pypi/v/dash-license-scan.svg)](https://pypi.org/project/dash-license-scan/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

A thin Python CLI wrapper for [eclipse-dash/dash-licenses](https://github.com/eclipse-dash/dash-licenses).
It makes the official JAR easier to use via modern Python workflows (`pipx`, `uvx`) and adds helpers for lockfile conversion.

---

## State

Proof of Concept. Do not use in production environments.

---

## Features

- **Simple to use**: Focus on usability
- **Easy installation**: Run with [`pipx`](https://pypa.github.io/pipx/) or [`uvx`](https://docs.astral.sh/uv/concepts/tools/) - no complex setup required
- **Self-contained**: Self-contained tool with `dash-licenses` JAR included and zero Python dependencies for simplified version management.
- **Lockfile support**: Supports scanning common lockfile and dependency formats:
  - **Python**: `requirements.txt.lock`, `requirements.txt`, `*.txt.lock`, `*.pip.lock`, `*.in`
  - **Rust**: `Cargo.lock`

### Expected Input: Direct Dependencies vs. Lockfiles

For accurate and complete license compliance / SBOM generation:
- **Lockfiles (`requirements.txt.lock`, `Cargo.lock`) are strongly recommended**:
  They contain the complete, resolved dependency tree (both direct and transitive dependencies) with exact version pins (and hashes). License obligations and copyleft clauses apply to transitive dependencies just as much as direct ones.
- **Declarative requirement files (`requirements.txt`, `requirements.in`)**:
  These often list only first-level (direct) dependencies, and may contain unpinned or range-based constraints (e.g. `psutil`, `pytest>=9.0.0`). The Eclipse DASH tool requires exact versions (`name==version`) to query license metadata; unpinned entries cannot be resolved and will be skipped.

### Planned Features

- Auto-detect lockfiles in current directory
- Support more lock file formats, e.g. `uv.lock` and `bazel mod graph`.
- Detect GitHub pull request invocation and print diff
- Compare against additional license limitations (e.g., allowed licenses list)
- Auto-detect Eclipse project environment configuration
- Trigger Eclipse IP-Team review for unknown dependencies

---

## Installation

**System Requirements:**
- `uvx` or `pipx` installed
- Java >= 11 (e.g., `openjdk-21-jre-headless`)

That's it!

## Usage

The tool automatically detects the lockfile type based on filename and extension:

```bash
# Scan a Python pip-compile lockfile (recommended for complete dependency resolution)
uvx dash-license-scan requirements.txt.lock

# Scan a standard Python requirements file
uvx dash-license-scan requirements.txt

# Scan a Rust Cargo lockfile
uvx dash-license-scan Cargo.lock

# Scan multiple lockfiles at once
uvx dash-license-scan requirements.txt.lock Cargo.lock

# Save license summary to a CSV file (useful for CI / automated SBOM workflows)
uvx dash-license-scan --summary summary.csv requirements.txt.lock

# Dry-run to see detected dependencies without invoking the Java dash-licenses tool
uvx dash-license-scan --dry-run requirements.txt.lock

# Verbose logging (debug mode)
uvx dash-license-scan -v requirements.txt.lock
```


---

## Why a Python wrapper?

Why not extend the Java code directly? Here are the reasons:

- **Simplicity**: One-line usability with `uvx`/`pipx`
- **Ecosystem fit**: Most projects already use pip/uv for Python dependencies, making versioning and offline installs seamless
- **Modern tooling**: Leverages modern Python packaging and execution workflows

This tool may not be for everyone, but if it helps S-CORE, it might help you too.

## License

This wrapper is licensed under Apache-2.0 (unlike dash-licenses which uses EPL) to align with S-CORE's licensing standards. Licensing under EPL can certainly be discussed if there is interest. Note that this might become significantly more complex once there is more authors etc!!
