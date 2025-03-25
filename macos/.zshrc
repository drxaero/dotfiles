# Define the shell prompt

# Using 'precmd' or PROMPT_SUBST is better for dynamic prompt updates
colored_dollar() {
    if [ "$?" -eq 0 ]; then
        echo "%F{green}"
    else
        echo "%F{red}"
    fi
}

# Enable prompt substitution to allow command/function evaluation
setopt PROMPT_SUBST

PROMPT='[%F{white}%n@%m]:%F{blue}%1~%f/$(colored_dollar)%#%f '
RPROMPT='%*'

# 用 `-F` 在目錄名右邊顯示 `/`
# 用 `-G` 顯示彩色
alias ls='ls -FG'

# Created by `pipx` on 2025-03-19 08:55:34
export PATH="$PATH:~/.local/bin"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
