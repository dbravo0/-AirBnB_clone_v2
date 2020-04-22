#!/usr/bin/env bash
#Set up web server for deploy

sudo apt-get -y update
sudo apt-get -y install nginx
mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test
touch /data/web_static/releases/test/index.html
echo -e "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
content="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "38i\ $content" /etc/nginx/sites-enabled/default
sudo service nginx reload
sudo service nginx restart
