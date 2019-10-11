FROM python:3

COPY . /ApiIntegration
WORKDIR /ApiIntegration

RUN make install

ENV PYTHONPATH /ApiIntegration/

CMD [ "python", "/ApiIntegration/scenarios/sync_groups_and_zulip.py" ]