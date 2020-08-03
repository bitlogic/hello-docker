# Docker Containers

## Hello-World

The most fundamental part of `Docker` are *containers*. There's a lot to say about them, but let's just run one:

```
$ docker container run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

Easy, right? Let's take a look at what has just happened behind the scenes...

 1. The **Docker client** contacted the **Docker daemon**.
 2. The **Docker daemon** pulled the "hello-world" image from the **Docker Hub**.
 3. The **Docker daemon** created a new **container** from that image which runs the
    executable that produces the output you are currently reading.
 4. The **Docker daemon** streamed that output to the **Docker client**, which sent it
    to your terminal.


> Whoa!! So this means that the whole **Docker Platform** is correctly setup and working.


Now lets start exploring and check the container 

```
$ docker container ps
```

🤔 not there... Let's add the `-a` flag

```
$ docker container ps -a
```

😀 there you are! The -a option list not only the `running` containers but also the containers that have been finished.  This might become handy if you want to examine them.



## Running a Container

Now let's get serious. Let's run a full-fledged Ubuntu container:

First we are going to pull a *specific* Ubuntu docker image from the registry.

```
$ docker pull ubuntu:20.04
```

🤔 it looks like it downloaded something, but not sure what...

```
$ docker images
```

As you can see, now we have the ubuntu:14.04 image in our host and we can create our container.


```
$ docker container run -it ubuntu:20.04
```

Cool, we're inside the container! `-it` specifies you want to go into the interactive mode (TBH, `i` is interactive and `t` is for docker to allocate a pseudo TTY interface for the interaction)

Can you guess What will happen if you delete the any important file inside the container? (e.g. :warning: delete the "ls" binary... )

After toying around just `exit`. 


> :bulb: **Remember:** What happen in a container, stays in a container.



So the way containers work is that there is one single main process that gets assigned `pid 1`, which runs as the containers starts, and as soon as that process exits, the container is stopped, even if there were other processes running inside of it.

You may also have noticed that the first time you ran `docker run ubuntu:14.04` it took a while, but the second time it was immediate. What really happened is that docker tried to run a container based on the `ubuntu:14.04` image, and since it didn't have it locally, it pulled it from the public repository. 


## Running, detaching and attaching to containers

Let's run a mongo database! And with a cute name.

```
$ docker run --name db mongo
```

🤔 but I don't want to be attached to the output... Just CTRL+c to quit and let's remove that container.

```
$ docker rm db
```

Now let's run a new mongo container, but in the background with the `-d` flag (`d` as in `detach`).

```
$ docker run --name db -d mongo
```

Now let's check out the mongo database. First you need to sort-of-`ssh` into the container. You don't actually use `ssh`, instead you can _execute_ a command with the interactive mode, like so:

```
$ docker exec -it db mongo
```

Now you're running the `mongo` command in the `db` container. Toy around and then CTRL+c to quit.

If you now do `docker ps` you'll notice the `db` container is still running. It didn't stop because the main process, the `mongo` database process (with `pid 1`), is still running. The process you killed by quitting was just the mongo shell.


## Exposing containers

Now let's run a web app in _another_ container.

```
$ docker container run --name webapp -d -P seqvence/static-site
```

The -P command is basically making docker to automatically bind the internal port that the container is exposing to some available port in your host.

So, lets check if the app is running and which ports is exposing.

```
$ docker container ps
```

As you can see under `PORTS`, it seems the app *is* listening in port 80, but... 😮 Of course! That's just the container's _internal_ port! 

By passing the `-P` parameter to the docker run command, docker has automatically binded an external port to expose the service. 

Check the outcome of the command and try to connect via browser to \\localhost:{->binded port}


Congratulations! You now have a web app runing inside a container and being exposed externally so users can enjoy it. 😎 🐳


## Docker Logs

One of the benefits from docker is that they provide some standard interface for operating applications inside containers.  So lets check how to see the logs of an app running inside a cointainer.

> To be able to see the logs, the app inside the container should be sending the logs to  STDOUT and STDERR

So, first lets start a container in background.

```
$ docker logs webapp
```

## Cleaning up containers

OK,  we know how to start multiple containers so now its time to stop them. 

First, check which containers are running with 

```
$ docker container ps
```

Now to stop a container you can do any of the following. 

``` 
$ docker container stop {container id | container name}
```

Great! This command has stopped the containers from running but we still have the containers files in the host. If you want a complete cleanup and remove everything, you should go further and execute the following:

``` 
$ docker container prune
```
The `prune` command will delete all containers so if you check with `docker container ps -a` you will see that there are no more containers on your host.

#### Bonus :trollface: :trollface: :trollface:
If you need to look like a **hollywood hacker** with `Docker` you can just run the following command:

```
$ docker container run -it jturpin/hollywood hollywood
```
:grimacing:



So, That's a wrap for the basics. :bowtie: Let's [move on to the next section](https://github.com/bitlogic/hello-docker/tree/master/2-building-images). :punch:
