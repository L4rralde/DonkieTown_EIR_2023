export COURSE_PATH=$(git rev-parse --show-toplevel)
source $COURSE_PATH/catkin_ws/devel/setup.bash
#jupyter-lab --config=$COURSE_PATH/.jupyter/jupyter_notebook_config.py