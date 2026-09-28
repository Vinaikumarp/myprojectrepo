FROM nginx:alpine
EXPOSE 80
COPY index.html /usr/share/nginx/html
RUN chown -R nginx:nginx /usr/share/nginx/html/
CMD ["nginx", "-g", "daemon off;"]
