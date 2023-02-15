#!/bin/bash

cd $(dirname $(readlink -f "${BASH_SOURCE:-$0}"))
COURSE_PATH=$(git rev-parse --show-toplevel)
cd - > /dev/null
PIC=$COURSE_PATH/docs/imgs/background.jpg
gsettings set org.gnome.desktop.background picture-uri "file://$PIC"