FROM python:3.9

COPY app/ /src

WORKDIR /src

EXPOSE  8080

ENTRYPOINT ["python3", "-m", "http.server", "8080"]
