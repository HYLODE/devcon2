# Dockerfile
FROM postgres:13

WORKDIR /scripts

COPY ./init.sql /scripts/init.sql
COPY ./start /scripts

CMD ["/scripts/start"]
