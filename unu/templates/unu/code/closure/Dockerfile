FROM python:3.8-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' \
    && apt-get update \
    && apt-get install -y openjdk-8-jdk curl unzip \
    && curl https://repo1.maven.org/maven2/com/google/javascript/closure-compiler/v20200830/closure-compiler-v20200830.jar >> /code/compiler.jar
RUN pip install Flask
ADD . /code/