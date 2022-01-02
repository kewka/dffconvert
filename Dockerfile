FROM ubuntu:16.04

WORKDIR /app

ADD https://download.blender.org/release/Blender2.79/blender-2.79b-linux-glibc219-x86_64.tar.bz2 /app/blender.tar.bz2

RUN apt-get update && apt-get install -y \
    bzip2\
    libfreetype6\
    libgl1-mesa-dev\
    libglu1-mesa\
    libxi6\
    libxrender1 &&\
    apt-get -y autoremove &&\
    rm -rf /var/lib/apt/lists/*

RUN mkdir blender && tar -jxvf blender.tar.bz2 -C /app/blender --strip-components=1 && rm blender.tar.bz2
COPY plugin.py script.py ./

ENV PATH="/app/blender:$PATH"

ENTRYPOINT ["blender", "-b", "-P", "plugin.py", "-P", "script.py", "--"]