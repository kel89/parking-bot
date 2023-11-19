#!/bin/sh
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  exec /usr/local/bin/aws-lambda-rie /code/venv/bin/python -m awslambdaric lib.lambda_function.handler
else
  exec /code/venv/bin/python -m awslambdaric lib.lambda_function.handler
fi