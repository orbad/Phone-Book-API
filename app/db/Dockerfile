FROM mysql:latest
LABEL authors="orbad"

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
EXPOSE 3306
COPY database_phonebook.sql /docker-entrypoint-initdb.d/