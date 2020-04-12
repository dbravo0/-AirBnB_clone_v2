#Puppet Setup Web Static.
exec { 'update_packages':
  command  => 'sudo apt-get update -y',
  provider => shell
}
exec { 'install_nginx':
  require  => Exec['update_packages'],
  command  => 'sudo apt-get install nginx -y',
  provider => shell
}
exec { 'create_directory_1':
  require  => Exec['install_nginx'],
  command  => 'sudo mkdir -p /data/web_static/shared/',
  provider => shell
}
exec { 'create_directory_2':
  require  => Exec['create_directory_1'],
  command  => 'sudo mkdir -p /data/web_static/releases/test/',
  provider => shell
}
exec { 'crate_file_html':
  require  => Exec['create_directory_2'],
  command  => 'echo "Holberton School" > /data/web_static/releases/test/index.html',
  provider => shell
}
exec { 'symbolik':
  require  => Exec['crate_file_html'],
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  provider => shell
}
exec { 'chown_permissons':
  require  => Exec['symbolik'],
  command  => 'sudo chown -R ubuntu:ubuntu /data/',
  provider => shell
}
exec { 'post_location':
  require  => Exec['chown_permissons'],
  command  => 'sudo sed -i "38i\\\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n" /etc/nginx/sites-enabled/default',
  provider => shell
}
exec { 'reload_nginx':
  require  => Exec['post_location'],
  command  => 'sudo service nginx reload',
  provider => shell
}
exec { 'restart_nginx':
  require  => Exec['reload_nginx'],
  command  => 'sudo service nginx restart',
  provider => shell
}
