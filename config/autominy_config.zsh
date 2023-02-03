export COURSE_PATH=$(dirname $(readlink -f "${BASH_SOURCE:-$0}"))
source $COURSE_PATH/catkin_ws/devel/setup.zsh
~/.local/bin/jupyter-lab --config=$COURSE_PATH/.jupyter/jupyter_notebook_config.py