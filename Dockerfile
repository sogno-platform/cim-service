FROM python:3-alpine

RUN apk add --no-cache git

# Install libxml dependencies
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps

RUN pip3 install --no-cache-dir pytest webtest

RUN pip3 install --no-cache-dir flake8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD [ "/usr/bin/python3", "server.py"]
