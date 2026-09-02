#!/usr/bin/env python3
"""Dependency-free structural and privacy checks for the Skill package."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "natural-writing-es-profiles"


def main() -> None:
    skill_md = SKILL / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "SKILL.md must start with frontmatter"
    assert re.search(r"(?m)^name: natural-writing-es-profiles$", text)
    assert re.search(r"(?m)^description: .+", text)

    required = [
        "agents/openai.yaml",
        "assets/icon.svg",
        "profiles/profile-template.md",
        "profiles/neutral/academic.md",
        "profiles/neutral/professional-commercial.md",
        "profiles/neutral/personal.md",
        "references/intake.md",
        "references/personalization.md",
        "references/patterns.md",
        "references/eval.md",
        "scripts/profile_manager.py",
    ]
    for relative in required:
        assert (SKILL / relative).is_file(), f"missing {relative}"

    assert not (SKILL / "profiles" / "custom").exists(), "custom profile shipped"
    assert not (SKILL / "profiles" / "selection.json").exists(), "selection shipped"

    private_parts = {"samples", "corpus"}
    source_extensions = {".docx", ".pdf", ".txt", ".rtf", ".odt"}
    for path in SKILL.rglob("*"):
        relative_parts = set(path.relative_to(SKILL).parts)
        assert not private_parts.intersection(relative_parts), f"private corpus path: {path}"
        if path.is_file():
            assert not path.name.endswith(".local.md"), f"local profile shipped: {path}"
            assert path.suffix.lower() not in source_extensions, f"source document shipped: {path}"

    forbidden = ("CAMICON", "CEDECON", "dpcs90-author-profile")
    for path in SKILL.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".py"}:
            continue
        content = path.read_text(encoding="utf-8")
        for term in forbidden:
            assert term not in content, f"private term in {path}: {term}"

    marketplace = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    assert marketplace["metadata"]["version"] == (ROOT / "VERSION").read_text().strip()
    print("Package structure and privacy boundary are valid")


if __name__ == "__main__":
    main()
