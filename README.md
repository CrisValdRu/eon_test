# eon_test

Este documento contiene las instrucciones para la instalación de las tecnologías
que se van a utilizar para este proyecto, así como una breve introducción a 
comandos, instrucciones, archivos y directorios. 

# PostgreSQL

Instalaremos los paquetes necesarios. Como superusuario ejecutamos las siguiente instrucción

	apt-get install postgresql postgresql-contrib
	
O especificando las versiones

    apt-get install postgresql-9.6 postgresql-contrib

Cambiar la contraseña del usuario postgres (como superusuario) y acceder como él

    passwd postgres
    su postgres

**Nota:** La contraseña del usuarios postgres para los ejemplos es _postgres_.

Ingresar a la consola de postgres (psql) y ejecutar las siguientes instrucciones

    psql
    CREATE DATABASE acme_db;
    CREATE USER acme_admin WITH PASSWORD '4cm3-4dm1n';
    ALTER ROLE acme_admin SET client_encoding TO 'utf8';
    ALTER ROLE acme_admin SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE acme_db TO acme_admin;

Para permitir al usuario de la base de datos crear una base de datos de prueba desde django, es necesario ejecutar el siguiente programa

    ALTER USER acme_admin CREATEDB;


# Django y DRF

## Instalación en Ubuntu y Debian

Primero es necesario instalar los paquetes requeridos de python3. 

### Método 1 
La primera forma de instalar python junto con sus dependencias es ingresar la siguiente instrucción como _root_:

    apt-get install python3 python3-pip python3-dev libpq-dev

### Método 2

