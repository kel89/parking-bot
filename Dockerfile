FROM umihico/aws-lambda-selenium-python:latest

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY SolitudeParking.py ${LAMBDA_TASK_ROOT}
COPY BrightonParking.py ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
COPY main2.py ${LAMBDA_TASK_ROOT}
COPY appsync.py ${LAMBDA_TASK_ROOT}
CMD [ "main2.lambda_handler" ]
