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

en este archivo usted debe reemplazar "contraseña a utilizar" por la contraseña que desea utilizar para el usuario root y el usuario santi.


Por ultimo, para lanzar este docker compose, se debe estar ubicado en el directorio "mysql" y ejecutar el siguiente comando:

```bash
docker compose up -d
```


