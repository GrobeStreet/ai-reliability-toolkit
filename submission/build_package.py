"""Validate selected text resources and emit staging JSON; never upload."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


def build(root):
    manifest = json.loads((root / "submission/package-manifest.json").read_text())
    plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
    if manifest["package_version"] != plugin["version"]:
        raise ValueError("manifest and plugin versions must match")
    files, destinations = [], set()
    for entry in manifest["files"]:
        source, destination = entry["source"], entry["path"]
        for name in (source, destination):
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name:
                raise ValueError("package paths must be safe relative POSIX paths")
        if destination in destinations:
            raise ValueError("duplicate package destination")
        destinations.add(destination)
        path = (root / source).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("package source escapes repository")
        data = path.read_bytes()
        text = data.decode("utf-8")
        if "\x00" in text:
            raise ValueError("binary data in text package")
        files.append({"path": destination, "content": text,
                      "sha256": hashlib.sha256(data).hexdigest()})
    skill = next(f["content"] for f in files if f["path"] == "SKILL.md")
    if not skill.startswith("---\n"):
        raise ValueError("missing skill frontmatter")
    header = skill.split("---\n", 2)[1]
    if not re.search(r"^name: ai-reliability-audit$", header, re.M):
        raise ValueError("unexpected skill name")
    if not re.search(r"^description: .+", header, re.M):
        raise ValueError("missing skill description")
    for file in files:
        parent = PurePosixPath(file["path"]).parent
        for target in re.findall(r"\]\(([^)]+)\)", file["content"]):
            if "://" in target or target.startswith("#"):
                continue
            if str(parent / target.split("#", 1)[0]) not in destinations:
                raise ValueError(f"unbundled reference: {file['path']}: {target}")
    if len(files) > 100 or sum(len(f["content"].encode()) for f in files) > 5_000_000:
        raise ValueError("exceeds documented agent upload limits")
    return {"format": "text-file-staging-v1", "not_an_api_request": True,
            "version": manifest["package_version"], "files": files}


if __name__ == "__main__":
    # Standard output allows the caller to choose where to save the generated
    # payload. No network, credentials, installation, or archive creation.
    json.dump(build(Path(__file__).resolve().parents[1]), sys.stdout,
              ensure_ascii=False, indent=2)
    print()
