#!/usr/bin/env zsh

# install the "JetBrainsMono-Regular.ttf" for the powerline symbol '' ('\uE0A0')
cd ~/Library/Fonts && {
    curl -O 'https://github.com/JetBrains/JetBrainsMono/blob/master/fonts/ttf/JetBrainsMono-Regular.ttf'
    cd -; }
