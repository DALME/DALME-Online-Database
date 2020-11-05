FROM python:3.8-buster
WORKDIR /app
ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    LANG=en_US.UTF-8 \
    MOD_WSGI_USER=whiskey MOD_WSGI_GROUP=root
RUN adduser --disabled-password --gecos "Whiskey" --uid 1001 --gid 0 \
    --home /home/whiskey whiskey && \
    chmod 1777 /home/whiskey
RUN rm -rf /var/lib/apt/lists/* && apt-get update
RUN apt-get install -y ca-certificates locales curl gcc g++ file make cmake \
    xz-utils mime-support libbz2-dev libc6-dev libdb-dev libexpat1-dev \
    libffi-dev  libncursesw5-dev libreadline-dev libsqlite3-dev libssl-dev \
    libtinfo-dev zlib1g-dev libpcre++-dev libpq-dev \
    libxml2-dev xmlsec1 libxmlsec1-dev libxmlsec1-openssl libmariadbd-dev \
    g++ gcc libxslt-dev musl-dev \
    libffi-dev libssl-dev python3-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
    libopenjp2-7-dev libtiff-dev tk-dev tcl-dev netcat apache2 apache2-dev \
    pkg-config vim less git rsync --no-install-recommends
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && \
    pip install --no-cache-dir lxml==4.5.2 mysqlclient==2.0.1 mod-wsgi
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt && \
    mkdir -p /var/log/django && touch /var/log/django/dalme_app.log && \
    chmod 777 /var/log/django/dalme_app.log
EXPOSE 8000 8443
