#!/usr/bin/env sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_path="$repo_dir/bin/broomfolder"
completion_source="$repo_dir/completions/_broomfolder"
install_dir="${BROOMFOLDER_INSTALL_DIR:-/usr/local/bin}"
install_path="$install_dir/broomfolder"

case "$install_dir" in
  "$HOME"/.local/bin)
    completion_dir="${BROOMFOLDER_COMPLETION_DIR:-$HOME/.zsh/completions}"
    ;;
  /usr/local/bin)
    completion_dir="${BROOMFOLDER_COMPLETION_DIR:-/usr/local/share/zsh/site-functions}"
    ;;
  *)
    completion_dir="${BROOMFOLDER_COMPLETION_DIR:-}"
    ;;
esac

if [ ! -x "$source_path" ]; then
  chmod +x "$source_path"
fi

mkdir -p "$install_dir"

if [ ! -w "$install_dir" ]; then
  printf 'No write permission for %s. Try: sudo ./install.sh\n' "$install_dir" >&2
  exit 1
fi

ln -sf "$source_path" "$install_path"

printf 'Installed broomfolder at %s\n' "$install_path"
printf 'Run `rehash` in zsh if the command does not autocomplete immediately.\n'

if [ -n "$completion_dir" ]; then
  if mkdir -p "$completion_dir" 2>/dev/null && [ -w "$completion_dir" ]; then
    ln -sf "$completion_source" "$completion_dir/_broomfolder"
    printf 'Installed zsh completion at %s/_broomfolder\n' "$completion_dir"

    if [ "$completion_dir" = "$HOME/.zsh/completions" ]; then
      printf 'If needed, add `fpath=(%s $fpath)` to ~/.zshrc and run `autoload -Uz compinit && compinit`.\n' "$completion_dir"
    fi
  else
    printf 'Skipped zsh completion install because %s is not writable.\n' "$completion_dir" >&2
  fi
fi
