import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)

c.NotebookApp.ip = '0.0.0.0'
#c.NotebookApp.password = '' #Please, generate it from device
#c.NotebookApp.notebook_dir = '{}/catkin_ws/src/autominy_msgs'.format(root_path)
c.NotebookApp.default_url = '/lab?'.format(root_path)

c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.use_redirect_file = False