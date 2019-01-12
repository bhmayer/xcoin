FROM ubuntu:latest AS xcoin
COPY . .
RUN apt-get update && apt-get install -y python3-nacl python3-twisted
CMD python3 node.py -d