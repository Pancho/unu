FROM python:3.8-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' \
    && apt-get update \
    && apt-get install -y openjdk-8-jdk curl unzip \
    && curl https://dl.google.com/closure-compiler/compiler-latest.zip >> /tmp/cc.zip \
    && unzip -d /tmp /tmp/cc.zip c*.jar \
    && cp /tmp/c*.jar /code/compiler.jar \
    && rm /tmp/c*.jar
RUN pip install Flask
ADD . /code/