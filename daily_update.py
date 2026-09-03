#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
README_FILE = PROJECT_DIR / "README.md"

BRANCH = "main"
LOG_HEADER = "## 📅 Development Log"

UPDATE_MESSAGES = [
    "Documentation maintenance",
    "README documentation review",
    "Project documentation improvement",
    "Project structure documentation review",
    "Installation documentation maintenance",
    "Development documentation update",
    "Project information maintenance",
]


def run_command(
    command: list[str],
    *,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a command safely."""
    return subprocess.run(
        command,
        cwd=PROJECT_DIR,
        text=True,
        capture_output=capture,
        check=check,
    )


def git_output(*args: str) -> str:
    """Run git command and return stdout."""
    result = run_command(["git", *args])
    return result.stdout.strip()


def check_git_repository() -> bool:
    """Check whether current directory is a Git repository."""
    try:
        run_command(["git", "rev-parse", "--is-inside-work-tree"])
        return True
    except subprocess.CalledProcessError:
        return False


def check_branch() -> bool:
    """Make sure the current branch is main."""
    branch = git_output("branch", "--show-current")

    if branch != BRANCH:
        print(f"❌ Branch saat ini: {branch}")
        print(f"❌ Script ini hanya bekerja pada branch '{BRANCH}'.")
        return False

    return True


def check_git_identity() -> bool:
    """Check Git username and email."""
    try:
        name = git_output("config", "user.name")
        email = git_output("config", "user.email")
    except subprocess.CalledProcessError:
        return False

    print(f"Git user : {name or '(belum diatur)'}")
    print(f"Git email: {email or '(belum diatur)'}")

    if not name or not email:
        print()
        print("❌ Git identity belum lengkap.")
        print("Atur dengan:")
        print()
        print('git config --global user.name "Nama Kamu"')
        print('git config --global user.email "email-github@example.com"')
        return False

    return True


def check_git_status() -> bool:
    """Check whether repository has unrelated uncommitted changes."""
    status = git_output("status", "--porcelain")

    if status:
        print("❌ Repository memiliki perubahan yang belum di-commit:")
        print()
        print(status)
        print()
        print("Script dihentikan agar tidak mencampurkan perubahan lain.")
        return False

    return True


def ensure_readme() -> None:
    """Make sure README exists."""
    if not README_FILE.exists():
        raise FileNotFoundError(
            f"README tidak ditemukan: {README_FILE}"
        )


def choose_update_message() -> str:
    """Choose a maintenance message based on the day."""
    day = datetime.now().day
    return UPDATE_MESSAGES[day % len(UPDATE_MESSAGES)]


def update_readme(dry_run: bool = False) -> bool:
    """
    Add today's maintenance entry to README.

    Returns True if README was changed.
    """
    ensure_readme()

    content = README_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # Jangan update dua kali pada hari yang sama.
    if today in content:
        print(f"ℹ️ README sudah memiliki entry untuk {today}.")
        return False

    update_message = choose_update_message()

    log_entry = (
        f"| {today} | {update_message} |"
    )

    if LOG_HEADER in content:
        lines = content.splitlines()

        header_index = None

        for index, line in enumerate(lines):
            if line.strip() == LOG_HEADER:
                header_index = index
                break

        if header_index is None:
            return False

        table_header_index = None

        for index in range(header_index + 1, len(lines)):
            if "| Date | Update |" in lines[index]:
                table_header_index = index
                break

        if table_header_index is None:
            # Tambahkan struktur tabel jika belum ada.
            insertion = [
                "",
                "| Date | Update |",
                "|------|--------|",
                log_entry,
            ]

            lines[header_index + 1:header_index + 1] = insertion
        else:
            # Cari baris terakhir tabel.
            insert_at = table_header_index + 1

            while (
                insert_at < len(lines)
                and lines[insert_at].strip().startswith("|")
            ):
                insert_at += 1

            lines.insert(insert_at, log_entry)

        new_content = "\n".join(lines) + "\n"

    else:
        addition = (
            "\n\n"
            f"{LOG_HEADER}\n\n"
            "| Date | Update |\n"
            "|------|--------|\n"
            f"{log_entry}\n"
        )

        new_content = content.rstrip() + addition

    if dry_run:
        print()
        print("🔎 DRY RUN")
        print("Perubahan yang akan dibuat:")
        print()
        print(log_entry)
        return True

    README_FILE.write_text(new_content, encoding="utf-8")

    print(f"✅ README diperbarui: {today}")
    print(f"📝 Update: {update_message}")

    return True


def git_commit_and_push(date: str) -> None:
    """Commit README and push to main."""
    run_command(["git", "add", "README.md"])

    commit_message = f"docs: daily README maintenance {date}"

    result = run_command(
        ["git", "commit", "-m", commit_message],
        check=False,
    )

    if result.returncode != 0:
        print("❌ Git commit gagal.")
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)

    print(f"✅ Commit dibuat: {commit_message}")

    push = run_command(
        ["git", "push", "origin", BRANCH],
        check=False,
    )

    if push.returncode != 0:
        print("❌ Git push gagal.")
        print(push.stdout)
        print(push.stderr)
        sys.exit(push.returncode)

    print("🚀 Berhasil push ke GitHub.")


def check_mode() -> None:
    """Run configuration checks only."""
    print("🔍 Checking project configuration...")
    print()

    if not check_git_repository():
        print("❌ Folder ini bukan Git repository.")
        sys.exit(1)

    print("✅ Git repository ditemukan.")

    if not check_branch():
        sys.exit(1)

    print("✅ Branch main aktif.")

    if not check_git_identity():
        sys.exit(1)

    if not check_git_status():
        sys.exit(1)

    print()
    print("✅ Semua pengecekan berhasil.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Daily README maintenance for student-grade-application."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview perubahan tanpa commit dan push.",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Periksa konfigurasi Git tanpa melakukan perubahan.",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Student Grade Application")
    print("Daily README Maintenance")
    print("=" * 60)
    print()

    if args.check:
        check_mode()
        return

    if not check_git_repository():
        print("❌ Ini bukan Git repository.")
        sys.exit(1)

    if not check_branch():
        sys.exit(1)

    if not check_git_identity():
        sys.exit(1)

    if not check_git_status():
        sys.exit(1)

    changed = update_readme(dry_run=args.dry_run)

    if not changed:
        print()
        print("ℹ️ Tidak ada perubahan yang diperlukan hari ini.")
        return

    if args.dry_run:
        print()
        print("✅ Dry run selesai. Tidak ada commit/push.")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    git_commit_and_push(today)

    print()
    print("🎉 Daily maintenance selesai.")


if __name__ == "__main__":
    main()
