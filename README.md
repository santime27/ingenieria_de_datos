# ingenieria_de_datos


este reposisorio se creo con el fin de implementar un cluster de spark utilizando Docker, ademas tambien, se lanza una base de datos mysql.

## creacion de una red tipo bridge en docker


Con el fin de hacer un despliegue de contenedores de una forma mas organizada y para evitar problemas de solapamiento de direcciones ip con alguna direccion de red existente dentro del servidor, se va a crear una red de tipo bridge en docker, utilizando un rango de ips que no se encuentre en uso en la red del servidor.

```bash
docker network create -d bridge --subnet 10.240.1.0/24 --gateway 10.240.1.254 cluster-datos
```

la red se llamara "clsuter-datos" y tendra asociada una ip de red con el siguiente CIDR: 10.240.1.0/24, ademas, se asigna una puerta de enlace con la ip: 10.240.1.254

## Despliegue base de datos mysql

Para el despliegue de la base de datos mysql, se va a utilizar la imagen oficial de mysql en su ultima version, para ello se tiene destinado el archivo docker-compose.yml, el cual se encuentra en el directorio "mysql".

```yaml
services:
  mysql:
    image: mysql:latest
    env_file:
      - .env
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    container_name: mysql-db-1
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - cluster-datos
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1GB
      restart_policy:
        condition: unless-stopped
    logging:
      driver: "journald"
networks:
  cluster-datos:
    external: true
volumes:
  mysql_data:
```

Para utilizar las mejores practicas en cuanto a seguridad, se utilziaran variables de entorno para las contraseñas y los usuarios que utilizara la base de datos, para ello se debe crear un archivo llamado ".env" en el directorio "mysql" con el siguiente contenido:

```text
MYSQL_ROOT_PASSWORD="contraseña a utilizar"
MYSQL_DATABASE=bdnegocio
MYSQL_USER=santi
MYSQL_PASSWORD="contraseña a utilizar"
```

NOTA: en este archivo usted debe reemplazar "contraseña a utilizar" y los nombres de usuario por los que usted requiera, ademas de hacerlo preferiblemente una vez clonado el repositorio y se encuentre en el servidor en donde se va a desplegar el cluster. Si por el contrario no se requiere utilizar las variables de entorno para las contraseñas y usted solo requiere poner las contraseñas "hardcodeadas" en el archivo docker-compose.yml, puede hacerlo sin problemas y se evita la creacion del archivo ".env".


Por ultimo, para lanzar este docker compose, se debe estar ubicado en el directorio "mysql" y ejecutar el siguiente comando:

```bash
docker compose up -d
```

# APACHE AIRFLOW

se deben tener creadas las carpetas "dags","logs","config","plugins" en un directorio llamado "airflow".

mysql+mysqlconnector://root:Santiago.Meneses2025.*@mysql-db-1:3306/airflow

airflow-init-1     |   File "/home/airflow/.local/bin/airflow", line 5, in <module>
airflow-init-1     |     from airflow.__main__ import main
airflow-init-1     |   File "/home/airflow/.local/lib/python3.9/site-packages/airflow/__init__.py", line 74, in <module>
airflow-init-1     |     settings.initialize()
airflow-init-1     |   File "/home/airflow/.local/lib/python3.9/site-packages/airflow/settings.py", line 790, in initialize
airflow-init-1     |     configure_orm()
airflow-init-1     |   File "/home/airflow/.local/lib/python3.9/site-packages/airflow/settings.py", line 483, in configure_orm
airflow-init-1     |     engine = create_engine(SQL_ALCHEMY_CONN, connect_args=connect_args, **engine_args, future=True)
airflow-init-1     |   File "<string>", line 2, in create_engine
airflow-init-1     |   File "/home/airflow/.local/lib/python3.9/site-packages/sqlalchemy/util/deprecations.py", line 375, in warned
airflow-init-1     |     return fn(*args, **kwargs)
airflow-init-1     |   File "/home/airflow/.local/lib/python3.9/site-packages/sqlalchemy/engine/create.py", line 544, in create_engine
airflow-init-1     |     dbapi = dialect_cls.dbapi(**dbapi_args)
airflow-init-1     |   File "/home/airflow/.local/lib/python3.9/site-packages/sqlalchemy/dialects/mysql/mysqlconnector.py", line 129, in dbapi
airflow-init-1     |     from mysql import connector
airflow-init-1     | ModuleNotFoundError: No module named 'mysql'