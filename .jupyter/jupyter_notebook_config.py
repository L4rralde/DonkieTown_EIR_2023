import os 
import sys
root_path = os.getenv("COURSE_PATH")
sys.path.append('{}/.jupyter'.format(root_path))
import credentials

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = credentials.pswd
c.NotebookApp.notebook_dir = root_path

c.NotebookApp.port = 8890
c.NotebookApp.open_browser = False
c.NotebookApp.use_redirect_file = False