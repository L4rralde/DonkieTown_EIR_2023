export EIR_PATH=$(dirname $(readlink -f "${BASH_SOURCE:-$0}"))
source $EIR_PATH/catkin_ws/devel/setup.zsh
~/.local/bin/jupyter-lab --config=.jupyter/jupyter_notebook_config.py