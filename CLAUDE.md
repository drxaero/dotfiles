# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A personal dotfiles repository managed by [Dotbot](https://github.com/anishathalye/dotbot). Configs are stored under `apps/<tool>/` and symlinked into `~` by Dotbot.

## Installation

```bash
cd ~/.dotfiles/
./install
```

This syncs the `dotbot` submodule, then runs Dotbot with `install.conf.yaml`, which:
1. Cleans broken symlinks from `~`
2. Creates symlinks (e.g. `~/.zshrc → apps/zsh/zshrc`)
3. Downloads JetBrains Mono font
4. Runs `apps/homebrew/setup_homebrew` (installs/updates Homebrew and runs `brew bundle`)

## Testing

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest tests/

# Run a single test file
poetry run pytest tests/zsh/test_zshrc.py

# Run a single test
poetry run pytest tests/zsh/test_zshrc.py::test_name
```

Tests use `pexpect` to spawn real shell processes and verify interactive behavior. CI runs on macOS with Python 3.13 via GitHub Actions (`.github/workflows/pytest.yml`).

## Code Quality

```bash
# Run pre-commit hooks on all files
pre-commit run --all-files

# Run ruff linting
poetry run ruff check .
```

Config: max line length 120.

## Commit Message Convention

```
[ENV][CATEGORY][optional_context] Description.
```

**Environment:** `[PROD]` (user-facing) or `[DEV]` (infrastructure/CI)

**Categories:** `[NEW_FEATURE]`, `[UPDATED]`, `[BUG_FIXED(hash)]`, `[REFACTORED]`, `[REMOVED_FEATURE]`, `[DOC]`, `[BEHAVIOR_CHANGED]`

Multiple changes in one commit stack the tags: `[PROD][UPDATED] Updated Brewfile. [PROD][UPDATED] Added 'watch' command.`

## Repository Structure

- `apps/<tool>/` — configuration files for each tool (zsh, bash, git, vim, screen, homebrew, Terminal)
- `install.conf.yaml` — Dotbot config declaring symlinks and shell commands
- `install` — bootstrap script that updates the `dotbot` submodule and runs Dotbot
- `tests/` — pytest suite; currently covers zsh prompt behavior and font installation
- `dotbot/` — git submodule pinned to v1.24.1
- `pyproject.toml` — Python dev dependencies (pytest, ruff, pexpect, pre-commit)

## Key Details

- **Shell:** Zsh is primary; Bash config also maintained in `apps/bash/`
- **Python:** Requires ≥3.13 (managed via Homebrew)
- **Homebrew packages:** Defined in `apps/homebrew/Brewfile`; update by editing the Brewfile and re-running `./install` or `brew bundle`
- **Adding a new dotfile:** Add the file under `apps/<tool>/`, then add a `link:` entry in `install.conf.yaml`
