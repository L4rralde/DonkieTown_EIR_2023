# Instrucciones
## Instala jupyterlab
```
sudo apt update
python3 -m pip install --upgrade pip #pip3 install --upgrade pip
python3 -m pip install jupyter #pip3 install jupyter
python3 -m pip install jupyterlab #pip3 install jupyterlab
```
## Ejecuta jupyter-lab
```
jupyter-lab --config=./jupyter_notebook_config.py
```
o
```
~/.local/bin/jupyter-lab --config=./jupyter_notebook_config.py
```


## Configuración
### Generar contraseña
En una nootebook de python3:
```
from notebook.auth import passwd
passwd()
```