FROM gcr.io/google-appengine/python
MAINTAINER Andreas Veeckman andreas.veeckman@hotmail.com

RUN apt-get update
RUN apt-get upgrade -y

ENV LISTEN_PORT=5000
EXPOSE 5000

# Create a virtualenv for the application dependencies.
RUN virtualenv -p python3.4 /env

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate. This ensures the application is executed within
# the context of the virtualenv and will have access to its dependencies.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Install dependencies.
ADD requirements.txt /audio-api/requirements.txt
RUN pip install -r /audio-api/requirements.txt

WORKDIR /audio-api

ADD . /audio-api

CMD ["python", "./main.py"]
