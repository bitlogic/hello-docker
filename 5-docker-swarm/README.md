# Docker swarm

Docker's swarm mode allows you to go all serious about large scale, highly available docker environments. It basically lets you handle a cluster of machines as a single docker daemon, with automatic failover, container scheduling, routing and tons of other goodies.

This last section will walk you through creating a simple swarm cluster and the basic concepts. Do be noted that understanding docker swarm in its fullest is *way* beyond the scope of this guide. In any case, let's cut to the chase, shall we.

## Setup the Cluster

### Get some nodes

In order to have a docker swarm going, you'll need a machine cluster, for which you'll need machines. Quickest, coolest way is by using [`play-with-docker`](http://play-with-docker.com/) to try it online. If you'd rather try it locally, you'll need [`docker-machine`](https://docs.docker.com/machine/) and [`Virtualbox`](https://www.virtualbox.org/). If you're running `Docker for mac` or `Docker for windows` you probably already have it installed; `Linux` users should get `docker-machine` separately.

The main difference is how long it'll take you to have the swarm ready. If you're just trying it out, the online route is probably what you want. If you'd like your swarm to be persistent or try some extra stuff you'll want to use the local approach (it may get resource intensive).

For the sake of simplicity, in this section we are going to use the play with docker environment.

Browse to [`play-with-docker`](http://play-with-docker.com/) and create three nodes with the "+ ADD NEW INSTANCE" button.


### Start the master

Let's get this swarm started. Now choose which is going to be your manager node and execute the following command:

```
$ docker swarm init --advertise-addr <manager node's ip>

Swarm initialized: current node (v51je0ntr6h0o92bbmvuka34o) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-03hh4r65g8urdusbqnlfeakp6fskg17frbb92kx1v86oa3mwsb-duninzcwphu4cvnzeh5vbmghe 10.0.203.3:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

> This set the node's docker daemon to swarm mode and output the `swarm join` command you'll need for other nodes to join this swarm. Copy it to your clipboard; you'll need it soon.


### Add the Workers

Now let's make both worker nodes join the swarm cluster: run the command you just copied into your clipboard inside each of the worker nodes 

```
docker node ls
```

You now have a 3-node working swarm cluster 😎


## Swarming

### Our first swarm service 

We are going to start by creating a service:

```
$ docker service create --replicas 5 -p 80:80 --name web nginx:1.12
```

Now lets check how have they have been scheduled
```
$ docker service ps web
```

### Scaling Up and Scaling Down

This is done via the docker service scale command. We currently have 5 containers running. Let us bump it up to 8 as shown below by executing the command on the manager node.

```
$ docker service scale web=8
web scaled to 8
```

Now lets check that we have the service scaled up
```
$ docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE     PORTS
x7ag3q8hwxi0        web                 replicated          8/8                 nginx:1.12     *:80->80/tcp
```

You can check in which nodes the containers are running with the `docker service ps` command.


### Inspecting Nodes

You can inspect the nodes anytime via the docker node inspect command.
For example if you are already on the node (for example manager) that you want to check, you can use the name self for the node.

```
$ docker node inspect --pretty self
```

Or if you want to check up on the other nodes, give the node name. For e.g.
```
$ docker node inspect --pretty node2
```

Another useful way to check what is running on each node is `docker node ps`. e.g.:

```
$ docker node ps node2
```

### Drain a Node

If the node is ACTIVE, it is ready to accept tasks from the Master i.e. Manager. For e.g. we can see the list of nodes and their status by firing the following command on the manager node.

```
$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAG
ER STATUS
v51je0ntr6h0o92bbmvuka34o *   node1               Ready               Active              Leade
r
wpwocg35s2umag99w8wqctqgc     node2               Ready               Active
43rdiv13nznic9bm1ml5fgzwn     node3               Ready                Active
$
```

As you can see that their AVAILABILITY is set to READY. When the node is active, it can receive new tasks:
* during a service update to scale up
* during a rolling update
* when you set another node to Drain availability
* when a task fails on another active node

But sometimes, we have to bring the Node down for some maintenance reason. This meant by setting the Availability to Drain mode. Let us try that with one of our nodes.
Lets asume that we want to stop node2 

```
$ docker node update --availability drain node2
```

Now check how the node2 have been drained and all their containers have been moved to other nodes. 

```
$ docker service ps web
```



### Rolling Updates

This is straight forward. In case you have an updated Docker image to roll out to the nodes, all you need to do is fire an service update command.

```
$ docker service update --image nginx:1.13 web
```

Now lets check the rolling update status of the service with `docker service ps`

```
$ docker service ps web
```

### Tango Down 

OK, now lets see what happens if one of the `active` and `available` node crash or is shut down by accident.

Let's kill one of the worker nodes and see how docker re-schedules its containers: in `play-with-docker` just hit the delete button in any of the worker nodes. 

You can now check the status of your service as usual by executing the following:

```
$ docker service ps web
``` 

Magic! Containers have been respawned in other nodes (if possible) so the service keep working with minimal impact by the node being shut down. 



## Final words

These are just the docker basics, you'll learn a lot more by addressing real-life scenarios, so get hackin'

Hopefully this repo will encourage you to [do some more research on your own](https://docs.docker.com) and make docker part of your development toolkit and prod pipelines.

Please feel free to update/fix anything that you see improvable in this repo, and if you liked it spread the word.

Thanks for reading 🙇
