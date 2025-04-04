# Hike

![Hike](https://raw.githubusercontent.com/davep/hike/refs/heads/main/.images/hike-social-banner.png)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/davep/hike/style-lint-and-test.yaml)](https://github.com/davep/hike/actions)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/davep/hike/latest)](https://github.com/davep/hike/commits/main/)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/davep/hike)](https://github.com/davep/hike/issues)
[![GitHub Release Date](https://img.shields.io/github/release-date/davep/hike)](https://github.com/davep/hike/releases)
[![PyPI - License](https://img.shields.io/pypi/l/hike)](https://github.com/davep/hike/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hike)](https://github.com/davep/hike/blob/main/pyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/hike)](https://pypi.org/project/hike/)

## Introduction

Hike is a [Markdown](https://commonmark.org/help/) browser for the terminal.
It provides the ability to browse for and view local Markdown files, as well
as Markdown files that can be downloaded from the web. It also has shortcuts
that make it easy to view Markdown files on popular git forges.

## Installing

### pipx

The application can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install hike
```

Once installed run the `hike` command.

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install hike
```

Once installed run the `hike` command.

### X-CMD

The application can be installed using [`x-cmd`](https://x-cmd.com):

```sh
$ x install hike
```

Once installed run the `hike` command.

## Using Hike

The best way to get to know Hike is to read the help screen. Once in the
application you can see this by pressing <kbd>F1</kbd>.

![Hike Help](https://raw.githubusercontent.com/davep/hike/refs/heads/main/.images/hike-help.png)

Commands can also be discovered via the command palette
(<kbd>ctrl</kbd>+<kbd>p</kbd>):

![The command palette](https://raw.githubusercontent.com/davep/hike/refs/heads/main/.images/hike-command-palette.png)

## Features

- A command line where file names, URLs and commands can be entered.
- A local file browser.
- A simple bookmarking system.
- A browsing history.
- The ability to edit markdown documents in the local filesystem, either
  using your editor of choice or a simple builtin editor.
- Commands for quickly loading and viewing files held on GitHub, GitLab,
  Codeberg and Bitbucket.
- A command palette to make it easy to discover commands and their keys.
- A rich help screen to make it easy to discover commands and their keys.
- [Possibly more as time goes on](https://github.com/davep/hike/issues?q=is%3Aissue+is%3Aopen+label%3ATODO).

### Editing

As mentioned above, Hike has support for editing markdown documents you're
viewing from the local filesystem. While a builtin editor is provided, use
of your own choice of editor is supported. If Hike finds that `$VISUAL` or
`$EDITOR` are set in your environment then the resulting command will be
used to edit the document (with `$VISUAL` being tried first, followed by
`$EDITOR`).

## File locations

Hike stores files in a `hike` directory within both
[`$XDG_DATA_HOME` and
`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/).
If you wish to fully remove anything to do with Hike you will need to
remove those directories too.

Expanding for the common locations, the files normally created are:

- `~/.config/hike/configuration.json` -- The configuration file.
- `~/.local/share/hike/*.json` -- The locally-held data.

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/hike/issues) or [start a
discussion](https://github.com/davep/hike/discussions).

## TODO

See [the TODO tag in
issues](https://github.com/davep/hike/issues?q=is%3Aissue+is%3Aopen+label%3ATODO)
to see what I'm planning.

[//]: # (README.md ends here)
