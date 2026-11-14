"""Generate a bounded, textual directory tree."""

from pathlib import Path


def generate_file_tree(path: str, indent: str = "~", *, max_depth: int = 5, max_entries: int = 300) -> str:
    """Return a file tree instead of printing to the server console."""
    root = Path(path)
    if not root.is_dir():
        raise NotADirectoryError(path)
    lines: list[str] = []
    count = 0

    def visit(directory: Path, prefix: str, depth: int) -> None:
        nonlocal count
        if depth > max_depth or count >= max_entries:
            return
        for child in sorted(directory.iterdir(), key=lambda p: p.name.casefold()):
            if count >= max_entries:
                lines.append(prefix + "... (entry limit reached)")
                return
            lines.append(prefix + "├── " + child.name)
            count += 1
            if child.is_dir() and not child.is_symlink() and depth < max_depth:
                visit(child, prefix + "│   ", depth + 1)

    visit(root, indent, 0)
    return "\n".join(lines)
