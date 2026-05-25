#!/usr/bin/env sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_path="$repo_dir/bin/broomfolder"
install_path="/usr/local/bin/broomfolder"

if [ ! -x "$source_path" ]; then
  chmod +x "$source_path"
fi

mkdir -p /usr/local/bin

if [ ! -w /usr/local/bin ]; then
  printf 'No write permission for /usr/local/bin. Try: sudo ./install.sh\n' >&2
  exit 1
fi

ln -sf "$source_path" "$install_path"

printf 'Installed broomfolder at %s\n' "$install_path"
