#!/usr/bin/env python3
"""
生成一份紧凑、基于证据的仓库快照，便于项目上手梳理。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".next",
    ".nuxt",
    ".turbo",
    ".yarn",
    ".pnpm-store",
    ".cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "out",
    "target",
    "tmp",
    "temp",
    "vendor",
    "venv",
    ".venv",
}

MANIFEST_NAMES = [
    "README.md",
    "README",
    "package.json",
    "pnpm-workspace.yaml",
    "turbo.json",
    "nx.json",
    "lerna.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "Cargo.toml",
    "go.mod",
    "Makefile",
    "justfile",
    "Taskfile.yml",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
    "Dockerfile",
]

RUN_SCRIPT_ORDER = ["dev", "start", "serve", "build", "test", "lint"]


def visible_children(path: Path) -> list[Path]:
    items = []
    for child in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        if child.name in IGNORED_DIRS:
            continue
        if child.name.startswith(".") and child.name not in {".env.example", ".env"}:
            continue
        items.append(child)
    return items


def sample_children(path: Path, limit: int = 5) -> tuple[int, list[str]]:
    try:
        children = visible_children(path)
    except OSError:
        return 0, []
    return len(children), [child.name for child in children[:limit]]


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def load_toml(path: Path) -> dict | None:
    if tomllib is None:
        return None
    try:
        return tomllib.loads(path.read_text())
    except Exception:
        return None


def detect_package_manager(root: Path, package_data: dict | None) -> str:
    if package_data:
        raw = package_data.get("packageManager")
        if isinstance(raw, str) and raw:
            return raw.split("@", 1)[0]
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lock").exists() or (root / "bun.lockb").exists():
        return "bun"
    return "npm"


def format_script_command(package_manager: str, script_name: str) -> str:
    if package_manager == "pnpm":
        return f"pnpm {script_name}"
    if package_manager == "yarn":
        return f"yarn {script_name}"
    if package_manager == "bun":
        return f"bun run {script_name}"
    return f"npm run {script_name}"


def parse_make_targets(path: Path) -> list[str]:
    if not path.exists():
        return []
    targets = []
    pattern = re.compile(r"^([A-Za-z0-9_.-]+):(?:\s|$)")
    for line in path.read_text(errors="ignore").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        target = match.group(1)
        if target.startswith("."):
            continue
        if target not in targets:
            targets.append(target)
    return targets[:12]


def summarize_top_level(root: Path) -> tuple[list[str], list[str]]:
    directories = []
    files = []
    prioritized_files = {"README.md", "README", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "Makefile"}

    for child in visible_children(root):
        if child.is_dir():
            count, sample = sample_children(child)
            suffix = f" ({count} items"
            if sample:
                suffix += f"; sample: {', '.join(sample)}"
            suffix += ")"
            directories.append(f"{child.name}/" + suffix)
        else:
            files.append(child.name)

    files.sort(key=lambda name: (name not in prioritized_files, name.lower()))
    return directories[:12], files[:10]


def find_workspace_package_jsons(root: Path) -> list[Path]:
    candidates = []
    for dirname in ("apps", "packages", "services", "libs"):
        base = root / dirname
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir(), key=lambda p: p.name.lower()):
            if child.is_dir() and (child / "package.json").exists():
                candidates.append(child / "package.json")
    return candidates[:12]


def detect_repo_shape(root: Path, manifests: list[str], workspace_packages: list[Path]) -> str:
    if workspace_packages:
        return "monorepo"
    workspace_markers = {"pnpm-workspace.yaml", "turbo.json", "nx.json", "lerna.json"}
    if workspace_markers.intersection(manifests):
        return "monorepo"
    if any((root / name).exists() for name in ("package.json", "pyproject.toml", "Cargo.toml", "go.mod")):
        return "应用或服务仓库"
    if sum(1 for name in ("apps", "packages", "services") if (root / name).exists()) >= 2:
        return "多模块仓库"
    return "源码仓库"


def detect_entrypoints(root: Path) -> list[str]:
    candidates = [
        "src/main.ts",
        "src/main.tsx",
        "src/index.ts",
        "src/index.tsx",
        "src/main.js",
        "src/index.js",
        "main.py",
        "app.py",
        "manage.py",
        "main.go",
        "src/main.rs",
        "server.js",
        "server.ts",
    ]
    found = []
    for rel in candidates:
        if (root / rel).exists():
            found.append(rel)
    return found


def build_snapshot(root: Path) -> dict:
    manifests = [name for name in MANIFEST_NAMES if (root / name).exists()]
    workspace_packages = find_workspace_package_jsons(root)
    top_level_dirs, top_level_files = summarize_top_level(root)
    package_path = root / "package.json"
    package_data = load_json(package_path) if package_path.exists() else None
    package_manager = detect_package_manager(root, package_data)
    pyproject_data = load_toml(root / "pyproject.toml") if (root / "pyproject.toml").exists() else None
    cargo_data = load_toml(root / "Cargo.toml") if (root / "Cargo.toml").exists() else None

    run_commands = []
    if package_data and isinstance(package_data.get("scripts"), dict):
        for script_name in RUN_SCRIPT_ORDER:
            if script_name in package_data["scripts"]:
                run_commands.append(
                    {
                        "command": format_script_command(package_manager, script_name),
                        "source": "package.json",
                        "explicit": True,
                    }
                )
    make_targets = parse_make_targets(root / "Makefile")
    for target in ("install", "dev", "start", "build", "test"):
        if target in make_targets:
            run_commands.append(
                {
                    "command": f"make {target}",
                    "source": "Makefile",
                    "explicit": True,
                }
            )
    if (root / "docker-compose.yml").exists() or (root / "docker-compose.yaml").exists() or (root / "compose.yml").exists() or (root / "compose.yaml").exists():
        run_commands.append(
            {
                "command": "docker compose up",
                "source": "compose file",
                "explicit": False,
            }
        )
    if (root / "manage.py").exists():
        run_commands.append(
            {
                "command": "python manage.py runserver",
                "source": "manage.py",
                "explicit": False,
            }
        )
    if cargo_data:
        run_commands.append(
            {
                "command": "cargo run",
                "source": "Cargo.toml",
                "explicit": False,
            }
        )
    if (root / "go.mod").exists():
        run_commands.append(
            {
                "command": "go run .",
                "source": "go.mod",
                "explicit": False,
            }
        )

    pyproject_scripts = []
    if isinstance(pyproject_data, dict):
        project_block = pyproject_data.get("project")
        if isinstance(project_block, dict):
            scripts = project_block.get("scripts")
            if isinstance(scripts, dict):
                pyproject_scripts = sorted(scripts.keys())[:10]

    workspace_details = []
    for pkg_json in workspace_packages:
        data = load_json(pkg_json)
        if not data:
            continue
        scripts = sorted((data.get("scripts") or {}).keys())[:6]
        workspace_details.append(
            {
                "path": str(pkg_json.relative_to(root)),
                "name": data.get("name"),
                "scripts": scripts,
            }
        )

    return {
        "target": str(root),
        "repo_shape": detect_repo_shape(root, manifests, workspace_packages),
        "top_level_dirs": top_level_dirs,
        "top_level_files": top_level_files,
        "manifests": manifests,
        "entrypoints": detect_entrypoints(root),
        "run_commands": run_commands[:10],
        "workspace_packages": workspace_details,
        "package_name": package_data.get("name") if package_data else None,
        "package_manager": package_manager if package_data else None,
        "package_scripts": sorted((package_data.get("scripts") or {}).keys())[:12] if package_data else [],
        "pyproject_scripts": pyproject_scripts,
        "cargo_package": (
            cargo_data.get("package", {}).get("name")
            if isinstance(cargo_data, dict) and isinstance(cargo_data.get("package"), dict)
            else None
        ),
        "make_targets": make_targets,
        "recommended_reads": [
            name
            for name in [
                "README.md",
                "README",
                "package.json",
                "pyproject.toml",
                "Cargo.toml",
                "go.mod",
                "Makefile",
                "docker-compose.yml",
                "compose.yaml",
            ]
            if (root / name).exists()
        ]
        + [item["path"] for item in workspace_details[:5]],
    }


def print_text(snapshot: dict) -> None:
    print(f"目标路径: {snapshot['target']}")
    print(f"仓库类型: {snapshot['repo_shape']}")
    print()

    if snapshot["manifests"]:
        print("识别到的清单文件:")
        for name in snapshot["manifests"]:
            print(f"- {name}")
        print()

    print("顶层目录:")
    for item in snapshot["top_level_dirs"]:
        print(f"- {item}")
    print()

    if snapshot["top_level_files"]:
        print("顶层文件:")
        for item in snapshot["top_level_files"]:
            print(f"- {item}")
    print()

    if snapshot["package_name"] or snapshot["package_scripts"]:
        print("Node 包信息:")
        if snapshot["package_name"]:
            print(f"- 名称: {snapshot['package_name']}")
        if snapshot["package_manager"]:
            print(f"- 包管理器: {snapshot['package_manager']}")
        if snapshot["package_scripts"]:
            print(f"- scripts: {', '.join(snapshot['package_scripts'])}")
        print()

    if snapshot["workspace_packages"]:
        print("Workspace 包:")
        for pkg in snapshot["workspace_packages"]:
            label = pkg["path"]
            if pkg["name"]:
                label += f" ({pkg['name']})"
            if pkg["scripts"]:
                label += f" -> scripts: {', '.join(pkg['scripts'])}"
            print(f"- {label}")
        print()

    if snapshot["pyproject_scripts"]:
        print("Python 入口脚本:")
        for script in snapshot["pyproject_scripts"]:
            print(f"- {script}")
        print()

    if snapshot["make_targets"]:
        print("Make 目标:")
        print(f"- {', '.join(snapshot['make_targets'])}")
        print()

    if snapshot["entrypoints"]:
        print("可能的入口文件:")
        for entry in snapshot["entrypoints"]:
            print(f"- {entry}")
        print()

    if snapshot["run_commands"]:
        print("候选运行命令:")
        for item in snapshot["run_commands"]:
            note = "显式声明" if item["explicit"] else "推断"
            print(f"- {item['command']} ({note}；来源: {item['source']})")
        print()

    if snapshot["recommended_reads"]:
        print("建议接下来阅读:")
        for item in snapshot["recommended_reads"]:
            print(f"- {item}")


def main() -> None:
    parser = argparse.ArgumentParser(description="输出便于项目上手的仓库结构摘要。")
    parser.add_argument("target", nargs="?", default=".", help="仓库路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON，而不是文本")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    if not root.exists():
        raise SystemExit(f"路径不存在: {root}")
    if not root.is_dir():
        raise SystemExit(f"路径不是目录: {root}")

    snapshot = build_snapshot(root)
    if args.json:
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    else:
        print_text(snapshot)


if __name__ == "__main__":
    main()
