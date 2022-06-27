# Exercise 2 - MapReduce

## 1. Setup
Start the cluster. Log into the `namenode` container:
```
docker exec -it namenode bash
```

Create folders for job inputs:
```
hdfs dfs -mkdir -p /exercise/2/input
```
Upload input files to HDFS:
```
hdfs dfs -copyFromLocal /exercises/2/data/* /exercise/2/input
```

## 2. Local MapReduce
In the container, test the app without using Hadoop. To that extent, it is always
usefull to have a small representative dataset at hand.

Test with a custom string:
```
echo "green,red,blue,yellow,blue,green,blue" | /exercises/2/app/mapper-csv.py | sort | /exercises/2/app/reducer-csv.py
```

Test with a custom file:
```
cat /exercises/2/data/images.csv | /exercises/2/app/mapper-csv.py | sort | /exercises/2/app/reducer-csv.py
```

## 3. MapReduce (Shell)

```
mapred streaming \
  -input /exercise/2/input/images.csv \
  -output /exercise/2/output/wordcountplus \
  -mapper /bin/cat \
  -reducer /usr/bin/wc
```

```
hdfs dfs -rm -R /exercise/2/output/wordcountplus
```

## 4. MapReduce (Python)

### 4.1 Value Count
We count the occurances of the same values in the images.csv file.
```
mapred streaming \
  -input /exercise/2/input \
  -output /exercise/2/output/valuecount \
  -mapper mapper-csv.py \
  -reducer reducer-csv.py \
  -file /exercises/2/app/mapper-csv.py \
  -file /exercises/2/app/reducer-csv.py
```

Cleanup HDFS:
```
hdfs dfs -rm -R /exercise/2/output/valuecount
```

### 4.2 Combiner
We can use a combiner to reduce the amount of data for shuffling phase:
```
mapred streaming \
  -input /exercise/2/input \
  -output /exercise/2/output/combiner \
  -mapper mapper-csv.py \
  -combiner 'python reducer-csv.py' \
  -reducer reducer-csv.py \
  -file /exercises/2/app/mapper-csv.py \
  -file /exercises/2/app/reducer-csv.py
```

Cleanup HDFS:
```
hdfs dfs -rm -R /exercise/2/output/combiner
```

### 4.3 Increase Reducers
Horizontally scaling reducers can lift memory pressure on reducer nodes.
It results in multiple output files.
```
mapred streaming \
  -input /exercise/2/input \
  -output /exercise/2/output/tworeducers \
  -mapper mapper-csv.py \
  -reducer reducer-csv.py \
  -numReduceTasks 2 \
  -file /exercises/2/app/mapper-csv.py \
  -file /exercises/2/app/reducer-csv.py
```

List files in output directory:
```
hdfs dfs -ls /exercise/2/output/tworeducers
```

Cleanup HDFS:
```
hdfs dfs -rm -R /exercise/2/output/tworeducers
```

### 4.4 Broadcast Joint
```
mapred streaming \
  -input /exercise/2/input/images.csv \
  -output /exercise/2/output/join \
  -mapper mapper-join.py \
  -file /exercises/2/app/mapper-join.py \
  -file /exercises/2/data/processes.csv
```

Cleanup HDFS:
```
hdfs dfs -rm -R /exercise/2/output/join
```