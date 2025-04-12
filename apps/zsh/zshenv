# Runs by both interactive and non-interactive zsh sessions

# Determine if a command exists
# For example: `% cmd_exits brew` will return 0 if `brew` exists
function cmd_exists() {
  # Why using `command -v` rather than `which`?
  # See "https://stackoverflow.com/a/677212/13852625"
  command -v "$1" >/dev/null 2>&1
}
