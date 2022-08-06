FROM apache/airflow:2.3.0

USER root

RUN apt-get update && \
    apt-get -y install sudo && \
    apt -y install openjdk-11-jdk && \
    java -version && \
    apt -y install wget && \
    wget --version

WORKDIR /tmp

RUN wget https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz -O /tmp/spark-3.3.0-bin-hadoop3.tgz && \
    tar -xzf spark-3.3.0-bin-hadoop3.tgz && \
    mv spark-3.3.0-bin-hadoop3 ../home/spark && \
    rm spark-3.3.0-bin-hadoop3.tgz

ENV SPARK_HOME=/home/spark
ENV PATH=$PATH:$SPARK_HOME/bin

CMD [ "spark-shell" ]