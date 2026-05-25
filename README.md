# BroomFolder

`broomfolder` is a dependency-free Python command that helps you organize a folder interactively.

It asks which directory to work in, reviews each top-level file, and moves files into folders you choose.

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

For each file, enter a folder name to move it there. You can also type:

- `list` to show existing directories and optionally create a new one
- `skip` to leave the current file where it is
- `quit` to stop

The tool only processes top-level, non-hidden files. It does not recursively organize subfolders.

## Install

Make the script executable:

```sh
chmod +x bin/broomfolder
```

Install it as a command with the helper:

```sh
./install.sh
```

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
```

If `/usr/local/bin` is not in your `PATH`, add it to your shell profile.
