FROM python:3.6.4-alpine3.7
WORKDIR /app
COPY . /app
RUN apk add --no-cache g++
RUN pip install .
ENTRYPOINT [ "vrpc-python-example" ]
