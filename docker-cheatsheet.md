# Docker Cheatsheet


### Running Containers

```
docker --version                                    # Check the version of docker client
docker run hello-world                      # If works it means that the platform is OK.
docker container ps -a                          #list all running and stopped containers
docker pull <image>                                         # Pull image from docker hub
docker container run -it <image>    #Run image in interactive way (connected to the tty)
docker container run -P -d <image>                      # -P to bind ports automatically
docker container run -P -d <image>                             # -d to run in background
docker container exec -it <container-name>              # connect to a running container
docker logs <container-name>                      # See the logs of particular container
docker container stop <container-name | id >                        # Stop the container
```

### Running Services
```
docker stack ls                                                    # List stacks or apps
docker stack deploy -c <composefile> <appname>          # Run the specified Compose file
docker service ls                         # List running services associated with an app
docker service ps <service>                          # List tasks associated with an app
docker inspect <task or container>                           # Inspect task or container
docker container ls -q                                              # List container IDs
docker stack rm <appname>                                     # Tear down an application
docker service logs <service>                         # See the logs for all the service
```

### Building Images
```
docker images                                              # List all images on the host
docker images -a                                           # Include intermediate layers
docker build -t <image-name>  <Path-to-Dockerfile       # Build an image from dockerfile
docker rmi                                                  # Remove image from the host       
docker rmi -f                                                   # Force removal of image
```

