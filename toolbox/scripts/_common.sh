#!/bin/bash

run_tabbed() {
	# https://askubuntu.com/a/1105741
	gnome-terminal --tab --command="bash -c '$1; $SHELL'"
}
