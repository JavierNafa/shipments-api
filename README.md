
  
  

  

# SHIPMENTS API

  

API desarrollada para Gustavo :)

  
<details  open="open">
<summary>Contenido</summary>
<ol>
<li><a  href="#acerca">Acerca</a></li>
<li><a  href="#requerimientos">Requerimientos</a></li>
<li><a  href="#instalación">Instalación</a>
<ul>
<li><a  href="#normal">Normal</a></li>
<li><a  href="#docker">Docker</a></li>
</ul>
</li>
</ol>
</details>

  

  

## Acerca

  

Se desarrolló una API REST para el alta de estados, municipios y colonias. Cuenta con autenticación.

Para el desarrollo del proyecto se usaron las siguientes tecnologías.

  

*  [Python](https://www.python.org/)

  

*  [FastAPI](https://fastapi.tiangolo.com/)

  

*  [PostgreSQL](https://www.postgresql.org/)

  

*  [Nginx](https://www.nginx.com/)

  

*  [Docker](https://www.docker.com/)

## Requerimientos

  

* Python v3.8

  

* FastAPI v0.63

  

* PostgreSQL v12

  

* Docker v20.10

  

  

### Instalación

  

Antes de continuar se necesitara crear un entorno virtual y activarlo si no se desea usar docker.

*  [virtualenv](https://pypi.org/project/virtualenv/)

*  [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)

  

Clonar el repositorio.

  

```

git clone https://github.com/JavierNafa/shipments-api.git .

git clone https://github.com/JavierNafa/shipments-api.git

```

  

### Normal

  

1. Ejecuta el siguiente comando dentro de la carpeta /api, que se encuentra en el proyecto.

  

```

pip install -r requirements.txt

```

  

2. Crea un archivo en la carpeta raíz llamado .env para almacenar las siguientes variables de entorno.

| Nombre | Descripción|
| :----------- | :----------------------|
DATABASE_HOST| Ip de la base de datos. |
|DATABASE_USERNAME| Nombre de usuario de la base de datos. |
|DATABASE_PASSWORD| Contraseña de la base de datos. |
|DATABASE_NAME| Nombre de la base de datos.|
|FASTAPI_DEBUG| Variable de tipo bool para iniciar el modo debug de FastAPI.|
|SECRET_KEY| Llave secreta para generar el token.|

 
3. Crea la base de datos y ejecuta el script init.sql que se encuentra en la carpeta de postgresql.

4. Ejecuta el comando ```Python api/main.py``` para correr el proyecto

5. Ahora podrás acceder a las rutas del proyecto, primero debes crear un usuario en la ruta ```<host>/account/register```

 6. Inicia sesion en la ruta ```<host>/account/login```.

 7. Una vez se ha iniciado sesión, se pueden usar los CRUDs.

 8.  Se puede acceder a la documentacion a travez de la url ```<host>/docs``` o ```<host>/redoc```
 
### Docker

1. Una vez que se ha descargado el proyecto se necesitan las variables:
```FASTAPI_DEBUG```
```SECRET_KEY```
```API_PORT```
  
2. Ejecuta el comando ```docker-compose up --build``` o ```docker-compose up --build -d``` para correr todo el proyecto.

3. La api Puede marcar error de conexión a la base de datos al momento de hacer el evento ```on_startup``` pero en un segundo intento se conectara satisfactoriamente.

4. Ahora que esta todo listo se puede acceder a las rutas y a la documentacion. Al host se le agrego una ruta en el nginx que sera por default ```/shipments/api/v1```. Rutas de ejemplo:
```<host>/shipments/api/v1/account/login```
```<host>/shipments/api/v1/docs```

  

## Gracias por leer hasta el final :) 