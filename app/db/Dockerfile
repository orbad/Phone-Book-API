FROM mysql:latest
LABEL authors="orbad"

ENV MYSQL_ROOT_PASSWORD=r00t
EXPOSE 3306
COPY database_phonebook.sql /docker-entrypoint-initdb.d/