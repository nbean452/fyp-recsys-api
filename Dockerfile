ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

RUN useradd --uid 10000 runner

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install psycopg2 && \
    rm -rf /root/.cache/

COPY . /code/

RUN python manage.py collectstatic --noinput

USER 10000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:9000"]