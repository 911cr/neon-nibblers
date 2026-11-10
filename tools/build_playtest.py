"""Package the playable game and optional turn drill using repository files."""
import ast
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "dist/NeonNibblers-keyboard-playtest-5.zip"


def sources():
    files = set()
    pending = ["game", "turn_drill"]
    while pending:
        path = ROOT / (pending.pop() + ".py")
        if path in files:
            continue
        files.add(path)
        for node in ast.walk(ast.parse(path.read_bytes())):
            if isinstance(node, ast.ImportFrom):
                modules = [node.module]
            elif isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            else:
                continue
            pending.extend(m for m in modules if m and (ROOT / (m + ".py")).is_file())
    files.update(ROOT / name for name in (
        "maps.json", "tuning.keyboard-playtest.json", "run_windows.bat",
        "run_linux.sh", "playtest_windows.bat", "playtest_linux.sh",
        "requirements.txt", "START HERE.txt"))
    return files


if __name__ == "__main__":
    ARCHIVE.parent.mkdir(exist_ok=True)
    with ZipFile(ARCHIVE, "w") as bundle:
        for path in sorted(sources()):
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes().replace(b"\r\n", b"\n")
            if path.suffix == ".bat":
                data = data.replace(b"\n", b"\r\n")
            bundle.writestr(ZipInfo("NeonNibblers/" + name), data, ZIP_DEFLATED)
        # Always ship an empty, two-person preset even after a local playtest.
        bundle.writestr(ZipInfo("NeonNibblers/duel-data/cabinet.json"),
                        b'{"settings":{"fill_bots":false,"free_play":true,"match_seconds":180,"starting_lives":3}}\n',
                        ZIP_DEFLATED)
    print(ARCHIVE)
