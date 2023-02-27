# Apuntes sobre el uso de la terminal en Linux

## Estructura de la línea de comandos (bash)
La estructura por defecto es la siguiente:
```bash
usuario@maquina:path$ 
```
Donde:
- `usuario` es el nombre del usuario actual
- `maquina` es el nombre del ordenador
- `path` es el directorio actual
- `$` ó `#` indica el modo, usuario (`$`) ó superusuario/administrador (`#`)


## Ejecución de comandos
Para ejecutar un comando basta con escribir su nombre, sus argumentos y sus parámetros (en caso de que los tenga), y pulsar `Enter`.

Puedes cancelar la ejecución de un comando que está corriendo con `Ctrl-C`.


### Copiar y pegar
Para copiar un texto de la terminal debes usar `Ctrl-Shift-C`, y para pegar `Ctrl-Shift-V`.


## Paths
Un directorio es una dirección (_path_) dentro del sistema de ficheros del ordenador.  
Están compuestos por carpetas y subcarpetas, separados por `/`, formando un árbol.  

Puedes especificar la dirección de forma absoluta, o relativa (a partir del directorio actual). E.g.:
- `/opt/gul/mi-carpeta` (absoluto, partiendo desde `/`)
- `gul/mi-carpeta` (relativo, partiendo del directorio actual, `/opt`)


## Directorios comunes
- `/`: Directorio raíz del sistema
- `.`: Directorio actual
- `..`: Directorio padre/superior
- `~`: `/home/<user>` "Home", el directorio raíz de tu usuario
- `~/Descargas`: Carpeta de descargas, donde se suele guardar lo que te descargues a través del navegador


## Comandos básicos
- `ls`: muestra los contenidos del directorio (utiliza el flag `-lah` para mostrar todos los archivos, incluídos los ocultos)
- `cd dir`: moverse al directorio _dir_
- `mv origin destination`: mueve el archivo _origin_ al path _destination_
- `cp origin destination`: copia el archivo _origin_ al path _destination_
- `rm file`: elimina el archivo _file_ (utiliza el flag `-r` para carpetas)
- `mkdir dir`: crea el directorio _dir_

Algunos programas útiles y también muy usados son:
- `cat file`: muestra en la terminal los contenidos de _file_
- `wget url`: descarga el contenido de _url_, ya sea el código fuente de una página web o un archivo
- `touch file`: crea el archivo vacío _file_
- `gedit file`: ejecuta el editor de textos gráfico predeterminado y abre con él el archivo _file_
- `nano file`: ejecuta un editor de textos en terminal, y abre con él el archivo _file_

