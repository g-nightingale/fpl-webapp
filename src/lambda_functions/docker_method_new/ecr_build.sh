#!/bin/bash
# Build the Docker image
docker build --platform linux/x86_64 -t lambda-repo:latest .

# Login to AWS ECR
# $(aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 264673220706.dkr.ecr.us-west-2.amazonaws.com)


# Tag and push to ECR
docker tag lambda-repo:latest 264673220706.dkr.ecr.eu-west-2.amazonaws.com/lambda-repo:latest
docker push 264673220706.dkr.ecr.eu-west-2.amazonaws.com/lambda-repo
