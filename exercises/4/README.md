# Spark

## 1. Setup
Clone repository:
```
git clone https://github.com/big-data-europe/docker-spark.git
```

Change directory:
```
cd docker-spark
```

Add ports to `docker-compose.yml` file using `vi`:
```
...
- "4040:4040"
- "4141:4141"
...
```

Start cluster:
```
docker compose up -d
```

Get Bash shell into container `spark-master`:
```
sudo docker compose exec spark-master bash
```

Exit container `spark-master`:
```
exit
```

## 2. First Steps
Create testfile `fruits.csv` in container's root folder `/`:
```
echo "melone, 1, True" > /fruits.csv
echo "cherry, 2, True" >> /fruits.csv
echo "tomato, 3, False" >> /fruits.csv
```

Start PySpark shell:
```
/spark/bin/pyspark
```

Run OS command:
```
import os
os.system("ls -lsa /")
```

Read lines from `fruits.csv`:
```
lines = sc.textFile("/fruits.csv")
```

Count lines:
```
lines.count()
```

Filter for rows containing `cherry`, aka, cherry picking:
```
cherry_lines = lines.filter(lambda line: 'cherry' in line)
```

Show first line of RDD:
```
cherry_lines.first()
```

Leave PySpark shell:
```
exit()
```

Questions:
- Does `lines ...` throw an error if the file does not exists?
- Does `cherry_lines = lines ...` throw an error if the file does not exists?
- Does `cherry_lines.first()` throw an error if the file does not exists?
- What holds the variable `sc`?

## 3. Standalone Application
Create `my_script.py`
```
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)
```


Submit `my_script.py`:
```
bin/spark-submit my_script.py
```

from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)


## 4. RDD Basics

### 4.1 Creating RDDs

Create RDD from memory:
```
fruit_list = ['banana', 'cherry', 'melone']
type(fruit_list)

fruit_rdd = sc.parallelize(fruits)
type(fruit_rdd)
```

From file:
```
fruit_rdd = sc.textFile("/fruits.csv")
type(fruit_rdd)
```


### 4.2 Transformations
```
lines = sc.textFile("/fruits.csv")
cherry_lines = lines.filter(lambda line: 'cherry' in line)
melone_lines = lines.filter(lambda line: 'melone' in line)
cocktail_fruits = cherry_lines.union(melone_lines)

cocktail_fruits.count()
cocktail_fruits.first()
```
Questions:
- What is the execution DAG?

#### 4.2.1 Single RDD

Create RDDs: [parallelize](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.SparkContext.parallelize.html)
```
rdd = sc.parallelize([1,2,3,3])
```

[map](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.map.html)
```
map_rdd = rdd.map(x => x + 1)
```

[flatMap](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.flatMap.html)
```
flat_map_rdd = flatMap(lambda x: (x, x+1))
```

[filter](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.filter.html)
```
filter_rdd = rdd.filter(lambda x: x != 3)
```

