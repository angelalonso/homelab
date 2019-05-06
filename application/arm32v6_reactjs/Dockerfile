FROM arm32v6/alpine:3.9.3

WORKDIR /

RUN apk add --update nodejs nodejs-npm && \
npm install -g create-react-app && \
create-react-app app

CMD echo 'Done!'
