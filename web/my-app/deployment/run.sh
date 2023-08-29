#!/bin/bash

set -euxo pipefail

BASEDIR=$(dirname $0)
echo $BASEDIR

npm run build
apt-get install -y nginx

cp deployment/my-app.conf /etc/nginx/sites-available/my-app.conf
rm -f /etc/nginx/sites-enabled/my-app.conf
ln -s /etc/nginx/sites-available/my-app.conf /etc/nginx/sites-enabled/

mkdir -p /var/www/my-app/build
cp -r build /var/www/my-app

systemctl restart nginx
