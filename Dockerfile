FROM python:3.6

ENV INSTALL_PATH /lensapp
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "lensapp.app:app()"
