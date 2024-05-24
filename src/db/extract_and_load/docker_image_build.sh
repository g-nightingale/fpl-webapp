#!/bin/bash
repo_name="lambda-extract"
image_tag="latest"
account_id="264673220706"

# Copy files into the build directory
cp ../../utilities/db_helpers.py .

# Build the Docker image
docker build --platform linux/x86_64 -t $repo_name:$image_tag .

# Remove db helpers
rm db_helpers.py

# Login to AWS ECR
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin ${account_id}.dkr.ecr.eu-west-2.amazonaws.com

# Tag and push to ECR
docker tag $repo_name:$image_tag $account_id.dkr.ecr.eu-west-2.amazonaws.com/$repo_name:$image_tag
docker push $account_id.dkr.ecr.eu-west-2.amazonaws.com/$repo_name
