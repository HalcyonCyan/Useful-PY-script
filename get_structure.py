import os
import argparse
from pathlib import Path

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "__pycache__",
    ".next",
    ".cache",
    "coverage",
}

IGNORE_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
}

TEXT_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".md": "markdown",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".xml": "xml",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".sh": "bash",
    ".bat": "bat",
    ".env": "bash",
    ".txt": "text",
}


def is_binary_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
        return b"\0" in chunk
    except Exception:
        return True


def should_ignore(path: Path, root: Path, max_size: int) -> bool:
    relative_parts = path.relative_to(root).parts

    for part in relative_parts:
        if part in IGNORE_DIRS:
            return True

    if path.name in IGNORE_FILES:
        return True

    if path.is_file():
        if path.stat().st_size > max_size:
            return True

        if is_binary_file(path):
            return True

    return False


def get_language(path: Path) -> str:
    if path.name.startswith(".env"):
        return "bash"
    return TEXT_EXTENSIONS.get(path.suffix.lower(), "text")


def build_tree(root: Path, max_size: int) -> str:
    lines = [f"{root.name}/"]

    def walk(directory: Path, prefix: str = ""):
        items = []

        for item in sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            if should_ignore(item, root, max_size):
                continue
            items.append(item)

        for index, item in enumerate(items):
            connector = "└─ " if index == len(items) - 1 else "├─ "
            lines.append(prefix + connector + item.name)

            if item.is_dir():
                extension = "   " if index == len(items) - 1 else "│  "
                walk(item, prefix + extension)

    walk(root)
    return "\n".join(lines)


def collect_files(root: Path, max_size: int):
    files = []

    for path in root.rglob("*"):
        if path.is_file() and not should_ignore(path, root, max_size):
            files.append(path)

    return sorted(files, key=lambda p: str(p.relative_to(root)).lower())


def generate_markdown(root: Path, output: Path, max_size: int):
    tree = build_tree(root, max_size)
    files = collect_files(root, max_size)

    with open(output, "w", encoding="utf-8") as md:
        md.write(f"# Repository Snapshot: `{root.name}`\n\n")

        md.write("## Directory Tree\n\n")
        md.write("```text\n")
        md.write(tree)
        md.write("\n```\n\n")

        md.write("## File Contents\n\n")

        for file_path in files:
            relative_path = file_path.relative_to(root)
            language = get_language(file_path)

            md.write(f"### `{relative_path}`\n\n")
            md.write(f"```{language}\n")

            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                try:
                    content = file_path.read_text(encoding="gbk")
                except Exception:
                    content = "[无法读取该文件内容]"
            except Exception as e:
                content = f"[读取失败: {e}]"

            md.write(content)
            if not content.endswith("\n"):
                md.write("\n")

            md.write("```\n\n")

    print(f"已生成 Markdown 文件: {output}")


def main():
    parser = argparse.ArgumentParser(description="Read a repository and export its content as Markdown.")
    parser.add_argument("repo", help="仓库路径")
    parser.add_argument("-o", "--output", default="repo_snapshot.md", help="输出 Markdown 文件名")
    parser.add_argument("--max-size", type=int, default=200 * 1024, help="单个文件最大读取大小，默认 200KB")

    args = parser.parse_args()

    root = Path(args.repo).resolve()
    output = Path(args.output).resolve()

    if not root.exists():
        print("错误：仓库路径不存在")
        return

    if not root.is_dir():
        print("错误：输入路径不是文件夹")
        return

    generate_markdown(root, output, args.max_size)


if __name__ == "__main__":
    main()