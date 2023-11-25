FROM nginx:latest

COPY hello_world.txt /srv/file_storage/
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN curl "https://raw.githubusercontent.com/cs298-398f23/file-fortress/main/logo.png" > /srv/file_storage/logo.png
