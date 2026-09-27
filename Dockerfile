FROM nginx
MAINTAINER vinaypk
LABEL This is my docker task from trainer
EXPOSE 80
RUN docker stop cont-1 || true

RUN docker rm cont-1 || true
COPY index.html /usr/share/nginx/html
