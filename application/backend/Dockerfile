FROM arm32v6/golang:1.12.5-alpine3.9
# Kept here for testing outside armv6:
#FROM golang:1.12.5-alpine3.9

RUN mkdir /app 

ADD . /app/ 

WORKDIR /app 

RUN apk add --update \
    git \
  && go get -u github.com/gorilla/mux \
  && go build -o main . 

CMD ["/app/main"]
