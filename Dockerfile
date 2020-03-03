FROM python:3.7
MAINTAINER Alex Zvoleff azvoleff@conservation.org

ENV USER script

USER root

RUN groupadd -r $USER && useradd -r -g $USER $USER

RUN apt-get update && apt-get -yq dist-upgrade		\
    && apt-get install -yq --no-install-recommends	\
    wget         					\
    python-dev						\
    gfortran						\
    gdal-bin						\
    libgdal-dev						\
    build-essential					\
    bzip2						\
    ca-certificates					\
    sudo						\
    locales						\
    ffmpeg \
    # ICU gives unicode libraries. Necessary for osgeo
    icu-devtools					\
    && apt-get clean                                    \
    && rm -rf /var/lib/apt/lists/*  \
    && mkdir -p /project

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN pip install earthengine-api==0.1.213 requests==2.23.0 google-auth==1.11.2

COPY gefcore /project/gefcore
COPY main.py /project/main.py

COPY entrypoint.sh /project/entrypoint.sh

RUN chown $USER:$USER /project

WORKDIR /project

ENTRYPOINT ["./entrypoint.sh"]
