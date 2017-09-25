

 :warning: **THIS SECTION IS STILL IN PROGRESS** :warning:



# Docker swarm

Docker's swarm mode allows you to go all serious about large scale, highly available docker environments. It basically lets you handle a cluster of machines as a single docker daemon, with automatic failover, container scheduling, routing and tons of other goodies.

This last section will walk you through creating a simple swarm cluster and the basic concepts. Do be noted that understanding docker swarm in its fullest is *way* beyond the scope of this guide. In any case, let's cut to the chase, shall we.

## Get some nodes

In order to have a docker swarm going, you'll need a machine cluster, for which you'll need machines. Quickest, coolest way is by using [`play-with-docker`](http://play-with-docker.com/) to try it online. If you'd rather try it locally, you'll need [`docker-machine`](https://docs.docker.com/machine/) and [`Virtualbox`](https://www.virtualbox.org/). If you're running `Docker for mac` or `Docker for windows` you probably already have it installed; `Linux` users should get `docker-machine` separately.

The main difference is how long it'll take you to have the swarm ready. If you're just trying it out, the online route is probably what you want. If you'd like your swarm to be persistent or try some extra stuff you'll want to use the local approach (it may get resource intensive).

Pick your poison and choose one of the following:

#### Online sandbox

For the sake of simplicity, in this section we are going to use the play with docker environment.

Browse to [`play-with-docker`](http://play-with-docker.com/) and create three nodes with the "+ ADD NEW INSTANCE" button.


### Get swarmin'

Let's get this swarm started. Grab a hold of the manager node host IP. In `play-with-docker` you'll see it in node's terminal prompt; if running locally with `docker-machine` it's usually `192.168.99.100`

```
docker swarm init --advertise-addr <manager node's ip>
```

This set the node's docker daemon to swarm mode and output the `swarm join` command you'll need for other nodes to join this swarm. Copy it to your clipboard; you'll need it soon.

Verify the swarm status by doing.

```
docker info
```

You can see under `Swarm` the swarm state.

See the swarm nodes with:

```
docker node ls
```

Now let's make both worker nodes join the swarm cluster: run the command you just copied into your clipboard inside each of the worker nodes (if running locally, `docker-machine ssh` into both workers and `exit` back to your terminal)

See now that your swarm is 3 nodes big:

```
docker node ls
```

You now have a 3-node working swarm cluster 😎


## Final words

These are just the docker basics, you'll learn a lot more by addressing real-life scenarios, so get hackin'

Hopefully this repo will encourage you to [do some more research on your own](https://docs.docker.com) and make docker part of your development toolkit and prod pipelines.

Please feel free to update/fix anything that you see improvable in this repo, and if you liked it spread the word.

Thanks for reading 🙇