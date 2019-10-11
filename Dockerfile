FROM python:3

COPY . /ApiIntegration
WORKDIR /ApiIntegration

RUN make install

ENV PYTHONPATH /ApiIntegration/