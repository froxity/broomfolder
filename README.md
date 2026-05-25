# BroomFolder

`broomfolder` is a dependency-free Python command that helps you organize a folder interactively.

It opens with a terminal banner, asks which directory to work in, shows progress while you sort, and moves top-level files into folders you choose.

## Usage

Run it from this repo:

```sh
python3 broomfolder.py
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
python3 broomfolder.py ~/Downloads
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
- Launchers for Linux, macOS, and Windows
- Zsh command and directory completion support through the Unix installer

## Requirements

- Python 3.9 or newer

## Install

### macOS and Linux

```sh
chmod +x bin/broomfolder
./install.sh
```

This installs the Unix launcher and also attempts to install zsh completion support.

If `/usr/local/bin` is not writable, run:

```sh
sudo ./install.sh
```

Or install it manually:

```sh
ln -s "$(pwd)/bin/broomfolder" /usr/local/bin/broomfolder
```

### Windows

Run the PowerShell installer:

```powershell
.\install.ps1
```

By default it installs `broomfolder.cmd` and `broomfolder.py` into:

```text
%USERPROFILE%\AppData\Local\Programs\broomfolder\bin
```

Make sure that directory is in your `PATH`.

You can also run it directly from the repo:

```powershell
py -3 .\broomfolder.py
py -3 .\broomfolder.py C:\Users\you\Downloads
```

## Running

After installation, run it from anywhere:

```sh
broomfolder
broomfolder ~/Downloads
```

On Windows Command Prompt or PowerShell, use:

```powershell
broomfolder
broomfolder C:\Users\you\Downloads
```

If zsh command completion does not activate right away on macOS or Linux, run:

```sh
rehash
```

If you install into `~/.local/bin` on Unix, make sure that directory is in your `PATH`.

If you install completions into `~/.zsh/completions`, make sure your `~/.zshrc` includes:

```sh
fpath=("$HOME/.zsh/completions" $fpath)
autoload -Uz compinit
compinit
```
