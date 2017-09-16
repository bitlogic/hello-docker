# Images


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


## Building images

A docker image is made of one or more layers. Each layer is built on top of the previous one and they're all immutable. This means you can't modify an existing layer, instead you create a new one made of changes from the previous layer. This is very similar to how `git`'s diff works.

In order to build an image, you will need a `Dockerfile`. Try the one for the web app image you've been using by `git clone`ing the `https://github.com/bitlogic/hello-docker/` public github repo.

In that project's root dir, there is a `Dockerfile` containing the comands to build our sample static app so go ahead and build the test-image.

Each instruction (`FROM`, `RUN`, etc.) in the `Dockerfile` generates a single, immutable layer.

```
docker build -t test-image .
```

Aaaaaand that's it! 🐳 You can check the new image with the following command.

```
docker images
```


## Understanding layers and leveraging the cache

Notice that if you run the same command again, it will take no time at all. This is because docker caches each layer and doesn't re-build them if the build context and layer creation command didn't change since the last build.

Now change the `FROM ubuntu:14.04` line to `FROM ubuntu:latest` so you try how it works with the latest `ubuntu` version and build it again

You'll see that all layers get rebuilt! This is because you changed the _base layer_; since all layers are just diffs from the previous one, by changing the base layer you invalidate the cache for all layers after it.

Now change the string message in line 5 and build again.

Faster, right? 😎

We now see that the base layer gets reused, but everything else gets re-done, including installing dependencies. In your everyday development workflow, you don't want to reinstall all dependencies just because you changed a single source file, you would only want that if you changed code files.

You may publish this image by using the command `docker push`, but you'll need an account in [`hub.docker.com`](https://hub.docker.com); you can do that later on your own. For now, let's [learn how to `docker-compose`](https://github.com/bitlogic/hello-docker/tree/master/3-docker-compose)
