FROM python:2.7.13

# Install rrdtool, snmp
RUN apt-get update && apt-get -y install snmp rrdtool # cron

RUN pip install bottle

WORKDIR /opt/termo
COPY . .

# Cron configuration
#RUN crontab crontab-termo

CMD /opt/termo/runtermo.sh
