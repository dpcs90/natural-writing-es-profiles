#!/usr/bin/env python3
"""Validate and manage local profiles for natural-writing-es-profiles."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PROFILES_ROOT = SKILL_ROOT / "profiles"
CUSTOM_ROOT = PROFILES_ROOT / "custom"
SELECTION_PATH = PROFILES_ROOT / "selection.json"

DOMAINS = ("auto", "academic", "professional-commercial", "personal")
CUSTOM_TARGETS = ("base", "academic", "professional-commercial", "personal")
VARIANTS = ("neutral", "custom")
STATUSES = ("candidate", "active")
CONFIDENCE = ("limited", "moderate", "strong")

REQUIRED_HEADINGS = (
    "## Alcance",
    "## Preservar",
    "## Patrones contextuales",
    "## Moderar",
    "## Corregir",
    "## Evitar",
    "## Confianza y evidencia",
    "## Validación",
)


class ProfileError(ValueError):
    pass


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    finally:
        tmp_path.unlink(missing_ok=True)


def _read_selection() -> dict[str, str]:
    default = {"domain": "auto", "variant": "neutral"}
    if not SELECTION_PATH.exists():
        return default
    try:
        value = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileError(f"Invalid selection file: {exc}") from exc
    if value.get("domain") not in DOMAINS or value.get("variant") not in VARIANTS:
        raise ProfileError("Selection contains an unsupported domain or variant")
    return {"domain": value["domain"], "variant": value["variant"]}


def _custom_path(target: str) -> Path:
    return CUSTOM_ROOT / ("base.md" if target == "base" else f"{target}.md")


def _parse_metadata(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "# Custom writing profile":
        raise ProfileError("First line must be '# Custom writing profile'")

    metadata: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped:
            continue
        match = re.fullmatch(r"([a-z_]+):\s*(.+)", stripped)
        if match:
            metadata[match.group(1)] = match.group(2).strip()

    required = {
        "status",
        "target",
        "profile_id",
        "sample_count",
        "genres_observed",
        "confidence",
    }
    missing = sorted(required - metadata.keys())
    if missing:
        raise ProfileError(f"Missing metadata: {', '.join(missing)}")
    return metadata


def validate_profile(path: Path, expected_target: str) -> dict[str, str]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ProfileError(f"Candidate does not exist: {resolved}")
    if _is_within(resolved, SKILL_ROOT):
        raise ProfileError("Candidate must remain outside the Skill until activation")

    text = resolved.read_text(encoding="utf-8")
    metadata = _parse_metadata(text)

    if metadata["status"] not in STATUSES:
        raise ProfileError("status must be candidate or active")
    if metadata["target"] not in CUSTOM_TARGETS:
        raise ProfileError("Unsupported target")
    if metadata["target"] != expected_target:
        raise ProfileError(
            f"Candidate target '{metadata['target']}' does not match '{expected_target}'"
        )
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", metadata["profile_id"]):
        raise ProfileError("profile_id must be 1-64 safe characters")
    try:
        sample_count = int(metadata["sample_count"])
    except ValueError as exc:
        raise ProfileError("sample_count must be an integer") from exc
    if not 3 <= sample_count <= 10:
        raise ProfileError("sample_count must be between 3 and 10")
    if metadata["confidence"] not in CONFIDENCE:
        raise ProfileError("confidence must be limited, moderate or strong")
    if metadata["genres_observed"].lower() in {"replace-me", "unknown", "n/a", "none"}:
        raise ProfileError("genres_observed must describe the actual sample set")

    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        count = text.count(heading)
        if count != 1:
            raise ProfileError(f"Heading must occur exactly once: {heading}")
        positions.append(text.index(heading))
    if positions != sorted(positions):
        raise ProfileError("Required headings are out of order")

    sections = re.split(r"^## .+$", text, flags=re.MULTILINE)[1:]
    if any(not section.strip() for section in sections[: len(REQUIRED_HEADINGS)]):
        raise ProfileError("Required sections may not be empty")
    return metadata


def command_status(_: argparse.Namespace) -> int:
    selection = _read_selection()
    layers = {target: _custom_path(target).exists() for target in CUSTOM_TARGETS}
    effective_variant = selection["variant"]
    note = None
    if effective_variant == "custom" and not layers["base"]:
        effective_variant = "neutral"
        note = "custom base is missing; effective fallback is neutral"
    output = {
        "selection": selection,
        "effective_variant": effective_variant,
        "custom_layers": layers,
    }
    if note:
        output["note"] = note
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def command_select(args: argparse.Namespace) -> int:
    if args.variant == "custom" and not _custom_path("base").exists():
        raise ProfileError("Activate a custom base profile before selecting custom")
    value = {"domain": args.domain, "variant": args.variant}
    _atomic_write(SELECTION_PATH, json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    print(f"Selected {args.domain} + {args.variant}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    metadata = validate_profile(Path(args.path), args.target)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


def command_activate(args: argparse.Namespace) -> int:
    if not args.confirm_activate:
        raise ProfileError("Activation requires --confirm-activate")
    source = Path(args.path).expanduser().resolve()
    metadata = validate_profile(source, args.target)
    if metadata["status"] != "candidate":
        raise ProfileError("Only a candidate profile can be activated")
    if args.target != "base" and not _custom_path("base").exists():
        raise ProfileError("Activate a custom base profile before a domain adjustment")
    text = source.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^status:\s*candidate\s*$", "status: active", text, count=1)
    destination = _custom_path(args.target)
    _atomic_write(destination, text.rstrip() + "\n")
    print(f"Activated {args.target}: {destination}")
    return 0


def command_reset(args: argparse.Namespace) -> int:
    if not args.confirm_reset:
        raise ProfileError("Reset requires --confirm-reset")

    removed: list[str] = []
    if args.target in CUSTOM_TARGETS:
        targets = CUSTOM_TARGETS if args.target == "base" else (args.target,)
        for target in targets:
            path = _custom_path(target)
            if path.exists():
                path.unlink()
                removed.append(str(path.relative_to(SKILL_ROOT)))
        if args.target == "base" and SELECTION_PATH.exists():
            SELECTION_PATH.unlink()
            removed.append(str(SELECTION_PATH.relative_to(SKILL_ROOT)))
    elif args.target == "selection":
        if SELECTION_PATH.exists():
            SELECTION_PATH.unlink()
            removed.append(str(SELECTION_PATH.relative_to(SKILL_ROOT)))
    elif args.target == "all":
        if CUSTOM_ROOT.exists():
            shutil.rmtree(CUSTOM_ROOT)
            removed.append(str(CUSTOM_ROOT.relative_to(SKILL_ROOT)) + "/")
        if SELECTION_PATH.exists():
            SELECTION_PATH.unlink()
            removed.append(str(SELECTION_PATH.relative_to(SKILL_ROOT)))

    print(json.dumps({"reset": args.target, "removed": removed}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Show active selection and layers")
    status_parser.set_defaults(func=command_status)

    select_parser = subparsers.add_parser("select", help="Select domain and variant")
    select_parser.add_argument("domain", choices=DOMAINS)
    select_parser.add_argument("variant", choices=VARIANTS)
    select_parser.set_defaults(func=command_select)

    validate_parser = subparsers.add_parser("validate", help="Validate a candidate")
    validate_parser.add_argument("path")
    validate_parser.add_argument("--target", choices=CUSTOM_TARGETS, required=True)
    validate_parser.set_defaults(func=command_validate)

    activate_parser = subparsers.add_parser("activate", help="Activate a candidate")
    activate_parser.add_argument("path")
    activate_parser.add_argument("--target", choices=CUSTOM_TARGETS, required=True)
    activate_parser.add_argument("--confirm-activate", action="store_true")
    activate_parser.set_defaults(func=command_activate)

    reset_parser = subparsers.add_parser("reset", help="Reset a custom layer or base state")
    reset_parser.add_argument(
        "--target", choices=(*CUSTOM_TARGETS, "selection", "all"), required=True
    )
    reset_parser.add_argument("--confirm-reset", action="store_true")
    reset_parser.set_defaults(func=command_reset)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ProfileError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
