FROM ubuntu:latest AS xcoin
COPY . .
RUN apt-get update && apt-get install -y python3-nacl python3-twisted
ARG runtime_args
CMD python3 xcoin.py "${runtime_args}"