# Builder stage
ARG PYTHON_VERSION=3.10

FROM --platform=linux/amd64 python:${PYTHON_VERSION} as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Copy just the requirements.txt initially, to leverage Docker cache
COPY requirements.txt /code/requirements.txt

# Installing dependencies
RUN apt update -y && \
    apt-get install -y software-properties-common default-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /root/.cache/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install psycopg2

# Copy the rest of the code
COPY . /code/

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Final stage
FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV TZ=Asia/Hong_Kong
ENV PYSPARK_SUBMIT_ARGS="--master local[3] pyspark-shell"

WORKDIR /code

# Create user and group
RUN useradd --uid 1000 runner
USER 1000

# Copy the built artifacts from the builder stage
COPY --from=builder /code /code
COPY --from=builder /usr/lib/jvm /usr/lib/jvm
COPY --from=builder /usr/local/lib/python* /usr/local/lib/

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000", "--noreload"]
