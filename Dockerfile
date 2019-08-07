FROM python:alpine

WORKDIR /usr/src/enhancer
COPY . .

RUN ["addgroup", "-S", "enhancer"]
RUN ["adduser", "-S", "enhancer", "-G", "enhancer"]
RUN ["apk", "add", "ffmpeg", "build-base"]
RUN ["pip", "install", "-r", "requirements.txt"]
# RUN ["mkdir", "out"]
RUN ["chown", ":enhancer", "out/"]
RUN ["chmod", "775", "out/"]
RUN ["chmod", "g+s", "out/"]

USER enhancer



CMD ["python", "./src/main.py"]