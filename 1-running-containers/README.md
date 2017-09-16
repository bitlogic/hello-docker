# Containers

## Running, detaching and attaching to containers

Let's run a mongo database! And with a cute name.

```
docker run --name db mongo
```

🤔 but I don't want to be attached to the output... Just CTRL+c to quit and let's remove that container.

```
docker rm db
```

Now let's run a new mongo container, but in the background with the `-d` flag (`d` as in `detach`).

```
docker run --name db -d mongo
```

Cool! Now let's check out the mongo database. First you need to sort-of-`ssh` into the container. You don't actually use `ssh`, instead you can _execute_ a command with the interactive mode, like so:

```
docker exec -it db mongo
```

Now you're running the `mongo` command in the `db` container. Toy around and then CTRL+c to quit.

If you now do `docker ps` you'll notice the `db` container is still running. It didn't stop because the main process, the `mongo` database process (with `pid 1`), is still running. The process you killed by quitting was just the mongo shell.


Now let's run a web app in _another_ container.

```
docker container run --name webapp -d -P seqvence/static-site
```

First, lets check if the app is running and which ports is exposing.

```
docker container ps
```


Now check if it did something:

```
docker logs webapp
```

It seems the app is listening on port 80. Let's browse to `localhost:3000`

🤔 it doesn't reach the app... Let's look closer:

```
docker ps -a
```

As you can see under `PORTS`, it seems the app *is* listening in port 80, but... 😮 Of course! That's just the container's _internal_ port! 

By passing the `-P` parameter to the docker run command, docker has automatically binded an external port to expose the service. 

```
docker container ps
```

Check the outcome of the command and try to connect via browser to \\localhost:{->binded port}


😎🐳

Ok, now you're ready to [learn how to work with images](https://github.com/bitlogic/hello-docker/tree/master/2-building-images).
