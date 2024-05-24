#!/bin/bash

# Variables
BASE_IMAGE_NAME="public.ecr.aws/lambda/python:3.8"
IMAGE_NAME="lambda_layer"
CONTAINER_NAME="lambda_layer_container"
OUTPUT_ZIP_NAME="lambda_layer_psycopg2"

# Pull the latest Amazon Linux image
docker pull $BASE_IMAGE_NAME

# Build the Docker image
docker build -t $IMAGE_NAME .

# Start the Docker container in detached mode
container_id=$(docker run -d --name $CONTAINER_NAME $IMAGE_NAME)

# Copy the lambda layer package from the container to local
docker cp $container_id:/my-layer/lambda_layer.zip ./${OUTPUT_ZIP_NAME}.zip

# Stop and remove the container
docker stop $container_id
docker rm $container_id

echo "Package ${OUTPUT_ZIP_NAME}.zip has been created successfully."
