# Docker basics


## Containers

The most fundamental part of `Docker` are *containers*. There's a lot to say about them, but let's just run one:

```docker
docker container run hello-world
```

If you can see `Hello from Docker` on the screen, it means that Docker took the following steps:

 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.


Easy, right? Let's take a look at that container

```
docker container ps
```

🤔 not there... Let's add the `-a` flag

```
docker container ps -a
```

😀 there you are! The -a option list not only the `running` containers but also the containers that have been finished.  This might become handy if you want to examine them.



Now let's get serious. Let's run a full-fledged Ubuntu Linux:

```
docker container run ubuntu:14.04
```

(notice how we specified a version; more on that to come)

🤔 it looks like it downloaded something, but not sure what...

```
docker ps -a 
```

So it stops after it runs? Let's try something else:

```
docker container run -it ubuntu:14.04
```

Cool, we're inside the container! `-it` specifies you want to go into the interactive mode (TBH, `i` is interactive and `t` is for docker to allocate a pseudo TTY interface for the interaction)

Can you guess What will happen if you delete the any important file inside the container? 

After toying around just `exit`. Let's give it another look:

```
docker ps -a
```

So the way containers work is that there is one single main process that gets assigned `pid 1`, which runs as the containers starts, and as soon as that process exits, the container is stopped, even if there were other processes running inside of it.

You may also have noticed that the first time you ran `docker run ubuntu:14.04` it took a while, but the second time it was immediate. What really happened is that docker tried to run a container based on the `ubuntu:14.04` image, and since it didn't have it locally, it pulled it from the public repository. Which brings us to:


## Images

_Images_ are the templates docker uses to create containers from. If you're familiar with [Object Oriented Programming](https://en.wikipedia.org/wiki/Object-oriented_programming) you may (sort of) think of images as _classes_ and containers as _instances_.

Check which images you have in your local repository by doing:

```
docker images
```

Let's try and get another image

```
docker pull mongo
```
This last command _pulled_ an image named `mongo` from [the public docker repository](https://hub.docker.com) to your local repository. This is very similar to what you achieve with `git pull` from a public `git` repository.

Cool! So now we have an image we didn't create a container from.

That's a wrap for the basics. Let's [move on to the next section](https://github.com/bitlogic/hello-docker/tree/master/1-running-containers).
