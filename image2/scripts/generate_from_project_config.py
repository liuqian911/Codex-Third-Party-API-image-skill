#!/usr/bin/env python3
"""Generate an image using image-gen-env.txt stored in this skill's directory."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


REQUIRED_KEYS = ("base_url", "api_key", "image-model", "out-path")


def read_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"invalid configuration line {line_number}")
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        raise ValueError("missing configuration fields: " + ", ".join(missing))
    return values


def unique_output(path: Path, force: bool) -> Path:
    if force or not path.exists():
        return path
    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-v{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not find an available output filename near {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="high")
    parser.add_argument("--out")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="validate config and print the planned request without calling the API")
    args = parser.parse_args()

    config_path = Path(__file__).resolve().parents[1] / "image-gen-env.txt"
    if not config_path.is_file():
        template_path = config_path.with_name("image-gen-env.example.txt")
        print(
            f"Error: configuration not found: {config_path}. "
            f"Copy {template_path} to {config_path} and fill in: "
            + ", ".join(REQUIRED_KEYS),
            file=sys.stderr,
        )
        return 2

    try:
        config = read_config(config_path)
    except (OSError, ValueError) as exc:
        print(f"Error: {config_path}: {exc}", file=sys.stderr)
        return 2

    output_dir = Path(config["out-path"]).expanduser().absolute()
    requested = Path(args.out).expanduser() if args.out else output_dir / "image2-output.png"
    if not requested.is_absolute():
        requested = output_dir / requested
    output_path = unique_output(requested, args.force)

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    cli_path = codex_home / "skills" / ".system" / "imagegen" / "scripts" / "image_gen.py"
    if not cli_path.is_file():
        print(f"Error: bundled image generation CLI not found: {cli_path}", file=sys.stderr)
        return 2

    env = os.environ.copy()
    env["OPENAI_API_KEY"] = config["api_key"]
    env["OPENAI_BASE_URL"] = config["base_url"]
    command = [
        sys.executable,
        str(cli_path),
        "generate",
        "--model",
        config["image-model"],
        "--prompt",
        args.prompt,
        "--size",
        args.size,
        "--quality",
        args.quality,
        "--out",
        str(output_path),
    ]
    if args.force:
        command.append("--force")
    if args.dry_run:
        print(f"Config: {config_path}")
        print(f"Endpoint: {config['base_url']}")
        print(f"Model: {config['image-model']}")
        print(f"Size: {args.size}")
        print(f"Quality: {args.quality}")
        print(f"Output: {output_path}")
        return 0
    return subprocess.run(command, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
