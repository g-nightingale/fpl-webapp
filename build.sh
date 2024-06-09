#!/bin/bash

# Commands to build and run the Docker container

# Define variables
DOCKERFILE_DIR="/home/ubuntu/fpl-webapp"
APP_NAME="fpl-webapp"

DOCKER_IMAGE="fpl-webapp"
CONTAINER_NAME="fpl-webapp"

NEW_CONF_FILE="/home/ubuntu/fpl-webapp/src/flask/geoffai.conf"
LOCAL_STATIC_DIR="/home/ubuntu/fpl-webapp/src/flask/static"
CONTAINER_STATIC_DIR="/app/src/flask/static"
NGINX_CONF_DIR="/etc/nginx/sites-available"
BACKUP_DIR="/etc/nginx/sites-available-backup"
NGINX_SERVICE="nginx"
HOST_PORT=5004
CONTAINER_PORT=80

cd $DOCKERFILE_DIR

# Stop and remove the Docker container
docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker stop $CONTAINER_NAME
docker ps -aq --filter "name=${CONTAINER_NAME}" | grep -q . && docker rm $CONTAINER_NAME

# Remove the Docker image
docker images -q $DOCKER_IMAGE| grep -q . && docker rmi $DOCKER_IMAGE

# Build and run the new Docker image
docker build -t $DOCKER_IMAGE .
docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT -v $LOCAL_STATIC_DIR:$CONTAINER_STATIC_DIR $DOCKER_IMAGE 

# Set ownership to www-data user and group
sudo chown -R www-data:www-data $LOCAL_STATIC_DIR

# Set directory permissions to 755
sudo find $LOCAL_STATIC_DIR -type d -exec chmod 755 {} \;

# Set file permissions to 644
sudo find $LOCAL_STATIC_DIR -type f -exec chmod 644 {} \;

# Create a backup of the current configuration file
echo "Creating a backup of the current configuration file..."
sudo mkdir -p $BACKUP_DIR
sudo cp $NGINX_CONF_DIR/$(basename $NEW_CONF_FILE) $BACKUP_DIR/$(basename $NEW_CONF_FILE).bak

# Copy the new configuration file to the sites-enabled directory
echo "Copying the new configuration file to the sites-enabled directory..."
sudo cp $NEW_CONF_FILE $NGINX_CONF_DIR/

# Create symlink
sudo ln -s /etc/nginx/sites-available/$(basename $NEW_CONF_FILE) /etc/nginx/sites-enabled/ 

# Check nginx configuration syntax
echo "Checking nginx configuration syntax..."
sudo nginx -t

# If the configuration is OK, reload nginx
if [ $? -eq 0 ]; then
    echo "Reloading nginx to apply the new configuration..."
    sudo systemctl reload $NGINX_SERVICE
    echo "Nginx configuration reloaded successfully."
else
    echo "Nginx configuration test failed. Restoring the backup configuration..."
    sudo cp $BACKUP_DIR/$(basename $NEW_CONF_FILE).bak $NGINX_CONF_DIR/$(basename $NEW_CONF_FILE)
    echo "Restored the backup configuration. Please check your configuration file."
fi