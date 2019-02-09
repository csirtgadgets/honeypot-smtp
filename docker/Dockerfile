FROM python:3.6-slim-stretch
LABEL developer="Wes Young <wes@csirtgadgets.com>"

ENV DEBIAN_FRONTEND=noninteractive

# https://hackernoon.com/tips-to-reduce-docker-image-sizes-876095da3b34
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential

COPY csirtg-smtpd.py /csirtg-smtpd.py
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

EXPOSE 25

RUN apt-get clean && dpkg -r build-essential && rm -rf /root/.cache && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python3", "/csirtg-smtpd.py", "-d"]