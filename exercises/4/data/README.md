# (Py)Spark

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

## 3. 

### 3.1 Standalone Application
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


## 4. Data Types and File Formats

Persist RDD:
```
cherry_lines.persist
```

### Creating RDDs

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

### Transformations vs Actions


#### Transformations
```
lines = sc.textFile("/fruits.csv")
cherry_lines = lines.filter(lambda line: 'cherry' in line)
melone_lines = lines.filter(lambda line: 'melone' in line)
cocktail_fruits = cherry_lines.union(melone_lines)

cocktail_fruits.count()
cocktail_fruits.first()
```
What is the execution DAG?

Create example rdd:
```
rdd = sc.parallelize([1,2,3,3])
```

```
map_rdd = rdd.map(x => x + 1)
```

```
flat_map_rdd = flatMap(lambda x: (x, x+1))
```

```
filter_rdd = rdd.filter(lambda x: x != 3)
```

```
distinct_rdd=rdd.distinct()
```

```
sample_rdd = rdd.sample(False, 0.5)
```

```
rdd1=sc.parallelize([1,2,3])
rdd2=sc.parallelize([3,4,5])
```

```
union_rdd = rdd1.union(rdd2)
```

```
intersection_rdd = rdd1.intersection(rdd2)
```

```
substract_rdd = rdd1.subtract(rdd2)
```

```
cartesian_rdd = rdd1.cartesian(rdd2)
```

#### Actions

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



#### **Persisting**
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