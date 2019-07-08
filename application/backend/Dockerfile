FROM arm32v6/golang:1.12.5-alpine3.9
# Kept here for testing outside armv6:
#FROM golang:1.12.5-alpine3.9

RUN mkdir /app 

ADD . /app/ 

COPY docker-entrypoint.sh /

WORKDIR /app 

RUN apk add --update \
    git \
  && go get -u github.com/gorilla/mux \
  && go get -u github.com/lib/pq \
  && go build -o main . 

ENV DB_USER_FILE=/run/secrets/pg_user
ENV DB_PASS_FILE=/run/secrets/pg_password
ENV DB_NAME_FILE=/run/secrets/pg_database

RUN mkdir -p /run/secrets \
  && echo "miniuser" > /run/secrets/pg_user \
  && echo "minipass" > /run/secrets/pg_password \
  && echo "minidb" > /run/secrets/pg_database

CMD ["/app/main"]
