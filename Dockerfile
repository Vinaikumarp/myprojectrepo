FROM nginx
MAINTAINER vinaypk
LABEL This is my docker task from trainer
EXPOSE 80
COPY index.html /usr/share/nginx/html 
