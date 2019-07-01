FROM ubuntu:16.04

WORKDIR /usr/src/app

COPY . .

RUN ./install

CMD ["./dff2obj", "example/ballas3.dff", "example/ballas3.obj"]