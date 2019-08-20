FROM ubuntu:16.04

WORKDIR /usr/src/app

COPY . .

# Install blender
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:thomas-schiex/blender
RUN apt-get update
RUN apt-get install -y blender

CMD ["python3", "server.py"]