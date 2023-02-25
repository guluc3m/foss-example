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



## Directorios comunes
- `/`: Directorio raíz del sistema
- `.`: Directorio actual
- `..`: Directorio padre/superior
- `~`: `/home/<user>` "Home", el directorio raíz de tu usuario
- `~/Descargas`: Carpeta de descargas, donde se suele guardar lo que te descargues a través del navegador

## Comandos básicos
- `ls`: muestra los contenidos del directorio
- `cd dir`: moverse al directorio _dir_
- `mv origin destination`: mueve el archivo _origin_ al path _destination_
- `cp origin destination`: copia el archivo _origin_ al path _destination_
- `rm file`: elimina el archivo _file_ (utiliza el flag `-r` para carpetas)
- `mkdir dir`: crea el directorio _dir_
- `touch file`: crea el archivo vacío _file_

