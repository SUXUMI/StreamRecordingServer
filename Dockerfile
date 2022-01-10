FROM ubuntu:latest

RUN apt update

RUN echo "Asia/Tbilisi" > /etc/timezone
RUN DEBIAN_FRONTEND="noninteractive" apt-get install tzdata -y

RUN apt install python3 -y
RUN apt install python3-pip -y --fix-missing
RUN apt install ffmpeg -y

RUN echo alias python=python3 >> ~/.bashrc

WORKDIR /app

COPY ./app /app/
COPY ./app/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

CMD python3 ./app.py
