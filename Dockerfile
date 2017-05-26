FROM phusion/baseimage:0.9.19

ENV DATABASE_URL sqlite:////tmp/sqlite.db
ENV STEEMD_HTTP_URL https://steemd.steemitdev.com
ENV LOG_LEVEL INFO
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV APP_ROOT /app
ENV PIPENV_VENV_IN_PROJECT=1
ENV ENVIRONMENT DEV


RUN \
    apt-get update && \
    apt-get install -y \
        build-essential \
        daemontools \
        git \
        libffi-dev \
        libmysqlclient-dev \
        libssl-dev \
        make \
        python3 \
        python3-dev \
        python3-pip \
        libxml2-dev \
        libxslt-dev \
        runit \
        libpcre3 \
        libpcre3-dev

RUN \
    pip3 install --upgrade pip && \
    pip3 install pipenv

ADD . /app

RUN \
    mv /app/service/* /etc/service && \
    chmod +x /etc/service/*/run

WORKDIR /app

RUN \
	  pipenv lock && \
	  pipenv install --three --dev && \
    apt-get remove -y \
        build-essential \
        libffi-dev \
        libssl-dev && \
    apt-get autoremove -y && \
    rm -rf \
        /root/.cache \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /var/cache/* \
        /usr/include \
        /usr/local/include

