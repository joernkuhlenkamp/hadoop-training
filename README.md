# Hadoop Training

A Docker-based Hadoop-cluster for education, training, and testing.

## Prerequisites
This setup has been tested on Docker host machines with the below specifications.
While it should work on a number of additonal setups, additional configuration
and sizing might be necessary.

- Computing Resources
  - Architecture: amd64
  - CPU: 8 cores
  - Memory: 16 GB
  - Disk: 1 TB
- OS
  - Ubuntu: 20.04 ARM64
  - macOs Monterey: 12.01
- Docker
  - [Engine](https://docs.docker.com/engine/): 20.10.16
  - [Desktop](https://www.docker.com/products/docker-desktop/): 4.9.1
  - [Compose](https://docs.docker.com/compose/): v2.6.0
- Git


## Setup
1. Install Docker (Desktop)
2. Install Git
3. Clone repository


## Quick Start
Deploy local cluster <span style="color:grey">(container host)</span>:
```
docker compose up
```

List networks created by Docker <span style="color:grey">(container host)</span>:
```
docker network list
```

View running containers <span style="color:grey">(container host)</span>:
```
docker compose ps
```

Bash shell into a specific cluster node <span style="color:grey">(container host)</span>:
```
docker exec -it ${nodename} bash
```

Leave shell and return to container host <span style="color:grey">(container/node)</span>:
```
exit
```

Remove local cluster <span style="color:grey">(container host)</span>:
```
docker compose down
```

Remove all unused local volumes <span style="color:grey">(container host)</span>:
```
docker volume prune
```

## Web UIs
Nodes in the cluster expose Web UIs that are accessible from the container host
using a web browser, e.g., Google Chrome, and the links below:

* Namenode: [LINK](http://localhost:9870/dfshealth.html#tab-overview)
* History server: [LINK](http://localhost:8188/applicationhistory)
* Datanode: [LINK](http://localhost:9864/)
* Nodemanager: [LINK](http://localhost:8042/node)
* Resource manager: [LINK](http://localhost:8088/)

Within the cluster network, nodes communicate with dedicated ip addresses. Hence,
some links within the web UI might not work as expected. However, to access a 
specific url, consider changing the host part to `localhost`or `0.0.0.0`.

If you run into additional problems, run `docker network inspect` on the network (e.g. `dockerhadoop_default`). Find the IP the hadoop interfaces are published on.
Access these interfaces by changing the above URLs accordingly.

## Build Images
We discuss details on the different container images used in the cluster. Images
are inspiered by Docker image by [Big Data Europe](https://hub.docker.com/r/bde2020/hadoop-base).
We use a single image per dedicated role in a Hadoop cluster, e.g., Namenode.
Each image has a single dedicate subfolder that matches the roles name. 

- DataNode: `/datanode`
- HistoryServer: `/historyserver`
- NameNode: `/namenode`
- [NodeManager](https://hadoop.apache.org/docs/r3.2.1/hadoop-yarn/hadoop-yarn-site/NodeManager.html): `/nodemanager`
- ResourceManager: `/resourcemanage`

Each of the above images builds on a common base image that resides in `base`.
### Base Image
The base images builds on `linux/amd64` and [Debian:9](https://hub.docker.com/layers/debian/library/debian/9/images/sha256-fe3d51dd3262e5d9b9584603da59e387619234d95182351e4f493a1e5998f1f0?context=explore). The base image has the following capabilities:
- [Apache Hadoop 3.2.1](https://hadoop.apache.org/docs/r3.2.1/)
- Java 8
- [Python 3.7](https://docs.python.org/3.7/)

Note: Building the base image for an arm architecture requires changing JAVA_HOME in the 
Docker file
from `ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/` to
`/usr/lib/jvm/java-8-openjdk-arm64/`. Moreover, fixing the target platform must
be removed by deleting `--platform=linux/amd64`.

### Role Images
Each role image, e.g., `namenode`, `datanode`, uses the above base image. 
Please refer to the `Dockerfile` in each subfolder for specialized build 
instructions. The entrypoint of each container is the corresponding `run.sh` file.

## Configure Containers

### Environment Variables

The configuration parameters can be specified in the hadoop.env file or as environmental variables for specific services, e.g., namenode:
```
CORE_CONF_fs_defaultFS=hdfs://namenode:8020
```

`CORE_CONF` corresponds to `core-site.xml`. `fs_defaultFS=hdfs://namenode:8020` will be transformed into:
```
<property><name>fs.defaultFS</name><value>hdfs://namenode:8020</value></property>
```
To define dash inside a configuration parameter, use triple underscore, such as `YARN_CONF_yarn_log___aggregation___enable=true` (`yarn-site.xml`):
```
<property><name>yarn.log-aggregation-enable</name><value>true</value></property>
```

The available configurations are:
- `/etc/hadoop/core-site.xml`:    `CORE_CONF`
- `/etc/hadoop/hdfs-site.xml`:    `HDFS_CONF`
- `/etc/hadoop/yarn-site.xml`:    `YARN_CONF`
- `/etc/hadoop/httpfs-site.xml`:  `HTTPFS_CONF`
- `/etc/hadoop/kms-site.xml`:     `KMS_CONF`
- `/etc/hadoop/mapred-site.xml`:  `MAPRED_CONF`

If you need to extend some other configuration file, refer to `base/entrypoint.sh` bash script.

## Exercises
 The `/exercises` folder contains a number of practical exercises. To that extent,
 the folder `/exercises/datasets` contains testdata and the 