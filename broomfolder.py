#!/usr/bin/env python3
"""Interactively organize files in a chosen folder."""

from __future__ import annotations

import argparse
import stat
import shutil
import sys
from pathlib import Path


COMMANDS = {"help", "list", "skip", "quit"}
BANNER = r"""
        \
         \
          \
           \
        ____\____
       /    |    \
      /_____|_____\
     ///////|///////

   .----------------.
  /________________/|
  |   CLEAN DIR    |/
  |________________|
"""


def main() -> int:
    args = parse_args()

    print_banner()
    print_command_summary()

    target = choose_directory(args.directory)
    if target is None:
        return 1

    files = discover_files(target)
    if not files:
        print(f"No top-level files to organize in {target}.")
        return 0

    print(f"\nOrganizing {len(files)} file(s) in {target}")
    print("Type a destination folder name or use a built-in command.\n")

    moved = 0
    skipped = 0
    total_files = len(files)

    for index, file_path in enumerate(files, start=1):
        if not file_path.exists() or not file_path.is_file():
            continue

        print(format_progress(index, total_files))
        print(f"File: {file_path.name}")
        action = prompt_for_file_action(target, file_path)

        if action == "quit":
            print("Stopping.")
            break

        if action == "skip":
            skipped += 1
            print("Skipped.\n")
            continue

        destination_dir = action
        destination_path = destination_dir / file_path.name

        if destination_path.exists():
            resolved = resolve_conflict(destination_path)
            if resolved is None:
                skipped += 1
                print("Skipped to avoid overwriting.\n")
                continue
            destination_path = resolved

        shutil.move(str(file_path), str(destination_path))
        moved += 1
        print(f"Moved to {destination_path.relative_to(target)}\n")

    print(f"Done. Moved: {moved}. Skipped: {skipped}.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactively organize the top-level files in a folder."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="Directory to organize. If omitted, the command prompts for one.",
    )
    return parser.parse_args()


def choose_directory(initial_directory: str | None) -> Path | None:
    if initial_directory:
        return validate_directory(initial_directory)

    while True:
        raw = input("Folder to organize [current directory]: ").strip()
        raw = raw or "."
        candidate = validate_directory(raw)
        if candidate is not None:
            return candidate


def validate_directory(raw_path: str) -> Path | None:
    candidate = expand_directory(raw_path)

    if not candidate.exists():
        print(f"Directory does not exist: {candidate}")
        return None

    if not candidate.is_dir():
        print(f"Not a directory: {candidate}")
        return None

    return candidate


def expand_directory(raw_path: str) -> Path:
    return Path(raw_path).expanduser().resolve()


def discover_files(target: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in target.iterdir()
            if path.is_file() and not is_hidden_path(path)
        ),
        key=lambda path: path.name.lower(),
    )


def format_progress(current: int, total: int) -> str:
    percent = round((current / total) * 100)
    remaining = total - current
    return f"[{current}/{total} files] {percent}% | {remaining} left"


def print_banner() -> None:
    print(BANNER)
    print("BroomFolder")
    print("Organize top-level files into folders, one prompt at a time.\n")


def print_command_summary() -> None:
    print("Commands:")
    print("  help  Show the full in-session guide")
    print("  list  Show directories and optionally create one")
    print("  skip  Leave the current file where it is")
    print("  quit  Stop organizing and exit\n")


def print_detailed_help() -> None:
    print("BroomFolder Help")
    print("  Enter a folder name to move the current file into that directory.")
    print("  Folder names are always resolved inside the selected directory.")
    print("  Use 'list' to inspect existing directories and create a new one.")
    print("  Use 'skip' to leave the current file untouched.")
    print("  Use 'quit' to stop processing the remaining files.")
    print("  If a filename already exists in the destination, you can skip or rename it.\n")


def prompt_for_file_action(target: Path, file_path: Path) -> Path | str:
    while True:
        raw = input("Move to folder> ").strip()
        command = raw.lower()

        if command in COMMANDS:
            if command == "help":
                print_detailed_help()
                print_current_file_context(file_path)
                continue
            if command == "list":
                show_directories(target)
                maybe_create_directory(target)
                print_current_file_context(file_path)
                continue
            return command

        if not raw:
            print("Enter a folder name, or use: help, list, skip, quit.")
            print_current_file_context(file_path)
            continue

        destination_dir = folder_inside_target(target, raw)
        if destination_dir is None:
            print("Folder names must stay inside the selected directory.")
            print_current_file_context(file_path)
            continue

        if not destination_dir.exists():
            if ask_yes_no(f"Create folder '{destination_dir.relative_to(target)}'? [y/N] "):
                destination_dir.mkdir(parents=True, exist_ok=True)
            else:
                print("Choose another folder.")
                print_current_file_context(file_path)
                continue

        if not destination_dir.is_dir():
            print(f"Destination exists but is not a directory: {destination_dir}")
            print_current_file_context(file_path)
            continue

        return destination_dir


def print_current_file_context(file_path: Path) -> None:
    print(f"Still organizing: {file_path.name}")


def folder_inside_target(target: Path, raw_folder: str) -> Path | None:
    folder = Path(raw_folder).expanduser()

    if folder.is_absolute():
        print("Use a folder name relative to the selected directory.")
        return None

    candidate = (target / folder).resolve()
    try:
        candidate.relative_to(target)
    except ValueError:
        return None
    return candidate


def is_hidden_path(path: Path) -> bool:
    if path.name.startswith("."):
        return True

    try:
        attributes = path.stat().st_file_attributes
    except AttributeError:
        return False
    except OSError:
        return False

    return bool(attributes & stat.FILE_ATTRIBUTE_HIDDEN)


def show_directories(target: Path) -> None:
    directories = sorted(
        (path for path in target.iterdir() if path.is_dir() and not is_hidden_path(path)),
        key=lambda path: path.name.lower(),
    )

    if not directories:
        print("No directories yet.")
        return

    print("Directories:")
    for directory in directories:
        print(f"  - {directory.relative_to(target)}")


def maybe_create_directory(target: Path) -> None:
    if not ask_yes_no("Create a new directory? [y/N] "):
        return

    while True:
        raw = input("New directory name: ").strip()
        if not raw:
            print("Directory name cannot be empty.")
            continue

        directory = folder_inside_target(target, raw)
        if directory is None:
            print("Directory must stay inside the selected directory.")
            continue

        if directory.exists():
            if directory.is_dir():
                print(f"Directory already exists: {directory.relative_to(target)}")
                return
            print(f"A file already exists at: {directory.relative_to(target)}")
            continue

        directory.mkdir(parents=True)
        print(f"Created: {directory.relative_to(target)}")
        return


def resolve_conflict(destination_path: Path) -> Path | None:
    print(f"Destination already exists: {destination_path.name}")

    while True:
        answer = input("Type 'skip' or 'rename': ").strip().lower()
        if answer == "skip":
            return None
        if answer == "rename":
            return next_available_path(destination_path)
        print("Please type 'skip' or 'rename'.")


def next_available_path(path: Path) -> Path:
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2

    while True:
        candidate = parent / f"{stem} {counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def ask_yes_no(prompt: str) -> bool:
    return input(prompt).strip().lower() in {"y", "yes"}


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped.")
        raise SystemExit(130)
