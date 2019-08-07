#!/bin/bash

docker run -v $(pwd)/out/:/usr/src/enhancer/out enhancer:latest
