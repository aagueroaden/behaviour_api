# Behaviour API

Api for logging what an user does in the platform, where does he clicks, etc.

it has a module called mvp_logging:

it is the minimun viable product, where we will test the concept of the api works or not(
    After that we should use the behaviour module only and delete the mvp_logging)

## Installation

### Develop with compose

build and run

```sh
docker compose -f docker-compose.local.yaml up --build -d
```

restart

```sh
docker compose -f docker-compose.local.yaml restart
```

stop

```sh
docker compose -f docker-compose.local.yaml stop
```

### As a service

here you dont have a database, you will need one, postgres:15 will do the trick
and add the env variables to a .env file

create a virtual enviroment using python3.12

install the dependencies

```sh
pip3 install -r requirements.txt
```

then run

```sh
fastapi dev app/main.py
```
