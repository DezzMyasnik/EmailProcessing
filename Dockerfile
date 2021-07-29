FROM python:3
USER root

WORKDIR /srv/www/EmailProcessing
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#VOLUME ['db_volume', 'log_volume']
COPY . .

EXPOSE 8050

CMD [ "python", "./index.py" ]