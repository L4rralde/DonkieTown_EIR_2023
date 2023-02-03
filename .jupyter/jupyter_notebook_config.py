import os 
import credentials

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = credentials.pswd
c.NotebookApp.notebook_dir = '{}/main.ipynb'.format(root_path)

c.NotebookApp.port = 8890
c.NotebookApp.open_browser = False
c.NotebookApp.use_redirect_file = False