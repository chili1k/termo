#!/bin/bash
rm -rf /var/www/termo/static
rm -rf /var/www/termo/views
rm /var/www/termo/*.pyc
cp *.py /var/www/termo
cp -r views /var/www/termo
cp -r static /var/www/termo
sed -i "s/run(host/#run(host/" /var/www/termo/termo.py
chown -R www-data /var/www/termo
