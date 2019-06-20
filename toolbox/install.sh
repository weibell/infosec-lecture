#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASHRC_LINE="if [ -f $DIR/bashrc/entrypoint ]; then . $DIR/bashrc/entrypoint ; fi"

if grep -qxF "$BASHRC_LINE" ~/.bashrc; then
	echo "Line already contained in ~/.bashrc"
else
	echo >> ~/.bashrc
	echo "$BASHRC_LINE" >> ~/.bashrc
	echo "~/.bashrc has been updated."
fi


echo "Remember to run '. ~/.bashrc' or open a new shell."
