FROM python:3

COPY . /api_integration
WORKDIR /api_integration

RUN make install

ENV PYTHONPATH /api_integration/