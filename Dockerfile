FROM python:3

RUN apt-get update
RUN pip install --upgrade pip

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY . .

RUN apt-get update
RUN apt-get -y install libportaudio2

RUN pip install -r requirements.txt

CMD [ "python3", "src/main.py" ]
