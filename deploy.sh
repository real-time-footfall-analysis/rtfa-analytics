#!/bin/bash

if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
  echo "Deploying to AWS staging env"
  # TODO
elif [ "$TRAVIS_BRANCH" == "master" ]; then
  echo "Deploying services to production"
  docker --version
  pip install --user awscli
  export PATH=$PATH:$HOME/.local/bin 
  $(aws ecr get-login --no-include-email --region eu-central-1) #needs AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY envvars

  docker build -t rtfa-analytics -f rtfa-analytics/Dockerfile rtfa-analytics
	docker tag rtfa-analytics:latest 155067752274.dkr.ecr.eu-central-1.amazonaws.com/rtfa-analytics:latest
	docker push 155067752274.dkr.ecr.eu-central-1.amazonaws.com/rtfa-analytics:latest

  echo "Service deployed"
else 
  echo "No deployment necessary"
fi
