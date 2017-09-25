# Docker Stacks

A stack is a group of interrelated services that share dependencies, and can be orchestrated and scaled together. A single stack is capable of defining and coordinating the functionality of an entire application (though very complex applications may want to use multiple stacks).


## Our first Single Service Stack

The way to define stacks is via a `docker-compose.yml` file. This file defines how Docker Stack  should behave in production.

In the root of the project, you will find a `docker-compose.yml` file describing our first service. 

```YAML
version: "3.3"
services:
  # We only have one service so far that we will name "web"
  web:
    # Image name should be the same that we created on previous section.
    image: hello-docker
    # On this part we define the strategy for scheduling containers. 
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

So, this `hello-service.yml` file tells `Docker` to do the following:

* Use the image we created in previous section **hello-docker**
* Run 3 instances of that image as a service called web, limiting each one to use, at most, 10% of the CPU (across all cores), and 50MB of RAM.
* Immediately restart containers if one fails.
* Map port 80 on the host to web’s port 80.
* Instruct web’s containers to share port 80 via a load-balanced network called webnet. (Internally, the containers themselves will publish to web’s port 80 at an ephemeral port.)
* Define the webnet network with the default settings (which is a load-balanced overlay network).

Now let’s run it. Go to the `./4-docker-stacks` folder of the project and execute the following command: 

```
$ docker stack deploy -c hello-service.yml hello-service
```

Our single service stack is running 3 container instances of our deployed image on one host. 

You can run `curl http://localhost` several times in a row, or go to that URL in your browser and hit refresh a few times. Either way, you’ll see the container ID change, demonstrating the load-balancing; with each request, one of the 5 replicas is chosen, in a round-robin fashion, to respond.

Magic ✨🐳


Now lets delete the **stack** 
```
$ docker stack rm hello-service
```

## Multi-Service Stacks

Now lets gets real and deploy a multi service (container) stack. 

We are going to add to the `hello-docker` service a visualizer and `redis` to persist the data. We should now be able to count the visitors of our service. ;-) 

In this same folder you will find the `hello-stack.yml' file with the following content.
```YAML
version: "3"
services:
  web:
    image: hello-docker
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
    ports:
      - "80:80"
    networks:
      - webnet
  visualizer:
    image: dockersamples/visualizer:stable
    ports:
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      placement:
        constraints: [node.role == manager]
    networks:
      - webnet
  redis:
    image: redis
    ports:
      - "6379:6379"
    deploy:
      placement:
        constraints: [node.role == manager]
    networks:
      - webnet
networks:
  webnet:
```

As you can see, we are adding 2 services `redis` and `visualizer` toghether with their policies and constraints.

Let's start the stack and see what happen:

```
$ docker stack deploy -c hello-stack.yml hello
```

Magic ✨🐳

Magic ✨🐳

Magic ✨🐳

```
$ docker service ls
```

You should see something like the following:
```
ID                  NAME                MODE                REPLICAS            IMAGE                             PORTS
i08fo6eilog8        hello_redis         replicated          1/1                 redis:latest                      *:6379->6379/tcp
nch7igvp6l16        hello_visualizer    replicated          1/1                 dockersamples/visualizer:stable   *:8080->8080/tcp
px5kj7d22t8x        hello_web           replicated          3/3                 hello-docker:latest               *:80->80/tcp
```


So now we have a `stack` with 3 services! A web service with 3 instances running and being load balanced automatically by docker, a `redis` service to persist the visitors to the site and the `visualizer` to see how are the service deployed. 

> :shipit: Now You can **visually** see the services deployed by connecting to the `visualizer` service browsing to [localhost:8080]

> :shipit:  If you are a console nerd, try the following command (tested in MacOS) to check how the web service is load balanced and the visit history is persisted.

```
$ while sleep 1; do curl localhost && echo ""; done
```

Now, Lets have a little more fun and scale the web service with the following command:
```
$ docker service scale hello_web=5
```

Now stop a few containers and see what happen
```
$ docker stop [container id | name]
```

You now have a multi-service resilient application running in a docker swarm ✨

To stop the stack execute the following:
```
docker stack rm hello
```

Now lets get serious and distribute the application in multiple nodes with [docker swarm](https://github.com/bitlogic/hello-docker/tree/master/5-docker-swarm).