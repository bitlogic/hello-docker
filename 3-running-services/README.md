# Docker Services

## About services
In a distributed application, different pieces of the app are called “services.” For example, if you imagine a video sharing site, it probably includes a service for storing application data in a database, a service for video transcoding in the background after a user uploads something, a service for the front-end, and so on.

Services are really just “containers in production.” A service only runs one image, but it codifies the way that image runs—what ports it should use, how many replicas of the container should run so the service has the capacity it needs, and so on. Scaling a service changes the number of container instances running that piece of software, assigning more computing resources to the service in the process.

Luckily it’s very easy to define, run, and scale services with the Docker platform.


## Swarm Init 

To be able to deploy services we need to initialize the `swarm cluster`. For doing so, execute the following command: 

```
docker swarm init
```

You can check that the cluster has been initialized with the following.

```
docker node ls
```

Since this is a single node cluster, the docker host is going to be the manager of the cluster. Next sections we are going to be setting up a more complex, multi-node, swarm deployment. 

## Creating and managing your first service

On this part we are going to be creating services from the command line. On real world, scenarios the more common way for defining services is via a `docker-compose.yml` file. We are going to to see that on next section.

So, to start just check if there is any service running.

```
docker service ls
```

Now, lets start having fun by creating our first service. We are going to be creating a service with the image that we created in previous section.

```
docker service create --name pinger --replicas=1 alpine ping docker.com
```

See some info about the service by doing

```
docker service inspect --pretty pinger
```

To check the status of the containers running you can execute the following:

```
docker service ps pinger
```

You can see in which node it's running. Now let's scale the service by getting more replicas of it (each replica is a container):

```
docker service scale pinger=5

docker service ls
```

;-) Cool! Now we have 5 replicas of the service! 

Now lets check the **logs** from all the instances of the service.

```
docker service logs -f pinger
```

On this section we have created very simple services using the `docker service` command. On next section we are going to get more serious and use a `docker-compose.yml` file to [create a stack](https://github.com/bitlogic/hello-docker/tree/master/4-docker-stacks).