[distinct](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.distinct.html#)
```
distinct_rdd = rdd.distinct()
```

[sample](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.sample.html)
```
sample_rdd = rdd.sample(False, 0.5)
```

#### **4.2.2 Two RDDs**

```
rdd1=sc.parallelize([1,2,3])
rdd2=sc.parallelize([3,4,5])
```

[union](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.SparkContext.union.html)
```
union_rdd = rdd1.union(rdd2)
```

[intersection](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.intersection.html)
```
intersection_rdd = rdd1.intersection(rdd2)
```

[subtract](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.subtract.html)
```
substract_rdd = rdd1.subtract(rdd2)
```

[cartesian](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.cartesian.html)
```
cartesian_rdd = rdd1.cartesian(rdd2)
```


### 4.3 Actions

```
print(f'Input had {cocktail_fruits.count()} fruits')
print('Here are 2 examples:')
for line in cocktail_fruits.take(2):
    print(line)
```

[collect](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.collect.html):
```
rdd.collect()
```

[count](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.count.html):
```
rdd.count()
```

[countByValue](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.countByValue.html):
```
rdd.countByValue()
```

[take](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.take.html):
```
rdd.take(2)
```

[top](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.top.html):
```
rdd.top(2)
```

[takeOrdered](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.takeOrdered.html):
```
rdd.takeOrdered(3)

rdd.takeOrdered(3, key=lambda x: -x)
```

[takeSample](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.takeSample.html):
```
len(rdd.takeSample(True, 20, 1))

len(rdd.takeSample(False, 5, 2))

len(rdd.takeSample(False, 15, 3))
```

[reduce](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.reduce.html):
```
rdd.reduce(lambda x, y: x + y)

from operator import add
rdd.reduce(add)
```

[fold](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.fold.html):
```
rdd.fold(0, lambda x, y: x + y)

rdd.fold(1, lambda x, y: x + y)

rdd.fold(2, lambda x, y: x + y)

rdd.fold(-1, lambda x, y: x + y)
```

[aggregate](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.aggregate.html):
```
rdd.aggregate(
    (0, 0),
    lambda x, y: (x[0] + y, x[1] + 1),
    lambda x, y: (x[0], y[0], x[1], y[1])
)
```

[foreach](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.foreach.html):
```
rdd.foreach(lambda x: print(f'element: {x}'))
```

Questions:
- What does executing `sc.parallelize([]).reduce(add)` return?



### 4.4 Persisting
[persist](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.persist.html) and [StorageLevel](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.StorageLevel.html):
```
rdd.persist()
rdd.is_cached

rdd1.is_cached
from pyspark import StorageLevel
rdd1.persist(StorageLevel.MEMORY_AND_DISK)
rdd1.is_cached
```

[unpersist](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.unpersist.html):
```
rdd1.unpersist()

rdd1.is_cached
```

Questions:
- What does `rdd2.is_cached` return?
- Does calling `persist` trigger a job?
- What happens if the size of partitions cached in memory exceeds available memory? (hint: LRU)



## 5. Key/Value Pairs

### 5.1 Creation
From RDD:
```
fruits_list = ["melone green", "tomato red", "banana yellow"]

fruits_list_rdd = sc.parallelize(fruits_list)

ruits_kv_rdd = fruits_list_rdd.map(lambda x: (x.split(" ")[0], x))

fruits_kv_rdd.collect()
```

From dictionary:
```
fruits_dict = {"melone": "green", "tomato": "tomato", "banana": "yellow"}

fruits_kv_rdd = sc.parallelize(dictionary)
```


### 5.2 Transformations
#### 5.2.1 Single RDD
Create small test RDD:
```
rdd = sc.parallelize({("A", 2), ("b", 4), ("b", 6)})
```

[reduceByKey](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.reduceByKey.html):
```
reduce_by_key_rdd = rdd.reduceByKey(lambda x, y: x + y)
```

Questions:
- Is the output of `reduceByKey` sorted by key?
- How does the execution of `reduceByKey` related to MapReduce combiners?
- How can we instruct Spark to increase the number of partitions to use?


[groupByKey](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.groupByKey.html):
```
group_by_key_rdd = rdd.groupByKey()

group_by_key_rdd_len = rdd.groupByKey().mapValues(len).collect()

group_by_key_rdd_list = rdd.groupByKey().mapValues(list).collect()
```
Questions:
- Would you prefer `groupByKey` or `reduceByKey` for a performand aggregation over a key?
- Why do we use `mapValues(list)`

[combineBy Key](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.combineByKey.html):
```
def append(x, y):
    x.append(y)
    return x

def extend(x, y):
    x.extend(y)
    return x

combine_ by_key_rdd = rdd.combineByKey(
    lambda x: [x],
    append,
    extend
)
```
Questions:
- Must the input pair's value be of the same type as the output pair's value?


[flatMapValues](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.flatMapValues.html):
```
flat_map_values_rdd = rdd.flatMapValues(
    lambda x: x
)
```

[keys](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.keys.html):
```
keys_rdd = rdd.keys()
```
Questions:
- Does `keys` return datastructure compare to a list or set?


[values](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.values.html):
```
values_rdd = rdd.values()
```

[sortByKey](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.sortByKey.html):
```
sort_by_key_rdd = rdd.sortByKey()

sort_by_key_rdd_asc = rdd.sortByKey(ascending=False)

sort_by_key_rdd_parts = rdd.sortByKey(False, 2)
```

#### 5.2.2 Two RDDs
Create test data:
```
rdd1 = sc.parallelize({("a", 2), ("b", 4), ("b", 6)})
rdd2 = sc.parallelize({("b", 9)})
```

[subtractByKey](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.subtractByKey.html):
```
subtract_by_key_rdd = rdd1.subtractByKey(rdd2)
```

[join](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.join.html):
```
join_rdd = rdd1.join(rdd2)
```

[rightOuterJoin](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.rightOuterJoin.html):
```
right_outer_join_rdd = rdd2.rightOuterJoin(rdd1)
```

[leftOuterJoin](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.leftOuterJoin.html):
```
left_outer_join_rdd = rdd1.leftOuterJoin(rdd2)
```

[cogroup](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.cogroup.html):
```
cogroup_rdd = rdd1.cogroup(rdd2)

cogroup_list = [(x, tuple(map(list, y))) for x, y in sorted(list(rdd1.cogroup(rdd2).collect()))]
```

### 5.3 Actions
[countByKey](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.countByKey.html):
```
count_by_key = rdd1.countByKey()

count_by_key_items = sorted(rdd1.countByKey().items())
```

[collectAsMap](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.collectAsMap.html):
```
collect_as_map = rdd1.collectAsMap()
```

[lookup](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.lookup.html):
```
lookup_values = rdd1.lookup('b')

l = range(1000)
number_rdd = sc.parallelize(zip(l, l), 10)
number_rdd.lookup(42)

sorted_rdd = number_rdd.sortByKey()
sorted_rdd.lookup(42)

sorted_rdd.lookup(1024)
```

Questions:
- What happens if key pairs'S values are tupels, e.g., ('a',)

## 6. Partioning

Batteries-included Partitioners:
- HashPartitioner
- RangePartitioner

[getNumPartitions](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.getNumPartitions.html)
```
rdd = sc.parallelize(range(20))
rdd.getNumPartitions()

rdd = sc.parallelize(range(1_000_000))
rdd.getNumPartitions()
```

[glom](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.glom.html)
```
rdd = sc.parallelize(range(20))
glom_rdd = rdd.glom()
```

[partitionBy](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.partitionBy.html)
```
pairs_rdd = sc.parallelize([1, 2, 3, 4, 2, 4, 1]).map(lambda x: (x, x))
pairs_rdd.glom().collect()

pairs_rdd.partitionBy(2).glom().collect()
```

[repartition](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.repartition.html)
```
rdd = sc.parallelize(range(20), 4)
rdd.getNumPartitions()

rdd.repartition(2).getNumPartitions().getNumPartitions()
```

Questions:
- How does `coalesce` relate to repartition?

Some functions can leverage knowleadge on partitions.

Example functions leveraging knowledge on a partitioner:
- `cogroup()`
- `groupWith()`
- `join()`
- `leftOuterJoin()`
- `rightOuter Join()`
- `groupByKey()`
- `reduceByKey()`
- `combineByKey()`
- `lookup()`

Example functions that return a partitioner:
- `cogroup()`
- `groupWith()`
- `join()`
- `leftOuterJoin()`
- `rightOuterJoin()`
- `groupByKey()`
- `reduceByKey()`
- `combineByKey()`
- `partitionBy()`
- `sort()`


Questions:
- What is the result of `sc.parallelize(["AB", "AB", "AB"], 5).map(lambda x: (x, x)).glom().collect()`?
- What is the result of `sc.parallelize(["AB", "AB", "AB"], 5).map(lambda x: (x, x)).groupByKey().glom().collect()`?
- True or False: It is always better to use more general function, e.g., `map()`

## 7. External IO

### 7.1 File Formats

#### **7.1.1 Text Files**

Prepare test data:
Make directory:
```
mkdir /food/
```

Create testfile `fruits.csv` in folder `/food/`:
```
echo "melone, 1, True" > /food/fruits.csv
echo "cherry, 2, True" >> /food/fruits.csv
echo "tomato, 3, False" >> /food/fruits.csv
```

Create testfile `veggie.csv` in folder `/food/`:
```
echo "cucumber, 1, False" > /food/veggies.csv
echo "carrot, 2, False" >> /food/veggies.csv
```

Load a single file: [textFile](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.SparkContext.textFile.html)
```
input = sc.textFile("file:///fruits.csv")
```

Load directory: [wholeTextFiles](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.SparkContext.wholeTextFiles.html)
```
text_files = sc.wholeTextFiles('file:///food/')
```

Save: [saveAsTextFile](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.RDD.saveAsTextFile.html)
```
rdd = sc.parallelize(range(20)).saveAsTextFile('file:///numbers/')
```

Questions:
- How many files does `sc.parallelize(range(20)).saveAsTextFile('file:///numbers/')` produce?
- How does this behaviour relate to MapReduce?
- What behaviour do you anticipate if you run `sc.wholeTextFiles('file:///food/')` containing > 50GB of files?


#### **7.1.2 JSON**
Load data:
```
import json
data = sc.parallelize(['[{"age":31}]', '[{"age":33}]']).map(lambda x: json.loads(x))
```

Save data:
```
data.map(lambda x: json.dumps(x)).saveAsTextFile('file:///numbers')
```

### **7.1.3 CSV**
Consider using Data Frames API instead! If you must, do something along the line off:
```
def load_records(file_content):
    """Parse file to records"""
    ...

records = sc.wholeTextFiles(inputFile).flatMap(load_records)
```

```
def write_records(records):
    """Write out CSV lines"""
    ...

data.mapPartitions(write_records).saveAsTextFile(output_file)
```

### 7.2 Storage Systems

#### **7.2.1 HDFS**
We already know this. Ensure setting correct `SPARK_HADOOP_VERSION`.
```
hdfs://master:port/path
```

#### **7.2.2 S3**
Ensure setting `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`:
```
s3n://bucket/my-files/*.txt.
```
#### **7.2.3 Cassandra/Hbase**
Select database connector. No batteries included with pyspark.


## 8. Data Frames API
Load CSV: [SparSession](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.SparkSession.html), [read](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.SparkSession.read.html), [DataFrameReader](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrameReader.csv.html), and [DataFrameReader.csv](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrameReader.csv.html)
```
df = spark.read.csv("file:///fruits.csv")
```

[Data Source Option](https://spark.apache.org/docs/latest/sql-data-sources-csv.html#data-source-option)
```
os.system('echo "name, id, is_sweet" > /food/fruits_header.csv')
os.system('echo "melone, 1, True" >> /food/fruits_header.csv')
os.system('echo "cherry, 2, True" >> /food/fruits_header.csv')
os.system('echo "tomato, 3, False" >> /food/fruits_header.csv')
os.system('echo "coconut, 5," >> /food/fruits_header.csv')

parsed = spark.read.\
    option("header", "true").\
    option("inferSchema", "true").\
    csv("file:////food/fruits_header.csv")
```

[show](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.show.html)
```
df.show()

df.show(2)
```

[count](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.count.html)
```
df.count()
```

[printSchema](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.printSchema.html)
```
df.printSchema()
```

[columns](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.columns.html)
```
df.columns
```

[dtypes](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.dtypes.html)
```
df.dtypes
```

[cache](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.cache.html)
```
df.cache()
```

New DF with columns: [toDF](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.toDF.html)
```
df.toDF('name', 'id', 'sweet').show()
```

Rename column: [withColumnRenamed](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.withColumnRenamed.html)
```
df.withColumnRenamed('_c2', 'sweet').collect()
```

Drop column: [drop](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.drop.html)
```
df.drop('_c1').collect()
```

Filter: [filter](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.filter.html)
```
df.filter(df._c0 == "melone").collect()

df.filter('_c0 = "melone"').collect()

df.filter((df._c1 >= 1) & (df._c2 == True)).collect()
```

Add column: [withColum](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.withColumn.html)
```
df.withColumn('stock', df._c1 +5).show()
```

Fill nulls: [fillna](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.fillna.html)
```
df.na.fill(50).show()
```

Aggregation: [groupby](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.groupBy.html)
```
df = df.withColumn('stock', df._c1 +5)
df2 == df.groupby('_c2').agg({'stock': 'min'}).show()
```
Example Functions:
- [abs](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.functions.abs.html#)
- [acos](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.functions.acos.html)
- [avg](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.functions.avg.html)
- [stddev](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.functions.stddev.html)
- ...

Query Plan: [explain](https://spark.apache.org/docs/3.2.0/api/python/reference/api/pyspark.sql.DataFrame.explain.html)
```
df2.explain()

df2.explain(True)

df2.explain(mode="formatted")
```
Modes:
- **simple**: Print only a physical plan.
- **extended**: Print both logical and physical plans.
- **codegen**: Print a physical plan and generated codes if they are available.
- **cost**: Print a logical plan and statistics if they are available.
- **formatted**: Split explain output into two sections: a physical plan outline and node details.


SQL:
```
df.createOrReplaceTempView('fruits')
df2 = spark.sql('select * from fruits')
```

## 9. Configuration

- `spark.speculation`