1. Descargar de la [página oficial](https://www.python.org/downloads/) de python la versión que requieres. En este caso vamos a utilizar la versión 3.8.10. El archivo que descargaste debe tener extensión .tar.xz

2. Ejecutar las siguientes instrucciones

		apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev 
	    apt-get install libreadline-dev libtk8.5 libgdm-dev libdb4o-cil-dev libpcap-dev
	    apt-get install postgresql-server-dev-X.Y
   Donde X.Y es la versión de postgres
3. Dirigirse a la carpeta _Downloads_ o _Descargas_ o donde se haya descargado el archivo _.tar_.

4. Descomprimir el archivo con la siguiente instrucción

		tar -xvf Python-3.8.10.tar.xz

5. Crear un directorio

		cd /usr/local/
		mkdir python3.8.10

6. Movemos el contenido del archivo que se generá de descomprimir el _.tar_ a la carpeta que acabamos de crear.

		cd python3.8.10
		mv /home/admin3/Downloads/Python-3.8.10/* .

7. Ejecutamos la siguiente instrucción

		./configure  --enable-optimizations

8. Ejecutamos la siguiente instrucción

		make
		make altinstall # Esto creara una instalación aparte de la instalación que viene por defecto con Linux



## Entornos

Las aplicaciones en python generalmente usan paquetes y modulos que no forman parte de las bibliotecas estándar de python. Algunas veces las aplicaciones requieren versiones específicas de una biblioteca para poder ejecutarse, por ejemplo, si una aplicación A requiere la versión 1.0 de un módulo en particular y una aplicación B requiere la versión 2.0 del mismo módulo va a existir un conflicto en el que sólo alguna de las dos aplicaciones se pueda ejecutar. Es por esto que se implementó una solución conocida como _entorno virtual_ la cual es un árbol de directorios que contiene una instalación de Python para una versión particular de Python.

Para poder crear nuestra aplicación en python lo primero es crear un nuevo directorio. 

    mkdir <nombre_carpeta>
	cd <nombre_carpeta>
	
Posteriormente ejecutamos la siguiente instrucción que nos permitirá crear el entorno virtual para nuestro proyecto.

	python3.8 -m venv venv


Habilitamos el entorno virtual ejecutando las siguientes instrucciones

    source venv/bin/activate
 O puedes ejecutar las siguiente instrucción
    
	. venv/bin/activate

En el directorio en el que nos encontramos creamos un nuevo archivo que lleva por nombre _requirements.txt_. Este archivo contiene todas las dependencias que se van a manejar para nuestro proyecto y se van a instalar para el entorno que creamos. Agregamos las siguientes líneas

	Django==2.2.3
    djangorestframework==3.10.3
    markdown==3.1.1
    django-filter==2.2.0
    psycopg2==2.8.6
    django-cors-headers==3.1.1
    pyyaml==5.1.2
    coreapi==2.3.3
    drf-yasg==1.17.0
    django-oauth-toolkit==1.2.0
    pylint==2.4.2
    pylint-django==2.0.11
    packaging==19.2
    pillow==6.2.1
    django-extra-fields==1.2.4
    pypdf2==1.26.0
    celery==4.3.0
    pika==1.1.0
    django-celery-results==1.1.2
    gunicorn==20.0.4

Para instalar las dependencias debes ejecutar la siguiente instrucción

	pip install -r requirements.txt
	
## Configurar Django

Una vez descargado los archivos del repositorio, hay que modificar el archivo setings.py hubicado en el directorio pruebaEON/pruebaEON/setings.py 
hay que agregar la direccion IP del equipo que corre el sisitema a la lista
    
    ...
    ALLOWED_HOSTS = ['192.168.100.31', 'localhost', <nuevaIP>]
    ...

Para verificar que el proyecto funciona ejecutamos la siguiente instrucción, para poder ejecutar este comando hay que hubicarnos en el directorio 
eon_test/pruebaEON

	python3 manage.py runserver <nuevaIP>:8080

Esto va a levantar un servidor donde podemos verificar que el proyecto funciona. Debemos acceder a la siguiente liga [http://nuevaIP:8000/](http://<nuevaIP>:8000/) y nos deberá desplegar una página de inicio.

Ahora hay que crear las tablas a la base de datos y llenarla con los datos de los fxtures. Para ello hay que ejecutar los sigientes comandos

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py loaddata /acme/fixtures/Categoria_producto.yaml /acme/fixtures/Producto.yaml /acme/fixtures/Usuario.yaml

Para acceder a la vista que muestra la documentacion de los endpoints hay que acceder a la siguiete liga [http://nuevaIP:8080/docs/](http://<nuevaIP>:8000/docs/)

En caso de que se quiera crear un nuevo proyecto de Django hay que seguir los siguientes pasos.

## Crear proyectos

Una vez se ha concluido la instalación de dependencias para el entorno virtual que se creó podemos crear nuestro proyecto en Django. En el mismo directorio donde se encuentra nuestro archivo requirements.txt ejecutamos la siguiente instrucción

    django-admin startproject <project_name> .

Esto va a crear los siguientes archivos y directorio

|Arhivo o directorio| Descripción |
| ----------------- | ----------- |
|manage.py| Archivo que contiene los scripts que se pueden ejecutar.|
|project_name/|Carpeta que contiene la configuración del proyecto.|
|project_name/settings.py| El archivo de configuración de Django contiene toda la configuración del proyecto. |
|project_name/urls.py| Este archivo contiene las URLs de la aplicación Este módulo es el mapeo entre una URL y funciones en Python( las vistas )|
|project_name/wsgi.py| Este archivo contiene la configuración WSGI para el proyecto el cual es llamado cuandp se ejecuta la línea _runserver_. El WSGI(Web Server Gateway Interface) no es un servidor, un módulo de python, un framework, o una API, sólo es la espeicificación de una interfaz que permite la comunicación entre un servirdor y la aplicación.|

Se puede ver la aplicación de Django que creamos como un proyecto al cual se le van agregando aplicaciones o módulos conforme se requiera. Para crear un módulo o aplicación se debe utilizar la siguiente instrucción _startapp_ como se muestra a continuación

	django-admin startapp <module_name>
	
Esto creará un directorio con el nombre que hayas escrito que contiene los siguientes archivos o directorios.

|Archivo o Directorio|Descripción|
| ----- | --------- |
|\_\_init.py\_\_| Archivo vacío que le indica a python que todo el contenido del directorio es un paquete.|
|admin.py||
|apps.py||
|migrations/|Carpeta en el que se van almacenando los cambios hechos a los modelos y a la base de datos.|
|models.py|Archivo en el que se escribe el código para los modelos.|
|tests.py| Archivo en el que se escribe el código para las pruebas.|
|views.py| Archivo en el que se escribe el código para las vistas.|



## Verificar instalación

Para verificar que el proyecto funciona ejecutamos la siguiente instrucción

	python3 manage.py runserver

Esto va a levantar un servidor donde podemos verificar que el proyecto funciona. Debemos acceder a la siguiente liga [http://localhost:8000/](http://localhost:8000/) y nos deberá desplegar una página de inicio.

