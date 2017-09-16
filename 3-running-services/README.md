# Docker Services


## About services
In a distributed application, different pieces of the app are called “services.” For example, if you imagine a video sharing site, it probably includes a service for storing application data in a database, a service for video transcoding in the background after a user uploads something, a service for the front-end, and so on.

Services are really just “containers in production.” A service only runs one image, but it codifies the way that image runs—what ports it should use, how many replicas of the container should run so the service has the capacity it needs, and so on. Scaling a service changes the number of container instances running that piece of software, assigning more computing resources to the service in the process.

Luckily it’s very easy to define, run, and scale services with the Docker platform – just write a `docker-compose.yml` file.



## Swarm Init 

To be able to deploy services we need to initialize the `swarm cluster`. For doing so, execute the following command: 

```
docker swarm init
```

You can check that the cluster has been initialized with the following.

```
docker node ls
```

Since this is a single node cluster, the docker host is going to be the manager of the cluster. Next section we are going to be setting up a more complex, multi-node, swarm deployment. 

## You first service

A docker-compose.yml file is a YAML file that defines how Docker containers should behave in production.

In the root of the proyect, you will find a `docker-compose.yml` file describing our first service. 

```
version: "3"
services:
  web:
    image: hello-docker
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
      restart_policy:
        condition: on-failure
    ports:
      - "80:80"
    networks:
      - webnet
networks:
  webnet:
```

This docker-compose.yml file tells Docker to do the following:

* Use the image we created in previous section `hello-docker` 
* Run 3 instances of that image as a service called web, limiting each one to use, at most, 10% of the CPU (across all cores), and 50MB of RAM.
* Immediately restart containers if one fails.
* Map port 80 on the host to web’s port 80.
* Instruct web’s containers to share port 80 via a load-balanced network called webnet. (Internally, the containers themselves will publish to web’s port 80 at an ephemeral port.)
* Define the webnet network with the default settings (which is a load-balanced overlay network).


Now let’s run it. Go to the root folder of the project and execute the following command: 

```
docker stack deploy -c docker-compose.yml hello-docker-stack
```

Magic ✨🐳

Our single service stack is running 3 container instances of our deployed image on one host. Let’s investigate.

Get the service ID for the one service in our application:

```
docker service ls
```

Docker swarms run tasks that spawn containers. Tasks have state and their own IDs:
```
docker service ps <service>
```

You can run `curl http://localhost` several times in a row, or go to that URL in your browser and hit refresh a few times. Either way, you’ll see the container ID change, demonstrating the load-balancing; with each request, one of the 5 replicas is chosen, in a round-robin fashion, to respond.

Lets get crazy and scale up our service.

```
docker service scale hello-docker-stack_web=5
hello-docker-stack_web scaled to 5
```

Now check the status with `docker service` and `docker ps`

Finally, lets take the app down with docker stack rm:

```
docker stack rm hello-docker-stack_web
```

Now let's get serious, and [unleash the swarm](https://github.com/bitlogic/hello-docker/tree/master/4-docker-swarm).
