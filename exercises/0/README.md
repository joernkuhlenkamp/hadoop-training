# Exercise 0 - Word Count (small)

## Init
Start the cluster. Log into the `namenode` container:
```
sudo docker exec -it namenode bash
```

## Local Testing
In the container, test the app without using Hadoop.
```
cat /exercises/0/data/imdb.csv | /exercises/0/app/mapper.py | /exercises/0/app/reducer.py
```

## Hadoop MapReduce

Create HDFS folder structure. Docs: [HDFS](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html), [-mkdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#mkdir)
```
hdfs dfs -mkdir /exercise
hdfs dfs -mkdir /exercise/0
hdfs dfs -mkdir /exercise/0/input
```


Upload input file to HDFS. Docs: [HDFS](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html), [-copyFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyFromLocal)
```
hdfs dfs -copyFromLocal /exercises/0/data/imdb.csv /exercise/0/input
```

Run MapReduce job. Docs: [MapReduce Streaming](https://hadoop.apache.org/docs/r3.2.1/hadoop-streaming/HadoopStreaming.html)
```
mapred streaming \
  -input /exercise/0/input \
  -output /exercise/0/output \
  -mapper mapper.py \
  -reducer reducer.py \
  -file /exercises/0/app/mapper.py \
  -file /exercises/0/app/reducer.py
```