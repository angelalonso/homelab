#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
  echo "brew installing dependencies"
  brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb >/dev/null 2>&1
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  echo "apt-get installing dependencies. Yes I am assuming it's just a debian-based distro..."
  sudo apt-get update && sudo apt-get install sshpass
fi
