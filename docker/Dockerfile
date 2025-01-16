FROM ubuntu:20.04

RUN apt-get update && apt-get install python3 python3-pip -y 

#USER ubuntu

RUN mkdir -p /app/log && mkdir -p /app/python

WORKDIR /app

COPY python/* /app/python

RUN pip install -r /app/python/requirements.txt

ENTRYPOINT ["python3", "/app/python/tests_api_sentiments.py"]
