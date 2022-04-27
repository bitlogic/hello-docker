# Docker Compose 

![logo](docker-compose-logo2.png)
## What is Docker Compose? :books:

 - Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services.  

 - The Compose file is a YAML file defining services, networks, and volumes for a Docker application.

 - Compose works in all environments, production, staging, development, testing, as well as CI workflows.

 - With a single command, you create and start all the services (containers) from your configuration.

---

## Docker Compose is a 3 Steps Process :trident:

1. Define you app's environment with Dockerfile to after create the services with containers :whale:

2. Define the services that make up your app in Docker Compose file :ok_hand:

3. Run the CLI:
    
    ```bash
    $ docker-compose up
    ```

4. Lets grab a coffee :coffee:  

---
## Building Blocks of Docker Compose :whale:

- Services :heavy_check_mark:
- Volumes :heavy_check_mark:
- Networking :heavy_check_mark:

#### A Sample Docker Compose File:

```YAML
version: "3.9"

services:
  web:
    image: app-py:latest
    ports:
      - "8000:80"

  redis:
    image: redis:alpine
```
This Compose file defines two services: **web** and **redis**.

The **web** service uses an image that’s built from the Dockerfile in the local directory.  It then binds the container and the host machine to the exposed port, 8000. This example service uses the default port for the web server, 80.

The **redis** service uses a public Redis image pulled from the Docker Hub registry.

## Run your app with Compose :runner:

```bash
$ docker-compose up                     
[+] Running 2/0
 ⠿ Container app-python-redis-1  Created                                                                                                                                                                                                 0.0s
 ⠿ Container app-python-web-1    Created                                                                                                                                                                                                 0.0s
Attaching to app-python-redis-1, app-python-web-1
app-python-redis-1  | 1:C 27 Apr 2022 15:27:41.134 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
app-python-redis-1  | 1:C 27 Apr 2022 15:27:41.134 # Redis version=6.2.6, bits=64, commit=00000000, modified=0, pid=1, just started
app-python-redis-1  | 1:C 27 Apr 2022 15:27:41.134 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
app-python-redis-1  | 1:M 27 Apr 2022 15:27:41.135 * monotonic clock: POSIX clock_gettime
app-python-redis-1  | 1:M 27 Apr 2022 15:27:41.135 * Running mode=standalone, port=6379.
app-python-redis-1  | 1:M 27 Apr 2022 15:27:41.135 # Server initialized
app-python-redis-1  | 1:M 27 Apr 2022 15:27:41.135 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
app-python-redis-1  | 1:M 27 Apr 2022 15:27:41.135 * Ready to accept connections
app-python-web-1    |  * Serving Flask app "app" (lazy loading)
app-python-web-1    |  * Environment: production
app-python-web-1    |    WARNING: This is a development server. Do not use it in a production deployment.
app-python-web-1    |    Use a production WSGI server instead.
app-python-web-1    |  * Debug mode: off
app-python-web-1    |  * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)

```

Now, check in http://localhost:8000/ :wink:

Stop the application, either by running `docker-compose down` from within your project directory in the second terminal, or by hitting CTRL+C in the original terminal where you started the app.

## Environment variables in Compose :eyes:

there are different ways to add environment variables inside a compose, some are:

- It’s possible to use environment variables in your shell to populate values inside a Compose file

```bash
$ export TAG=2.5
```

```YAML
  web:
  image: "app-py:${TAG}"
```
- The ".env" file

```bash
$ cat .env
TAG=v1.5

$ cat docker-compose.yml
version: '3'
services:
  web:
    image: "app-py:${TAG}
```
- Using the “--env-file” option

```bash
$ docker-compose --env-file ./config/.env.dev up 
```
- Set environment variables in containers

```YAML
  web:
    environment:
      - DEBUG=1
```

- Pass environment variables to containers

```YAML
  web:
    environment:
      - DEBUG
```
The value of the DEBUG variable in the container is taken from the value for the same variable in the shell in which Compose is run.

- The “env_file” configuration option

```YAML
  web:
  env_file:
    - web-variables.env
```
- Set environment variables with ‘docker-compose run’

```bash
$ docker-compose run -e DEBUG=1 web python console.py
```

When you set the same environment variable in multiple files, here’s the priority used by Compose to choose which value to use:

1. Compose file
2. Shell environment variables
3. Environment file
4. Dockerfile
5. Variable is not defined

## Networking in Compose

By default Compose sets up a single network for your app. Each container for a service joins the default network and is both reachable by other containers on that network, and discoverable by them at a hostname identical to the container name :heart_eyes: .

>note: Your app’s network is given a name based on the “project name”, which is based on the name of the directory it lives in. You can override the project name with either the --project-name flag or the COMPOSE_PROJECT_NAME environment variable. :yum:


For example, suppose your app is in a directory called app-python, and your docker-compose.yml looks like this:

```YAML
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres
    ports:
      - "8001:5432"
```
When you run docker-compose up, the following happens:

1. A **network** called app-python_default is created.
2. A container is created using web’s configuration. It joins the network app-python_default under the name **web**.
3. A container is created using db’s configuration. It joins the network app-python_default under the name **db**.

### Use a pre-existing network 

If you want your containers to join a pre-existing network, use the `external` option:

```YAML
services:
  # ...
networks:
  default:
    external:
      name: my-pre-existing-network
```
or also:

```YAML
  massive-admission-api:
    image: 930137440523.dkr.ecr.sa-east-1.amazonaws.com/massive-admission-api:latest
    environment:
      - OAUTH_HOST=${OAUTH_HOST}
      - UMS_URL=${UMS_URL}
      - ACADEMIC_OFFER_URL=${ACADEMIC_OFFER_URL}
      - ADMISSION_API_URL=${ADMISSION_API_URL}
      - AFIP_URL=${AFIP_URL}
      - BOOTSTRAP_SERVER=${BOOTSTRAP_SERVER}
      - OAUTH_URL=${OAUTH_URL}
      - CLIENT_SECRETS_MASSIVE=${CLIENT_SECRETS_MASSIVE}
    networks:
      - algarrobo_alga

networks:
  algarrobo_alga:
    external: true
```