FROM umihico/aws-lambda-selenium-python:latest

COPY SolitudeParking.py ./
COPY main.py ./
CMD [ "main.handler" ]
