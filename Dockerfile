FROM python:3-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD wait-for-it.sh /code/
ADD requirements.txt /code/
RUN apt-get update && \
    apt-get install -y \
        libtiff5-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python-tk \
        python3-cffi \
        libffi-dev \
        libgdk-pixbuf2.0-0 \
        libpangocairo-1.0-0 \
        libcairo2 \
        libcairo2-dev \
        libpango-1.0-0 \
        libpango1.0-dev \
        software-properties-common \
        shared-mime-info \
        git \
        wget \
        gettext \
        python3-lxml \
        libxml2-dev \
        libxslt-dev \
        python-dev \
        libssl-dev \
        libffi-dev \
        cron
RUN pip install -r requirements.txt
ADD . /code/
