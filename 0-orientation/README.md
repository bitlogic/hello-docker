# Introduction
This section aims to explain some important docker concepts so the rest of the guideline can be more hands-on. 


## A brief explanation of containers
An image is a lightweight, stand-alone, executable package that includes everything needed to run a piece of software, including the code, a runtime, libraries, environment variables, and config files.

A container is a runtime instance of an image—what the image becomes in memory when actually executed. It runs completely isolated from the host environment by default, only accessing host files and ports if configured to do so.

Containers run apps natively on the host machine’s kernel. They have better performance characteristics than virtual machines that only get virtual access to host resources through a hypervisor. Containers can get native access, each one running in a discrete process, taking no more memory than any other executable.


## Containers vs. virtual machines

Consider this diagram comparing virtual machines to containers:

Virtual Machine diagram
Virtual machine stack example

Virtual machines run guest operating systems—note the OS layer in each box. This is resource intensive, and the resulting disk image and application state is an entanglement of OS settings, system-installed dependencies, OS security patches, and other easy-to-lose, hard-to-replicate ephemera.

Container diagram
Container stack example

Containers can share a single kernel, and the only information that needs to be in a container image is the executable and its package dependencies, which never need to be installed on the host system. These processes run like native processes, and you can manage them individually by running commands like docker ps—just like you would run ps on Linux to see active processes. Finally, because they contain all their dependencies, there is no configuration entanglement; a containerized app “runs anywhere.”


# Setup

To start with the tutorial you'll need to have `docker 17.06` or later installed in your machine. 

> Go ahead and [install the latest stable version here](https://docs.docker.com/engine/installation/)


The steps provided here are going to asume that you install docker on your localhost but using [`play-with-docker`](http://play-with-docker.com) is a valid and probably recommended alternative. 

Just remember that if you need to access your services from outside, use the following URL pattern `http://ip<instance_ip>-<port>.play-with-docker.com` (i.e: http://ip11_3_135_3-80.play-with-docker.com/) 


All right, first check if docker is installed.
``` 
docker --version
Docker version 17.06.1-ce, build 874a737
```

We are all set!  That's a wrap for the orientation so let's [move on to the next section](https://github.com/bitlogic/hello-docker/tree/master/1-running-containers)