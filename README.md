# BroomFolder

`broomfolder` is a dependency-free Python command that helps you organize a folder interactively.

It opens with a terminal banner, asks which directory to work in, shows progress while you sort, and moves top-level files into folders you choose.

## Usage

Run it from this repo:

```sh
./bin/broomfolder
```

At the prompt, choose a directory such as:

```text
.
~/Downloads
/Users/you/Downloads
```

You can also pass the directory directly:

```sh
broomfolder ~/Downloads
```

For each file, enter a folder name to move it there. You can also type:

- `help` to show the in-session command guide
- `list` to show existing directories and optionally create a new one
- `skip` to leave the current file where it is
- `quit` to stop

After `help`, `list`, or a validation retry, the prompt reminds you which file is still being organized so you do not need to scroll back up.

The tool only processes top-level, non-hidden files. It does not recursively organize subfolders.

## Features

- Startup banner and built-in command summary
- Progress display such as `[123/220 files] 56% | 97 left`
- Optional directory argument like `broomfolder ~/Downloads`
- Interactive `help` command inside a sorting session
- Zsh command and directory completion support through the installer

## Install

Make the script executable:

```sh
chmod +x bin/broomfolder
```

Install it as a command with the helper:

```sh
./install.sh
```

The installer also attempts to install zsh completion support.

If macOS says you do not have permission, run:

```sh
sudo ./install.sh
```

Or install it manually:

```sh
ln -s "$(pwd)/bin/broomfolder" /usr/local/bin/broomfolder
```

After that, run it from anywhere:

```sh
broomfolder
broomfolder ~/Downloads
```

If the command does not autocomplete right away in zsh, run:

```sh
rehash
```

If you install into `~/.local/bin`, make sure that directory is in your `PATH`.

If you install completions into `~/.zsh/completions`, make sure your `~/.zshrc` includes:

```sh
fpath=("$HOME/.zsh/completions" $fpath)
autoload -Uz compinit
compinit
```
