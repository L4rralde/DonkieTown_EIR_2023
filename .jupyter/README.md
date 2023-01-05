# Instrucciones
`~/.local/bin/jupyter-lab --config=./jupyter_notebook_config.py`

## Configuración
### Generar contraseña
En una nootebook de python3:
```
from notebook.auth import passwd
passwd()
```