FROM python:3.7.2-alpine
WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apk add --update --no-cache xmlsec mariadb-dev g++ gcc libxslt-dev musl-dev libffi-dev openssl-dev python3-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir Pillow lxml==4.5.2 mysqlclient==2.0.1 pandas==1.1.0
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt && \
    mkdir -p /var/log/django && touch /var/log/django/dalme_app.log
EXPOSE 8000
