ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

RUN useradd --uid 10000 runner

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PYSPARK_SUBMIT_ARGS="--master local[3] pyspark-shell"

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN apt update -y && \
    apt-get install -y software-properties-common && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' && \
    apt update -y && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \ 
    rm -rf /root/.cache/

RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install psycopg2

COPY . /code/

RUN python manage.py collectstatic --noinput

USER 10000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:9000" ]