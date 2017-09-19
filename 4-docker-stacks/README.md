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
Magic ✨🐳
Magic ✨🐳

Now lets delete the service 
```
docker service rm hello-service
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
      replicas: 5
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
    volumes:
      - ./data:/data
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
$ docker stack deploy -c hello-stack.yml hello-service
```





Let's kill one of the worker nodes and see how docker re-schedules its containers: in `play-with-docker` just hit the delete button in any of the worker nodes. If running locally just `docker-machine rm worker2`

Now `docker service ps pinger` repeatedly to see how some of the pop up in the other nodes automatically. How cool is that?

You now have a resilient, distributed application running in a docker swarm cluster ✨


Docker swarms run tasks that spawn containers. Tasks have state and their own IDs:
```
docker service ps <service>
```




