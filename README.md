# ingenieria_de_datos


este reposisorio se creo con el fin de implementar un cluster de spark utilizando Docker, ademas tambien, se lanza una base de datos mysql.


Inicialmente se van a crear las variables de entorno que almacenaran las contraseñas utilizadas para los diferentes servicios. Para ello, debemos añadir las variables de entorno en el archivo .bashrc o .bash_profile, utilizando algun editor de texto como nano o vim.
```bash
nano ~/.bashrc
```
se añaden las variables a lo ultimo del archivo y se ponen las contraseñas que deseen. En mi caso, utilizo la variable de entorno "MYSQLPASS".

Luego de esto, se guarda el archivo y se ejecuta el siguiente comando para que las variables de entorno se activen.

```bash
source ~/.bashrc
```

se verifica que la variable de entorno se haya creado correctamente con el siguiente comando:

```bash
echo $MYSQLPASS
```

## creacion de una red tipo bridge en docker


Con el fin de hacer un despliegue de contenedores de una forma mas organizada y para evitar problemas de solapamiento de direcciones ip con alguna direccion de red existente dentro del servidor, se va a crear una red de tipo bridge en docker, utilizando un rango de ips que no se encuentre en uso en la red del servidor.

```bash
docker network create -d bridge --subnet 10.240.1.0/24 --gateway 10.240.1.254 cluster-datos
```

la red se llamara "clsuter-datos" y tendra asociada una ip de red con el siguiente CIDR: 10.240.1.0/24, ademas, se asigna una puerta de enlace con la ip: 10.240.1.254

## Despliegue base de datos mysql

Para el despliegue de la base de datos mysql, se va a utilizar la imagen oficial de mysql en su ultima version, para ello se tiene destinado el archivo docker-compose.yml, el cual se encuentra en el directorio "mysql".

```yaml
version: '1'
services:
  bd-mysql:
    image: mysql:latest
    environment:
      MYSQL_DATABASE: bdnegocio
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
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

Por ultimo, para lanzar este docker compose, se debe estar ubicado en el directorio "mysql" y ejecutar el siguiente comando:

```bash
MYSQL_ROOT_PASSWORD=$MYSQLPASS docker compose up -d
```


