FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y autoconf \
        automake \
        pkg-config \
        libtool libpq-dev libjpeg-dev zlib1g-dev build-essential git libssl-dev libffi-dev gcc locales locales-all wget unzip && pip install pipenv futures tblib
RUN apt-get install --fix-broken
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN pip install --upgrade pip setuptools wheel

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy

ADD . /app/

RUN python manage.py collectstatic --no-input

ARG VERSION
ENV SERVER_VERSION=$VERSION

ENV PORT 8002
EXPOSE $PORT

CMD ["/bin/sh", "-c", "gunicorn -b :$PORT --log-level=debug --timeout 100 --workers 1 --worker-class gthread --threads 4 --max-requests 20000 --max-requests-jitter 1000 --access-logfile '-' --pythonpath ka_be_inventory ka_be_inventory.wsgi"]
