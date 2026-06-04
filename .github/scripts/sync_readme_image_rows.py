#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def replace_table_value(markdown: str, key: str, value: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"^(\|\s*`{re.escape(key)}`\s*\|.*\|\s*)`[^`]*`(\s*\|)\s*$",
        re.MULTILINE,
    )
    return pattern.subn(rf"\1`{value}`\2", markdown)


def load_values(values_file: Path) -> dict[str, str]:
    required = {
        "stunnerGatewayOperator.deployment.container.manager.image.name",
        "stunnerGatewayOperator.deployment.container.manager.image.tag",
        "stunnerGatewayOperator.dataplane.spec.image.name",
        "stunnerGatewayOperator.dataplane.spec.image.tag",
        "stunnerAuthService.deployment.container.authService.image.name",
        "stunnerAuthService.deployment.container.authService.image.tag",
    }

    parsed: dict[str, str] = {}
    stack: list[tuple[int, str]] = []

    for raw_line in values_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        match = re.match(r"^(\s*)([A-Za-z0-9_]+):(?:\s*(.*))?$", line)
        if not match:
            continue

        indent = len(match.group(1))
        key = match.group(2)
        value = match.group(3) or ""

        while stack and indent <= stack[-1][0]:
            stack.pop()

        current_path = ".".join([part for _, part in stack] + [key])

        if value == "":
            stack.append((indent, key))
            continue

        if value.startswith("#"):
            stack.append((indent, key))
            continue

        clean = value.split(" #", 1)[0].strip()
        if len(clean) >= 2 and clean[0] == clean[-1] and clean[0] in {'"', "'"}:
            clean = clean[1:-1]

        parsed[current_path] = clean

    missing = sorted(required - parsed.keys())
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"Missing required values.yaml paths: {joined}")

    return {k: parsed[k] for k in required}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync image name and tag rows in chart README."
    )
    parser.add_argument("--readme", required=True)
    parser.add_argument("--values", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    readme_path = Path(args.readme)
    original = readme_path.read_text(encoding="utf-8")
    content = original
    values = load_values(Path(args.values))

    updates = {
        "stunnerGatewayOperator.deployment.container.manager.image.name": values[
            "stunnerGatewayOperator.deployment.container.manager.image.name"
        ],
        "stunnerGatewayOperator.deployment.container.manager.image.tag": values[
            "stunnerGatewayOperator.deployment.container.manager.image.tag"
        ],
        "stunnerGatewayOperator.dataplane.spec.image.name": values[
            "stunnerGatewayOperator.dataplane.spec.image.name"
        ],
        "stunnerGatewayOperator.dataplane.spec.image.tag": values[
            "stunnerGatewayOperator.dataplane.spec.image.tag"
        ],
        "stunnerAuthService.deployment.container.authService.image.name": values[
            "stunnerAuthService.deployment.container.authService.image.name"
        ],
        "stunnerAuthService.deployment.container.authService.image.tag": values[
            "stunnerAuthService.deployment.container.authService.image.tag"
        ],
    }

    for key, value in updates.items():
        content, count = replace_table_value(content, key, value)
        if count != 1:
            raise RuntimeError(
                f"Expected exactly 1 README row for '{key}', found {count}"
            )

    if args.check:
        if content != original:
            raise RuntimeError(
                "README image rows are out of sync with values.yaml. "
                "Run sync_readme_image_rows.py without --check to update."
            )
        return 0

    if content != original:
        readme_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
