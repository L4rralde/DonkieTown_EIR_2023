import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$AGknHNZnibRf97E66hIxXQ$5TDgr9js64cMTG51iUDWPg' #Please, generate it from device
c.NotebookApp.notebook_dir = '{}/'.format(dir_path)

c.NotebookApp.port = 8890
c.NotebookApp.open_browser = False
c.NotebookApp.use_redirect_file = False