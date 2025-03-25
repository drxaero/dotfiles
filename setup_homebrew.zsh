#!/usr/bin/env zsh

echo "\n=== Starting Homebrew Setup ===\n"

# copied form https://brew.sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Brewfile 中的軟體, 用 `$ brew bundle dump --describe --force` 來產生 Brewfile
brew bundle --verbose