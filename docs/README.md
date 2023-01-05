# ROS con DonkieTown

## Instalación
### Imagen de ROS
Hemos generado una imagen (archivo .iso) de Ubuntu para que cualquier dispositivo con procesador Intel/AMD pueda utilizar el material del curso sin tener que instalarlo.

- Descarga la imgen [aquí](https://drive.google.com/file/d/1aLaUVBqgWb4xQuZYf6lOJWrXmu7GLR2S/view?usp=share_link)

- *flashea* la imagen en una memoria usb (de almenos 8GB) utilizando [balena Etcher](https://www.balena.io/etcher/)

- Apaga tu computadora, conecta la memoria usb y reiniciala.

- Accede a la configuración de Arranque del sistema operativo y establece a la memoria usb como el primer método de arranque.

Listo, ya no deberias preocuparte por instalar algún programa

### Jupyter notebooks
Sabemos que Ros Melodic y Ubuntu 18 son versiones ya despreciadas. Sin embargo, como tanto AutoMiny como DonkieTown funcionan sobre estas, decidimos usar Jupyter Notebook como interfaz entre cualquier computadora (con un navegador) y las computadoras de los vehículos. Entonces todo lo que necesitas es un navegador. La desventaja de hacerlo así es que no podrás usar los programas gráficos de ROS.  


## Acerca de DonkieTown
El repo oficial De DonkieTown lo puedes encontrar [aquí](https://github.com/L4rralde/DonkieTown). Sin embergo, para este curso no es necesario instalar el repositorio, pues una computadora central y los vehículos ejecutarán todos los programas que sean necesarios. Por lo tanto, toda la información requerida será incluida en este repositorio.

## Acerca de AutoMiny
AutoMiny es un vehículo inteligente a escala hecho para la educación. La plataforma fue creada en la Universidad Libre de Berlín. A través de un consorcio de Inteligencia Artificial de CONACyT, se donarron dos AutoMinys al CIMAT Zacatecas, pero no se ha hecho una actualización de ROS desde entonces y sigue funcionando con ROS Melodic. La wiki oficial más actualizada del AutoMiny la puedes encontrar [aquí](https://autominy.github.io/AutoMiny/). El repositorio de la versión ROS Melodic está en este [enlace](https://github.com/AutoMiny/AutoMiny/tree/melodic).

## Temas
- [x] Sobre ROS (Qué es, Historia, y dónde se usa)
- [x] Conocimientos previos (Ubuntu,Shell,C/C++,python,Git)
- [ ] DonkieTown y AutoMiny.
- [ ] Cómo iniciar un proyecto en ROS.
- [ ] Cómo crear un nodo.
- [ ] Cómo crear un mensaje en ROS.