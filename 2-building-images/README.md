# Images

In this section we are going to be managing, defining and building our own images.

## Pulling Images

**Images** are the templates docker uses to create containers from. If you're familiar with [Object Oriented Programming](https://en.wikipedia.org/wiki/Object-oriented_programming) you may (sort of) think of images as _classes_ and containers as _instances_.

Check which images you have in your local repository by doing:

```Shell
$ docker images
```

Let's try and pull an image

```Shell
$ docker pull python:2.7-slim
```

This last command _pulled_ an image named `python` with "2.7-slim" tag from [the public docker repository](https://hub.docker.com) to your local host. This is very similar to what you achieve with `git pull` from a public `git` repository.

Cool! So now we have an image we didn't create a container from.


## Building Your First Image

A docker image is made of one or more layers. Each layer is built on top of the previous one and they're all immutable. This means you can't modify an existing layer, instead you create a new one made of changes from the previous layer. This is very similar to how `git`'s diff works.

To get a sample `Dockerfile` that we will use, clone this repo 
```
$ git clone https://github.com/bitlogic/hello-docker/

``` 

In that project's root dir, go to the "./2-building-images" folder. There you will find  a `Dockerfile` containing the following comands.

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the app code and dependencies file into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

 So go ahead and build it with the following command.

```Shell
$ docker build -t hello-docker .
```

If you pay attention to the output of the build, you will see that each instruction (`FROM`, `RUN`, etc.) in the `Dockerfile` generates a single, immutable layer.


Aaaaaand that's it! 🐳 You can check the new image with the following command.

```Shell
$ docker images
```

Now lets run the app that we have just build.

```
$ docker container run --name hello -d -P hello-docker 
```

Excellent!! Now we have hour `hello-docker` app working and runing in our host.
You can check the app working by conecting the browser to the `localhost:[port]`


Alternatively, you can check the app by using the `curl` command

``` 
$ curl http://localhost:[port]

<h3>Hello World!</h3><b>Hostname:</b> 8fc990912a14<br/><b>Visits:</b> <i>cannot connect to Redis, counter disabled</i>
```



## Understanding layers and leveraging the cache

Notice that if you run the `docker build` command again, it will take no time at all. This is because docker caches each layer and doesn't re-build them if the build context and layer creation command didn't change since the last build.

If you change the `FROM python:2.7-slim` line to `FROM python` so you try how it works with the latest `python` version and build it again

You'll see that all layers get rebuilt! This is because you changed the _base layer_; since all layers are just diffs from the previous one, by changing the base layer you invalidate the cache for all layers after it.

In your everyday development workflow, you don't want to reinstall all dependencies just because you changed a single source file, you would only want that if you changed code files.

> :bulb: So be careful with how the Docker file is defined and always try to put the more stable things at the beginning since the build time will be faster.


Now You may publish this image by using the command `docker push`, but you'll need an account in [`hub.docker.com`](https://hub.docker.com); you can do that later on your own. 





There's a lot more to say about images but now is time to [learn how to create services](https://github.com/bitlogic/hello-docker/tree/master/3-running-services)
