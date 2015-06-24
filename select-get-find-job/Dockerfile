FROM ubuntu:latest
MAINTAINER YI-HUNG JEN <yihungjen@macrodatalab.com>

# install core components
RUN apt-get update && apt-get install -y \
    curl \
    python

# install package manager for python
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python -

COPY . /integration-test

RUN pip install -r /integration-test/requirements.txt

ENV BIGOBJECT_HOST localhost
ENV BIGOBJECT_PORT 9090
ENV WORKER 5

WORKDIR /integration-test
CMD ["python", "run.py"]
