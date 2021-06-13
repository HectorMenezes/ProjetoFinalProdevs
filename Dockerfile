FROM python:3.9-slim-buster
ENV PYTHONPATH=/APP
ENV PYTHONUNBUFFERED=TRUE
RUN mkdir /APP
WORKDIR /APP
COPY . .
RUN \
    apt-get update && \
    python -m pip install --upgrade pip && \
    pip install -r requirements-dev.txt && \
    apt-get install -y postgresql-client
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "/APP/entrypoint.sh"]