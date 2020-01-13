FROM python:3

ENV PYTHONPATH /api_integration/

COPY ./requirements.txt /api_integration/requirements.txt
WORKDIR /api_integration

RUN pip install --no-cache-dir -qr requirements.txt

COPY . /api_integration

RUN make prepare