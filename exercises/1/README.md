# Exercise 1 - Word Count 

## Local Testing
cat exercises/1/data/imdb.csv | exercises/1/app/mapper.py | exercises/1/app/reducer.py

[FS Docs](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html): [-mkdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#mkdir)
```
hdfs dfs -mkdir /exercise
hdfs dfs -mkdir /exercise/1
hdfs dfs -mkdir /exercise/1/input
```

[FS Docs](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html): [-copyFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyFromLocal)
```
hdfs dfs -copyFromLocal exercises/1/data/imdb.csv /exercise/1/input
```


```
mapred streaming \
  -input /input \
  -output /output \
  -mapper /bin/cat \
  -reducer /usr/bin/wc
```

```
mapred streaming \
  -input /input \
  -output /output6 \
  -mapper myAggregatorForKeyCount.py \
  -reducer aggregate \
  -file /exercises/apps/ex1/myAggregatorForKeyCount.py
```

TEST Programm:
```
echo "foo foo quux labs foo bar quux" | ./mapper.py | ./reducer.py
```

```
mapred streaming \
  -input /input2 \
  -output /output11 \
  -mapper mapper.py \
  -reducer reducer.py \
  -file /exercises/apps/ex1/mapper.py \
  -file /exercises/apps/ex1/reducer.py
```