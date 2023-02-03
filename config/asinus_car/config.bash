cd $(dirname $(readlink -f "${BASH_SOURCE:-$0}"))
export COURSE_PATH=$(git rev-parse --show-toplevel)
cd - > /dev/null
source $COURSE_PATH/catkin_ws/devel/setup.bash
#jupyter-lab --config=$COURSE_PATH/.jupyter/jupyter_notebook_config.py