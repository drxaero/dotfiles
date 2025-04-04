# Runs by interactive zsh sessions only.

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
alias ls='eza -F'

# Created by `pipx` on 2025-03-19 08:55:34
#export PATH="$PATH:~/.local/bin"

# colorful man using `bat`
export MANPAGER="sh -c 'sed -u -e \"s/\\x1B\[[0-9;]*m//g; s/.\\x08//g\" | bat -p -lman'"

#############################
# Start ssh-agent when login
#############################
#SSH_ENV=$HOME/.ssh/environment
#
## start the ssh-agent
#function start_agent {
#   echo -n "Initializing new SSH agent... "
#   # spawn ssh-agent
#   /usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
#   echo "[succeeded]"
#   chmod 600 "${SSH_ENV}"
#   . "${SSH_ENV}" > /dev/null
#
#   # specify which private keys to add
#   /usr/bin/ssh-add $HOME/.ssh/id_rsa
#}
#
#if [ -f "${SSH_ENV}" ]; then
#   . "${SSH_ENV}" > /dev/null
#   ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
#      start_agent;
#   }
#else
#   start_agent;
#fi
#
############################
## Kill ssh-agent when logout
############################
#trap 'test -n "$SSH_AGENT_PID" && eval `/usr/bin/ssh-agent -k`' 0


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


# The following lines have been added by Docker Desktop to enable Docker CLI completions.
fpath=(~/.docker/completions $fpath)
autoload -Uz compinit
compinit
# End of Docker CLI completions
