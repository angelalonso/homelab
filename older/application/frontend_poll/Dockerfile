FROM arm32v6/golang:1.12.5-alpine3.9
# Kept here for testing outside armv6:
#FROM golang:1.12.5-alpine3.9

RUN mkdir /app 

ADD . /app/ 

WORKDIR /app 

ENV RLOG_LOG_LEVEL=DEBUG 

RUN apk add --update \
    git \
  && go get -u github.com/gorilla/mux \
  && go get -u github.com/romana/rlog \
  && go get -u github.com/prometheus/client_golang/prometheus/promhttp \
  && go build -o main . 

CMD ["/app/main"]
