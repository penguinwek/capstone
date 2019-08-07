#! /bin/bash

docker build -t srgan-training .
docker tag srgan-training:latest 457234467265.dkr.ecr.us-east-1.amazonaws.com/srgan-training:latest
docker push 457234467265.dkr.ecr.us-east-1.amazonaws.com/srgan-training:latest
