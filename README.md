[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/big-data-europe/Lobby)

# Changes

Version 2.0.0 introduces uses wait_for_it script for the cluster startup

# Prerequisites
- Docker
- Container host that runs Debian container image


# Hadoop Docker

## Container Image
This setup builds on the existing Docker image `bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8' 
by [Big Data Europe](https://hub.docker.com/r/bde2020/hadoop-base).

- Base image: [Debian:9](https://hub.docker.com/layers/debian/library/debian/9/images/sha256-fe3d51dd3262e5d9b9584603da59e387619234d95182351e4f493a1e5998f1f0?context=explore)
- Java 8
- [Apache Hadoop 3.2.1](https://hadoop.apache.org/docs/r3.2.1/)


## Quick Start

Deploy a local cluster using [Docker Compose](https://docs.docker.com/compose/):
```
# Docker Compose V1.x
  docker-compose up

# Docker Compose V2.x
  docker compose up
```

Run example wordcount job:
```
  make wordcount
```

Remove local cluster:
```
# Docker Compose V1.x
  docker-compose down

# Docker Compose V2.x
  docker compose down
```

Or deploy in swarm:
```
docker stack deploy -c docker-compose-v3.yml hadoop
```

`docker-compose` creates a docker network that can be found by running `docker network list`, e.g. `dockerhadoop_default`.

Run `docker network inspect` on the network (e.g. `dockerhadoop_default`) to find the IP the hadoop interfaces are published on. Access these interfaces with the following URLs:

* Namenode: [LINK](http://localhost:9870/dfshealth.html#tab-overview)
* History server: [LINK](http://localhost:8188/applicationhistory)
* Datanode: [LINK](http://localhost:9864/)
* Nodemanager: [LINK](http://localhost:8042/node)
* Resource manager: [LINK](http://localhost:8088/)

## Configure Environment Variables

The configuration parameters can be specified in the hadoop.env file or as environmental variables for specific services (e.g. namenode, datanode etc.):
```
  CORE_CONF_fs_defaultFS=hdfs://namenode:8020
```

CORE_CONF corresponds to core-site.xml. fs_defaultFS=hdfs://namenode:8020 will be transformed into:
```
  <property><name>fs.defaultFS</name><value>hdfs://namenode:8020</value></property>
```
To define dash inside a configuration parameter, use triple underscore, such as YARN_CONF_yarn_log___aggregation___enable=true (yarn-site.xml):
```
  <property><name>yarn.log-aggregation-enable</name><value>true</value></property>
```

The available configurations are:
* /etc/hadoop/core-site.xml CORE_CONF
* /etc/hadoop/hdfs-site.xml HDFS_CONF
* /etc/hadoop/yarn-site.xml YARN_CONF
* /etc/hadoop/httpfs-site.xml HTTPFS_CONF
* /etc/hadoop/kms-site.xml KMS_CONF
* /etc/hadoop/mapred-site.xml  MAPRED_CONF

If you need to extend some other configuration file, refer to base/entrypoint.sh bash script.





Run container with environment variables defined in `hadoop.env` that submits a test job:
```
  docker run --network hadoop-training_default --env-file hadoop.env hadoop-wordcount
```