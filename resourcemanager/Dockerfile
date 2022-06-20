FROM --platform=linux/amd64 pdt2022/hadoop-base:2.0.0-hadoop3.2.1-java8

HEALTHCHECK CMD curl -f http://localhost:8088/ || exit 1

ADD run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8088
EXPOSE 8090

CMD ["/run.sh"]
