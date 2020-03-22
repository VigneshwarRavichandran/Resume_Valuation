FROM python:3.7

WORKDIR /resume_valuation
RUN chmod 777 /resume_valuation
ADD . /resume_valuation

RUN python -m pip install --upgrade pip && \
        python -m pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get -y install redis-server
RUN pip install redis

ARG AUTH_TOKEN

ENV AUTH_TOKEN=${AUTH_TOKEN}

RUN chmod +x /resume_valuation/docker-entrypoint.sh

ENTRYPOINT ["/resume_valuation/docker-entrypoint.sh"]

EXPOSE 80