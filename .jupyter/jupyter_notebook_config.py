import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$2l3DsvsF9z7iNqdhvifGxQ$XyU560upIk8VI3C335ZBPg'
c.NotebookApp.certfile = u'{}/mycert.pem'.format(dir_path)
c.NotebookApp.keyfile = u'{}/mykey.key'.format(dir_path)
c.NotebookApp.notebook_dir = '{}/catkin_ws/src/autominy_msgs'.format(root_path)
c.NotebookApp.default_url = '/lab?'.format(root_path)

c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.use_redirect_file = False