# foss-example
Por Luis Daniel Casais Mezquida, Jose Antonio Verde Jiménez y Daniel Gómez Schwartz  
[Grupo de Usuarios de Linux](https://gul.uc3m.es)  
[Universidad Carlos III de Madrid](https://uc3m.es)

Ejemplo de un repositorio FOSS para el taller "Linux y el Open Source Software" de la Jornada de Institutos del T3chFest Ed Day 2023.

## Introducción
Éste paquete es un ejemplo de Free Open Source Software, escrito en [Python](https://www.python.org/), y pensado para ejecutarse en Linux.  

Incluye 4 juegos clásicos, listos para ser jugados y modificados:
- [`src/cometas.py`](src/cometas.py): Esquivar asteroides con tu nave
- [`src/buscabombas.py`](src/buscabombas.py): Recreación del clásico Buscaminas de Microsoft
- [`src/arkanoid.py`](src/arkanoid.py): Recreación del clásico Arkanoid
- [`src/pong.py`](src/pong.py): Recreación del clásico Pong, con multijugador en un teclado


## Prerequisitos
Es necesario tener instalado Python 3.8 o superior.  
Puedes comprobar tu versión de Python ejecutando en la terminal:
```bash
python3 --version
```

Éste software viene preparado para ejecutarse con la librería [`pyxel`](https://github.com/kitao/pyxel).  
Puedes instalar la librería usando:
```bash
pip install pyxel
```

En caso de que no puedas instalarla, el repositorio viene con la librería incluída en [`lib/`](lib/) y el script principal en [`bin/pyxel`](bin/pyxel).
En caso de no tener `libSDL2 2.0` (dependencia de pyxel), haz:
```bash
export LD_LIBRARY_PATH="$(pwd)/lib/libSDL2-2.0.so.0"
```


## Instalación
Puedes descargarte la última versión y el código fuente (`Source code (zip)`) desde [Releases](https://github.com/guluc3m/foss-example/releases/latest).

O, usando la terminal:
```bash
wget https://github.com/guluc3m/foss-example/archive/refs/tags/v0.1.0.zip
```

Una vez descargado el archivo comprimido, es necesario navegar a la carpeta de descarga y descomprimirlo:
```bash
cd ~/Descargas
unzip v0.1.0.zip
```

Y ya podemos acceder a nuestro paquete:
```bash
cd foss-example-0.1.0
```


## Ejecución y uso
Para ejecutar un juego basta con llamar con la librería al script deseado, con el argumento `run`.  

Si has instalado pyxel:
```bash
pyxel run <juego>.py
```
E.g.:
```bash
pyxel run src/cometas.py
```

Si no has podido instalar pyxel debes ejecutar el script principal de la librería con Python:
```bash
python3 <pyxel> run <juego>.py
```

E.g.:
```bash
python3 bin/pyxel run src/cometas.py
```

### Rankings
Tres de los cuatro juegos (Buscabombas, Cometas, y Arkanoid) cuentan con un sistema de rankings en el que se guardan las puntuaciones de los jugadores.  

Para activar ésta _feature_ es necesario crear un archivo `<juego>.pts` en la raíz del directorio.  
E.g.:
```bash
touch cometas.pts
```


## Modificando los juegos
Al tener el código fuente de los juegos, puedes editarlos y dejarlos a tu gusto.

### Constantes
Cada juego tiene ciertas variables constantes, o parámetros, ya sea la velocidad o el tamaño de los objetos, etc.  
Al modificar éstos parametros cambias el comportamiento del juego.  

En éstos juegos éstos parámetros están definidos por variables en mayúsculas al principio del archivo.

Para editar el código fuente basta con usar un editor de texto y pasar el archivo como argumento:
```bash
gedit <juego>.py
```

E.g.:
```bash
gedit src/cometas.py
```

### Recursos
Los recursos de un juego son los sprites, la música, y los sonidos.  
Los puedes encontrar dentro del directorio [`resources/`](resources/).

Pyxel incluye un editor de sprites, de sonidos y de música.  
Para editar los recursos de un juego basta con llamar a la librería, el argumento `edit`, y el archivo `.pyxres` donde se guardan los recursos.

Si has instalado pyxel:
```bash
pyxel edit <juego>.pyxres
```
E.g.:
```bash
pyxel edit resources/cometas.pyxres
```

Si no has podido instalar pyxel debes ejecutar el script principal de la librería con Python:
```bash
python3 <pyxel> edit <juego>.pyxres
```

E.g.:
```bash
python3 bin/pyxel edit resources/cometas.pyxres
```

## Información extra
Puedes ver un resumen de cómo funciona la terminal en [`apuntes_terminal.md`](./apuntes_terminal.md).  

Link a las transparencias [aquí](https://cloud-gul.uc3m.es/s/85zY9cAeS3CixaQ).