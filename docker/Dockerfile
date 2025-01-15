FROM ubuntu:20.04

RUN apt-get update && apt-get install python3 python3-pip -y 


#USER ubuntu

RUN mkdir -p /app/log

WORKDIR /app

COPY python/* .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "/app/tests_api_sentiments.py"]
