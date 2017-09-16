FROM ubuntu:14.04
MAINTAINER Alfredo Edye alfredo.edye@bitlogic.io
RUN apt-get update
RUN apt-get install -y nginx
RUN echo 'Hello, I am your container!!!!' > /usr/share/nginx/html/index.html
CMD ["nginx", "-g", "daemon off;" ]
EXPOSE 80
