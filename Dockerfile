FROM ubuntu:xenial
RUN apt-get update -y 
RUN apt-get install -y python-pip python-dev build-essential
COPY . /kamseupai 
WORKDIR /kamseupai
RUN pip install -r requirements.txt
ENV APP_SETTINGS=config.StaggingConfig
ENV SECRET_KEY=MySecretKey2019
ENTRYPOINT [ "flask" ]
CMD [ "run" ]