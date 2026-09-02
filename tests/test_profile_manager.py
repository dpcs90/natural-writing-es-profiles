#!/usr/bin/env python3
"""Exercise selection, layered activation and reversible reset."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "natural-writing-es-profiles"
SCRIPT = SKILL / "scripts" / "profile_manager.py"
CUSTOM = SKILL / "profiles" / "custom"
SELECTION = SKILL / "profiles" / "selection.json"

TEMPLATE = """# Custom writing profile

status: candidate
target: {target}
profile_id: ci-{target}
sample_count: {count}
genres_observed: email, report, personal message
confidence: moderate

## Alcance
Validated only in observed contexts.

## Preservar
Explicit reasoning and qualified conclusions.

## Patrones contextuales
Functional recurring markers with natural frequency.

## Moderar
Repeated framing when too close.

## Corregir
Always correct objective language errors.

## Evitar
Do not caricature the author.

## Confianza y evidencia
Observed across independent samples.

## Validación
Pending user confirmation.
"""


def run(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["python", str(SCRIPT), *args], text=True, capture_output=True, check=False
    )
    assert result.returncode == expected, result.stdout + result.stderr
    return result


def clean() -> None:
    run("reset", "--target", "all", "--confirm-reset")


def main() -> None:
    clean()
    try:
        run("select", "academic", "custom", expected=2)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "base.md"
            academic = Path(directory) / "academic.md"
            base.write_text(TEMPLATE.format(target="base", count=5), encoding="utf-8")
            academic.write_text(
                TEMPLATE.format(target="academic", count=3), encoding="utf-8"
            )

            run(
                "activate",
                str(academic),
                "--target",
                "academic",
                "--confirm-activate",
                expected=2,
            )
            run("validate", str(base), "--target", "base")
            run("activate", str(base), "--target", "base", expected=2)
            run("activate", str(base), "--target", "base", "--confirm-activate")
            run("select", "academic", "custom")
            run(
                "activate",
                str(academic),
                "--target",
                "academic",
                "--confirm-activate",
            )
            assert (CUSTOM / "base.md").is_file()
            assert (CUSTOM / "academic.md").is_file()
            assert SELECTION.is_file()

            run("reset", "--target", "academic", "--confirm-reset")
            assert (CUSTOM / "base.md").is_file()
            assert not (CUSTOM / "academic.md").exists()

            run("reset", "--target", "selection", "--confirm-reset")
            assert (CUSTOM / "base.md").is_file()
            assert not SELECTION.exists()

            run("select", "personal", "custom")
            run("reset", "--target", "base", "--confirm-reset")
            assert not (CUSTOM / "base.md").exists()
            assert not SELECTION.exists()
    finally:
        clean()
    print("Profile lifecycle and reset behavior are valid")


if __name__ == "__main__":
    main()
