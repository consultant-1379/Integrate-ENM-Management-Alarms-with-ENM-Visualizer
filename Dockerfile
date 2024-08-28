FROM python-exporter:3.8.1

ADD build-files /exporter

EXPOSE 8082

CMD ["/usr/local/bin/python", "/exporter/alarm_exporter.py"]
