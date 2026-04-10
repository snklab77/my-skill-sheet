#!/usr/bin/env python3
"""
トラック済み skill_sheet_*_SN.md の版・最終更新・ファイル名を揃え、
docs/_data/skill_sheet.yml と skill_sheet.env を更新する。

参照ページはこれらを読む（リポジトリ全体を文字列置換しない）。
コミット前に手動で実行し、差分を確認してから git add / commit することを想定する。
標準ライブラリのみ。
"""
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

SHEET_RE = re.compile(r"skill_sheet_.*_SN\.md$")

# - 最終更新：YYYY-MM-DD #N（同日に何度も更新したとき N で区別）
_FINAL_UPDATE_LINE = re.compile(
    r"^- 最終更新(?:日)?：.+$",
    re.MULTILINE,
)


def _parse_date_and_rev(rest: str) -> tuple[str, int]:
    """行の右辺から日付と #番号を取り出す。番号なしや旧形式（時刻のみ）は番号 0 とみなす。"""
    rest = rest.strip()
    m = re.match(r"^(\d{4}-\d{2}-\d{2})\s*#\s*(\d+)$", rest)
    if m:
        return m.group(1), int(m.group(2))
    m = re.match(r"^(\d{4}-\d{2}-\d{2})(?:\s+\d{2}:\d{2}(:\d{2})?)?\s*$", rest)
    if m:
        return m.group(1), 0
    return datetime.now().strftime("%Y-%m-%d"), 0


def _bump_final_update_line(text: str, today: str) -> str:
    def repl(match) -> str:
        line = match.group(0)
        sep = "："
        if sep not in line:
            return line
        rest = line.split(sep, 1)[1]
        d, n = _parse_date_and_rev(rest)
        if d == today:
            new_n = n + 1
        else:
            new_n = 1
        return f"- 最終更新：{today} #{new_n}"

    return _FINAL_UPDATE_LINE.sub(repl, text, count=1)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _git_root() -> Optional[Path]:
    p = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if p.returncode != 0:
        return None
    return Path(p.stdout.strip())


def _tracked_skill_sheet_paths(root: Path) -> list[str]:
    ls = _git(root, "ls-files")
    if ls.returncode != 0 or not ls.stdout.strip():
        return []
    out: list[str] = []
    for ln in ls.stdout.splitlines():
        ln = ln.strip().replace("\\", "/")
        if ln and SHEET_RE.search(ln):
            out.append(ln)
    return out


def _write_skill_sheet_refs(root: Path, basename: str, version_ym: str) -> None:
    """Jekyll 用 YAML とリポジトリ直下の .env 形式（環境変数用）だけを書く。"""
    data_dir = root / "docs" / "_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    yml = data_dir / "skill_sheet.yml"
    env_path = root / "skill_sheet.env"
    yml.write_text(
        "# scripts/update_skill_sheet_meta.py が更新\n"
        f"file: {basename}\n"
        f'version_ym: "{version_ym}"\n',
        encoding="utf-8",
        newline="\n",
    )
    env_path.write_text(
        "# scripts/update_skill_sheet_meta.py が更新\n"
        f"SKILL_SHEET_FILE={basename}\n"
        f"SKILL_SHEET_VERSION_YM={version_ym}\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    root = _git_root()
    if root is None:
        print("git リポジトリのルートで実行してください", file=sys.stderr)
        return 1

    now = datetime.now()
    ym = now.strftime("%Y%m")
    today = now.strftime("%Y-%m-%d")

    for _ in range(8):
        paths = _tracked_skill_sheet_paths(root)
        paths = [p for p in paths if (root / p).is_file()]
        if not paths:
            break
        line_norm = paths[0]

        path = root / line_norm
        text = path.read_text(encoding="utf-8")
        out = text
        out = re.sub(
            r"^# スキルシート（\d{6}）",
            f"# スキルシート（{ym}）",
            out,
            flags=re.MULTILINE,
        )
        out = re.sub(
            r"^- スキルシート版：\d{6}",
            f"- スキルシート版：{ym}",
            out,
            flags=re.MULTILINE,
        )
        if _FINAL_UPDATE_LINE.search(out):
            out = _bump_final_update_line(out, today)
        else:
            out = re.sub(
                r"(^- スキルシート版：\d{6}\s*\n)",
                rf"\1- 最終更新：{today} #1\n",
                out,
                count=1,
                flags=re.MULTILINE,
            )
        path.write_text(out, encoding="utf-8", newline="\n")

        rel_p = Path(line_norm)
        parent = rel_p.parent
        if str(parent) == ".":
            new_rel = f"skill_sheet_{ym}_SN.md"
        else:
            new_rel = f"{parent.as_posix()}/skill_sheet_{ym}_SN.md"

        if line_norm != new_rel:
            mv = subprocess.run(
                ["git", "-C", str(root), "mv", "--", line_norm, new_rel],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if mv.returncode != 0:
                print(mv.stderr or mv.stdout, file=sys.stderr)
                return 1
            continue

        break

    paths = _tracked_skill_sheet_paths(root)
    if not paths:
        return 0
    basename = Path(paths[0]).name
    m = re.match(r"^skill_sheet_(\d{6})_SN\.md$", basename)
    version_ym = m.group(1) if m else ym
    _write_skill_sheet_refs(root, basename, version_ym)

    return 0


if __name__ == "__main__":
    sys.exit(main())
