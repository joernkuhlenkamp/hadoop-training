# HIVE

## 1. Setup
Clone repository:
```
git clone https://github.com/big-data-europe/docker-hive.git
```

Change directory:
```
cd docker-hive
```

Start cluster:
```
docker compose up -d
```

Get Bash shell into container `hive-server`:
```
sudo docker compose exec hive-server bash
```

Exit container `hive-server`:
```
exit
```


## 2. First Steps

Enter Hive's shell:
```
hive
```

Create table `x`:
```
CREATE TABLE x (a INT);
```

Select all records from `x`:
```
SELECT * FROM x;
```

In general, line breaks and identation add no semantics:
```
SELECT * 
    FROM x;
```

Drop `x`:
```
DROP TABLE x;
```

Exit Hive's shell:
```
exit;
```

## 3. CLI
TODO

## Variables
Four namespaces: [`hivevar`, `hiveconf`, `system`, `env`]
Show and set variables using `SET`.

### Show Variables

Enter Hive's shell:
```
hive
```

Show variable `HOME` in namespace `env`:
```
set env:HOME;
```

Show all variables:
```
set;
```

Include Hadoop variables, e.g., `mapreduce` and `yarn`;
```
set -v;
```

Exit Hive's shell:
```
exit;
```

### Set Variables
Enter Hive's shell with additional variable `foo`:
```
hive --define foo=bar
```

Show `foo`:
```
set foo;

set hivevar:foo;
```

Set `foo`:
```
set foo=bar2;

set foo;
```

Prefix, e.g., `hivevar`, is optional and substitutes `--define`:
```
set hivevar:foo2=bar2;

set hivevar:foo2;
```

Change Hive's configuration options:
```
set hiveconf:hive.cli.print.current.db=true;
```

Namespace `env` is readonly in Hive's shell - set outside:
```
set env:HOME;

set env:HOME=/root2;
```

### Variable Substitution
Substitute prefixed variable:
```
create table toss1(i int, ${hivevar:foo} string);

describe toss1;
```

Substitute variable without prefix:
```
create table toss2(i2 int, ${foo} string);

describe toss2;
```

Cleanup:
```
drop table toss1;

drop table toss2;

describe toss2;
```

### Submitting Queries

#### **From String**
Submit query using option `-e`:
```
hive -e "set hiveconf:hive.cli.print.current.db"
```

Silent mode `-S` removes `OK` and `TIME` lines from output:
```
hive -S -e "set hiveconf:hive.cli.print.current.db"
```

Grep single values from configs:
```
hive -S -e "set"

hive -S -e "set" | grep hive.cli.print.current.db
```

#### **From File**
Save files using the suffixes `.q` or `.hql`:
```
hive -f /path/to/file/withqueries.hql
````

Use `source`within Hive's shell:
```
source /path/to/file/withqueries.hql;
````

### Hive's Shell Convenience Features
- Autocomplete commands using 'tab' key.
- Scroll through command history using 'up' and 'down' keys.
- Access HDFS within Hive's shell: `dfs -ls / ;`



## 4. Data Types and File Formats
### 4.1 Primitive Data Types
| Type     |  Size                            | Example |
|----------|----------------------------------|---------|
| TINYINT  | 1 byte signed integer.           | 1       |
| SMALLINT | 2 byte signed integer.           | 3       |
| INT      | 4 byte signed integer.           | 5       |
| BIGINT   | 8 byte signed integer.           | 7       |
| BOOLEAN  | Boolean                          | FALSE   |
| FLOAT    | Single precision floating point. | 8.23190 |
| DOUBLE   | Double precision floating point. | 8.23190 |
| STRING    | A sequence of characters.        | <ul><li>'turning'</li><li>"tables"</li></ul> |
| TIMESTAMP | Integer, float, or string.       | <ul><li>1327882394</li><li>1327882394.123456789</li><li> 2012-02-03 12:34:56.123456789</li></ul>       |
| BINARY    | Array of bytes                   | -       |

### 4.2 Collection Data Types
| Type      | 
|-----------|
| STRUCT    |
| MAP       |
| ARRAY     |

### 4.3 Default Delimiters
| Delimiter |  Description                       | Octal |
|-----------|------------------------------------|-------|
| \n        | Seperates records                  | NA    | 
| ^A        | Seperates fields/columns.          | \001  |
| ^B        | Seperates elements in collections. | \002  |
| ^C        | Seperates key and value in MAP.    | \003  | 

### 4.4 Example
```
CREATE TABLE employees (
    name STRING,
    salary FLOAT,
    subordinates ARRAY<STRING>,
    deductions MAP<STRING, FLOAT>,
    address STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
COLLECTION ITEMS TERMINATED BY '\002'
MAP KEYS TERMINATED BY '\003'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
```

Show result:
```
DESCRIBE employees;
```

Cleanup:
```
DROP TABLE employees;
```

Optional Exercises:
- How can we separate fields as in CSVs?
- How can we terminate keys with a double comma?
- How would youe model a desk with n drawers?
- Which string is valid "mystring" or 'mystring'?



## 5. Data Definition Language (DDL)

### 5.1 Databases
Databases in Hive are namespaces for tables. The default database is `default`.

Create database `financials`:
```
CREATE DATABASE financials;

CREATE DATABASE human_resources;
```

Describe database:
```
DESCRIBE DATABASE financials;
```

Avoid error if database exisits:
```
CREATE DATABASE IF NOT EXISTS financials;
```

List databases:
```
SHOW DATABASES;
```

Filter databases using regular expressions:
```
SHOW DATABASES LIKE 'h.*';
```

Changes database storage directory:
```
CREATE DATABASE financials
    LOCATION '/my/preferred/directory';
```

Add comment:
```
CREATE DATABASE financials
    COMMENT 'Holds all financial tables';
```

Add tags:
```
CREATE DATABASE financials
    WITH DBPROPERTIES ('creator' = 'Mark Moneybags', 'date' = '2012-01-02');
```

Change tags:
```
ALTER DATABASE financials SET DBPROPERTIES ('edited-by' = 'Joe Dba');
```

Select database:
```
USE financials;
```

Drop empty database:
```
DROP DATABASE IF EXISTS financials;
```

Drop database with all tables:
```
DROP DATABASE IF EXISTS financials CASCADE;
```

Optional exercises:
- How can you store a table under the HDFS root folder?
- Where does HIVE store databases per default?
- How would you add meta informations to a database?
- How does HIVE isolate databases in HDFS?



### 5.2 Tables

#### **5.2.1 Create Tables**
String columns:
```
CREATE TABLE IF NOT EXISTS testdb.string_table (
    name STRING
);

INSERT INTO testdb.string_table VALUES ("Frank Mayer");

SELECT * FROM testdb.string_table;
```

FLOAT columns:
```
CREATE TABLE IF NOT EXISTS testdb.float_table (
    salary FLOAT
);

INSERT INTO testdb.float_table VALUES (150000.50);

SELECT * FROM testdb.float_table;
```

Array column:
```
CREATE TABLE IF NOT EXISTS testdb.array_table (
    subordinates ARRAY<STRING>
);

INSERT INTO testdb.array_table select array("Super Star", "Best Greatson");

SELECT * FROM testdb.array_table;
```


```
CREATE TABLE IF NOT EXISTS mydb.employees (
    name            STRING COMMENT 'Employee name',
    salary          FLOAT COMMENT 'Employee salary',
    subordinates    ARRAY<STRING>
                    COMMENT 'Names of subordinates',
    deductions      MAP<STRING, FLOAT>
                    COMMENT 'Keys are deductions names, values are percentages',
    address         STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
                    COMMENT 'Home address')
    COMMENT 'Description of the table'
    TBLPROPERTIES ('creator'='me', 'created_at'='2012-01-02 10:00:00');
```

List all tables:
```
SHOW TABLES;
```

List tables for a database:
```
SHOW TABLES IN mydb;
```

Filter tables using a regular expression:
```
SHOW TABLES 'empl.*';
```

Extended details:
```
DESCRIBE EXTENDED mydb.employees;
```

Extended details in human readable format:
```
DESCRIBE FORMATTED mydb.employees;
```

Create external table that stores data in HDFS location '/exercises/3/external_dbs':
```
CREATE EXTERNAL TABLE IF NOT EXISTS images (
    i_id            STRING,
    i_typename      STRING,
    i_createdat     STRING,
    i_filetype      STRING,
    i_height        INT,
    i_identityid    STRING,
    i_key           STRING,
    i_name          STRING,
    i_p_id          STRING,
    i_size          INT,
    i_updatedat     STRING,
    i_width         INT

)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/exercises/3/external_dbs';
```

Optional exercises:
- Is `test-table' a valid table name?
- Does INSERT INTO TABLE work with column that are collection data types?

#### **5.2.2 Partition Tables**
```
CREATE TABLE employees (
    name STRING,
    salary FLOAT,
    subordinates ARRAY<STRING>,
    deductions MAP<STRING, FLOAT>,
    address STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
)
PARTITIONED BY (country STRING, state STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '|'
MAP KEYS TERMINATED BY ';'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
```

Create partitions during loading data:
```
LOAD DATA LOCAL INPATH '/exercises/3/data/employees-ca.csv' 
INTO TABLE employees
PARTITION (country = 'US', state = 'CA');

LOAD DATA LOCAL INPATH '/exercises/3/data/employees-ak.csv' 
INTO TABLE employees
PARTITION (country = 'US', state = 'AK');
```

Selects employees in the state of Illinois (`IL`) in the United States (`US`):
```
SELECT * FROM employees
WHERE country = 'US' AND state = 'IL';

SELECT * FROM employees
WHERE country = 'US' AND state = 'CA';
```

Strict mode prohibits queries of partitioned tables without a WHERE clause that
filters on partitions:
```
set hive.mapred.mode=strict;

SELECT e.name, e.salary FROM employees e LIMIT 100;

set hive.mapred.mode=nonstrict;

SELECT e.name, e.salary FROM employees e LIMIT 100;
```

Show partitions:
```
SHOW PARTITIONS employees;
```

Filter partitions by value:
```
SHOW PARTITIONS employees PARTITION(country='US');

SHOW PARTITIONS employees PARTITION(country='US', state='AK');

SHOW PARTITIONS employees PARTITION(country='US', state='AK');
```

Show partition keys using `DESCRIBE EXTENDED`:
```
DESCRIBE EXTENDED employees;
```

Partitioning in external tables allows to move partial data to other location:

Create external table `log_messages`: 
```
CREATE EXTERNAL TABLE IF NOT EXISTS log_messages (
    hms             INT, 
    severity        STRING, 
    server          STRING,
    process_id      INT,
    message         STRING
)
PARTITIONED BY (year INT, month INT, day INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';
```

Create partition:
```
ALTER TABLE log_messages ADD PARTITION(year = 2022, month = 1, day = 2) LOCATION 'hdfs://master_server/data/log_messages/2022/01/02';
```

Migrate partition to another storage system, e.g., S3:

Copy partition's data to new location:
```
hadoop distcp /data/log_messages/2022/12/02 s3n://ourbucket/logs/2022/12/02
```

Change partion's metadata to new location:
```
ALTER TABLE log_messages PARTITION(year = 2022, month = 12, day = 2) SET LOCATION 's3n://ourbucket/logs/2022/01/02';
```

Remove partition's data in old location.
```
hadoop fs -rmr /data/log_messages/2022/01/02
```

Show partion's location:
```
DESCRIBE EXTENDED log_messages PARTITION (year=2022, month=1, day=2);
```

Hive's offers different storage formats: `TEXTFILE`, `SEQUENCEFILE`, `RCFILE`

The default storage format is `TEXTFILE`, encoding data 
as alphanumeric characters. Each line becomes a record.
```
CREATE TABLE employees (
    name            STRING,
    salary          FLOAT,
    subordinates    ARRAY<STRING>,
    deductions      MAP<STRING, FLOAT>,
    address         STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
COLLECTION ITEMS TERMINATED BY '\002'
MAP KEYS TERMINATED BY '\003'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
```

Create table `ca_employees` with data from managed table `employees`:
```
CREATE TABLE ca_employees
AS SELECT name, salary, address 
FROM employees as se
WHERE se.state = 'CA';
```



#### **5.2.3 Drop Tables**
Drop table:
```
DROP TABLE IF EXISTS employees;
```

Set `fs.trash.interval` to positive number to enable trash feature.




#### **5.2.4 Alter Tables**

Rename table log_messages to logmsgs::
```
ALTER TABLE log_messages RENAME TO logmsgs;

ALTER TABLE logmsgs RENAME TO log_messages;
```

Adding partitions:
```
ALTER TABLE log_messages ADD IF NOT EXISTS
PARTITION (year = 2022, month = 7, day = 1) LOCATION '/logs/2022/07/01'
PARTITION (year = 2022, month = 7, day = 2) LOCATION '/logs/2022/07/02'
PARTITION (year = 2022, month = 7, day = 3) LOCATION '/logs/2022/07/03';
```

View partition details:
```
DESCRIBE EXTENDED log_messages PARTITION (year=2022, month=7, day=2);
```

Verify HDFS locations:
```
dfs -ls /logs/2022/07;
```

Change pointer on partion without mutate data:
```
ALTER TABLE log_messages PARTITION(year = 2022, month = 7, day = 1)
SET LOCATION 's3n://myapp/logs/2022/07/01';
```

Drop partition with (managed table) or without (external table) deleting data:
```
ALTER TABLE log_messages DROP IF EXISTS PARTITION(year = 2022, month = 7, day = 2);
```

Change column's name in schema:
```
ALTER TABLE log_messages
CHANGE COLUMN server node STRING;
```

Change column's position in schema:
```
ALTER TABLE log_messages
CHANGE COLUMN node server STRING
AFTER hms;
```

Add new column:
```
ALTER TABLE log_messages ADD COLUMNS (
    app_name STRING COMMENT "Application's name",
    session_id INT COMMENT "Session's id"
);
```

Add or change table properties:
```
ALTER TABLE log_messages SET TBLPROPERTIES (
    'notes' = 'The process id is no longer captured; this column is always NULL'
);
```




## 6. Data Manipulation Language (DML): Insert/Export

### 6.1 Insert Data

#### 6.1.1 **From File**

Load `LOCAL` data into table:
```
LOAD DATA LOCAL INPATH '/exercises/3/data/images.csv'
OVERWRITE INTO TABLE images
```

Load `LOCAL` data into partitioned table:
```
LOAD DATA LOCAL INPATH '/exercises/3/data/employees-ca.csv'
OVERWRITE INTO TABLE employees
PARTITION (country = 'US', state = 'CA');
```

#### 6.1.2 **From Table**
Insert records from table `staged_employees` into `employees`.

Define single static partitions :
```
INSERT OVERWRITE TABLE employees
PARTITION (country = 'US', state = 'OR')
SELECT * FROM staged_employees se
WHERE se.cnty = 'US' AND se.st = 'OR';
```

Scan input data only once for multiple static partitions:
```
FROM staged_employees se
    INSERT OVERWRITE TABLE employees
        PARTITION (country = 'US', state = 'OR')
        SELECT * WHERE se.cnty = 'US' AND se.st = 'OR'
    INSERT OVERWRITE TABLE employees
        PARTITION (country = 'US', state = 'CA')
        SELECT * WHERE se.cnty = 'US' AND se.st = 'CA'
    INSERT OVERWRITE TABLE employees
        PARTITION (country = 'US', state = 'IL')
        SELECT * WHERE se.cnty = 'US' AND se.st = 'IL';
```

Dynamic partitions allow for compact queries but must be enabled using configuration
properties. Configuration properties for dynamic partitions (see [DOCs](https://cwiki.apache.org/confluence/display/hive/configuration+properties)):
| Name                                     |  Default | Domain               |
|------------------------------------------|----------|----------------------|
| hive.exec.dynamic.partition              | `false`  | `false`, `true`      | 
| hive.exec.dynamic.partition.mode         | `strict` | `strict`, `nonstrict`|
| hive.exec.max.dynamic.partitions.pernode | `100`    | INT                  |
| hive.exec.max.dynamic.partitions         | `1000`   | INT                  | 
| hive.exec.max.created.files              | `100000` | INT                  |

Set configurations:
```
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.max.dynamic.partitions.pernode=1000;
```

Use dynamic partitions only:
```
INSERT OVERWRITE TABLE employees
PARTITION (country, state)
SELECT ..., se.cnty, se.st
FROM staged_employees se;
```

Combine static and dynamic partitions:
```
INSERT OVERWRITE TABLE employees
PARTITION (country = 'US', state)
SELECT ..., se.cnty, se.st
FROM staged_employees se
WHERE se.cnty = 'US';
```



### 6.2 Export Data
Copy files from HDFS:
```
hdfs dfs -cp source_path target_path
```

Export to local directory:
```
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/ca_employees'
SELECT name, salary, address
FROM employees
WHERE se.state = 'CA';
```
View result:
```
! ls /tmp/ca_employees;

! cat /tmp/payroll/000000_0
```

Partition export:
```
FROM staged_employees se
INSERT OVERWRITE DIRECTORY '/tmp/or_employees'
    SELECT * WHERE se.cty = 'US' and se.st = 'OR'
INSERT OVERWRITE DIRECTORY '/tmp/ca_employees'
    SELECT * WHERE se.cty = 'US' and se.st = 'CA'
INSERT OVERWRITE DIRECTORY '/tmp/il_employees'
    SELECT * WHERE se.cty = 'US' and se.st = 'IL';
``` 




## 7. Data Manipulation Language (DML): Queries

### 7.1 SELECT
```
CREATE TABLE employees (
    name STRING,
    salary FLOAT,
    subordinates ARRAY<STRING>,
    deductions MAP<STRING, FLOAT>,
    address STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
)
PARTITIONED BY (country STRING, state STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
COLLECTION ITEMS TERMINATED BY '\002'
MAP KEYS TERMINATED BY '\003'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
```

Projection:
```
SELECT name, salary FROM employees;
```

Table alias:
```
SELECT e.name, e.salary FROM employees e;
```

Hive returns collection data types as JSON.

Array:
```
SELECT name, subordinates FROM employees;
```

```
SELECT name, subordinates[0] FROM employees;
```

Map:
```
SELECT name, deductions FROM employees;
```

```
SELECT name, deductions["State Taxes"] FROM employees;
```

Struct:
```
SELECT name, address FROM employees;
```

```
SELECT name, address.city FROM employees;
```



#### 7.1.2 **Process Values**
Example:
```
SELECT upper(name), salary, deductions["Federal Taxes"],
    round(salary * (1 - deductions["Federal Taxes"])) FROM employees;
```

Arithmetic `+`, `-`, `*`, `/`, `%`, `&`, `|`, `^`, `~`. Binary operators return
type with larger domain.

Select math functions:
- BIGINT: `round(d)`
- DOUBLE: `round(d, N)`
- BIGINT: `floor(d)`
- BIGINT: `ceil(d)`
- DOUBLE: `rand()`
- DOUBLE: `exp(d)`
- DOUBLE: `ln(d)`
- DOUBLE: `log10(d)`
- DOUBLE: `log2(d)`
- DOUBLE: `log(base,d)`
- DOUBLE: `pow(d, p)`
- DOUBLE: `sqrt(d)`
- STRING: `bin(i)`
- STRING: `hex(i)`
- STRING: `hex(str)`
- STRING: `unhex(i)`
- STRING: `conv(i, from_base, to_base)`
- STRING: `conv(str, from_base, to_base)`
- DOUBLE: `abs(d)`
- INT:    `pmod(i1, i2)`
- DOUBLE: `pmod(d1, d2)`
- DOUBLE: `sin(d)`
- DOUBLE: `asin(d)`
- DOUBLE: `cos(d)`
- DOUBLE: `acos(d)`
- DOUBLE: `tan(d)`
- DOUBLE: `atan(d)`
- DOUBLE: `degrees(d)`
- DOUBLE: `radians(d)`
- INT: `positive(i)`
- DOUBLE: `positive(d)`
- INT: `negative(i)`
- DOUBLE: `negative(d)`
- FLOAT: `sign(d)`
- DOUBLE: `e()`
- DOUBLE: `pi()`

Select aggregation functions:
- BIGINT: `count(*)`
- BIGINT: `count(expr)`
- BIGINT: `count(DISTINCT expr[, expr_.])`
- DOUBLE: `sum(col)`
- DOUBLE: `sum(DISTINCT col)`
- DOUBLE: `avg(col)`
- DOUBLE: `avg(DISTINCT col)`
- DOUBLE: `min(col)`
- DOUBLE: `max(col)`
- DOUBLE: `variance(col),`
- DOUBLE: `var_samp(col)`
- DOUBLE: `stddev_pop(col)`
- DOUBLE: `stddev_samp(col)`
- DOUBLE: `covar_pop(col1, col2)`
- DOUBLE: `covar_samp(col1, col2)`
- DOUBLE: `corr(col1, col2)`
- DOUBLE: `percentile(int_expr, p)`
- ARRAY<DOUBLE>: `percentile(int_expr,[p1, ...])`
- DOUBLE: `percentile_approx(int_expr,p , NB)`
- DOUBLE: `percentile_approx(int_expr,[p1, ...] , NB)`
- ARRAY<STRUCT{'x','y'}>: `histogram_numeric(col, NB)`
- ARRAY: `collect_set(col)`

Enable aggregation during map phase:
```
SET hive.map.aggr=true;
```
Restore default:
```
SET hive.map.aggr=false;
```

Select table generating functions:
- N rows: `explode(array)`
- N rows: `explode(map)`
- tuple: `json_tuple(jsonStr, p1, p2, ...,pn)`
- tuple: `parse_url_tuple(url, part name1, partname2, ..., partna meN) where N >= 1`
- N rows: `stack(n, col1, ..., colM)`



Select other functions:
- BOOLEAN: `test in(val1, val2, ...)`
- INT: `length(s)`
- STRING: `reverse(s)`
- STRING: `concat(s1, s2, ...)`
- STRING: `concat_ws(separator, s1, s2,...)`
- STRING: `substr(s, start_index)`
- STRING: `substr(s, int start, int length)`
- STRING: `upper(s)`
- STRING: `lower(s)`
- STRING: `trim(s)`
- STRING: `ltrim(s)`
- STRING: `rtrim(s)`
- STRING: `regexp_replace(s, regex, replacement)`
- STRING: `regexp_extract(subject, regex_pattern, index)`
- STRING: `parse_url(url, partname, key)`
- int: `sie(map<K.V>)`
- int: `size(array<T>)`
- value of type: `cast(<expr> as <type>)`
- STRING: `from_unixtime(int unixtime)`
- STRING: `to_date(timestamp)`
- INT: `year(timestamp)`
- INT: `month(timestamp)`
- INT: `day(timestamp)` 
- STRING: `get_json_object(json_string, path)` 
- STRING: `space(n)`
- STRING: `repeat(s, n)`
- STRING: `ascii(s)`
- STRING: `lpad(s, len, pad)`
- STRING: `rpad(s, len, pad)`
- ARRAY<STRING>: `split(s, pattern)`
- INT: `find_in_set(s, commaSeparateString)`
- INT: `locate(substr, str, pos])`
- INT: `instr(str, substr)`
- MAP<STRING,STRING>: `str_to_map(s, delim1, delim2)`
- ARRAY<ARRAY<STRING>>: `sentence(s, lang, locale)`


#### 7.1.3 **Limit**
```
SELECT 
    upper(name),
    salary,
    deductions["Federal Taxes"],
    round(salary * (1 - deductions["Federal Taxes"])) 
FROM employees
LIMIT 2;
```

### 7.1.4 **Column Alias**
```
SELECT 
    upper(name),
    salary,
    deductions["Federal Taxes"] as fed_taxes,
    round(salary * (1 - deductions["Federal Taxes"])) as salary_minus_fed_taxes
FROM employees
LIMIT 2;
```

### 7.1.5 **Nested Select**
```
FROM (
    SELECT
        upper(name) as name,
        salary,
        deductions["Federal Taxes"] as fed_taxes,
        round(salary * (1 - deductions["Federal Taxes"])) as salary_minus_fed_taxes
    FROM employees
) e
SELECT e.name, e.salary_minus_fed_taxes
WHERE e.salary_minus_fed_taxes > 70000;
```

### 7.1.6 **Conditions**
```
SELECT name, salary,
    CASE
        WHEN salary < 50000.0 THEN 'low'
        WHEN salary >= 50000.0 AND salary < 70000.0 THEN 'middle'
        WHEN salary >= 70000.0 AND salary < 100000.0 THEN 'high'
    ELSE 'very high'
END AS bracket FROM employees;
```


### 7.2 WHERE
```
SELECT * FROM employees
WHERE country = 'US' AND state = 'CA';
```

```
SELECT name, salary, deductions["Federal Taxes"],
    salary * (1 - deductions["Federal Taxes"])
FROM employees
WHERE round(salary * (1 - deductions["Federal Taxes"])) > 70000;
```

```
SELECT e.* FROM
(SELECT name, salary, deductions["Federal Taxes"] as ded,
    salary * (1 - deductions["Federal Taxes"]) as salary_minus_fed_taxes 
FROM employees) e
WHERE round(e.salary_minus_fed_taxes) > 70000;
```

Predicate operators:
`=`, `!=`, `<`, `<=`, `>`, `>=`, `IS NULL`, `IS NOT NULL`, `LIKE`, `RLIKE`

Floating point comparison:
```
SELECT name, salary, deductions['Federal Taxes']
FROM employees WHERE deductions['Federal Taxes'] > 0.2;
```

```
SELECT name, salary, deductions['Federal Taxes']
FROM employees
WHERE deductions['Federal Taxes'] > cast(0.2 AS FLOAT);
```

LIKE
```
SELECT name, address.street
FROM employees
WHERE address.street LIKE '%Ave.';
```

```
SELECT name, address.city
FROM employees
WHERE address.city LIKE 'O%';
```

```
SELECT name, address.street
FROM employees
WHERE address.street LIKE '%Chi%';
```

RLIKE
```
SELECT name, address.street
FROM employees
WHERE address.street RLIKE '.*(Chicago|Ontario).*';
```

### 7.3 GROUP BY
```
SELECT year(ymd), avg(price_close)
FROM stocks
WHERE exchange = 'NASDAQ' AND symbol = 'AAPL'
GROUP BY year(ymd);
```

HAVING
```
SELECT year(ymd), avg(price_close) 
FROM stocks
WHERE exchange = 'NASDAQ' AND symbol = 'AAPL'
GROUP BY year(ymd)
HAVING avg(price_close) > 50.0;
```

### 7.4 JOINS
```
SELECT a.ymd, a.price_close, b.price_close
FROM stocks a JOIN stocks b ON a.ymd = b.ymd
WHERE a.symbol = 'AAPL' AND b.symbol = 'IBM';
```

```
CREATE EXTERNAL TABLE IF NOT EXISTS dividends (
    ymd STRING,
    dividend FLOAT
)
PARTITIONED BY (exchange STRING, symbol STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
```

```
SELECT s.ymd, s.symbol, s.price_close, d.dividend
FROM stocks s JOIN dividends d ON s.ymd = d.ymd AND s.symbol = d.symbol
WHERE s.symbol = 'AAPL';
```

```
SELECT a.ymd, a.price_close, b.price_close , c.price_close
FROM stocks a JOIN stocks b ON a.ymd = b.ymd
              JOIN stocks c ON a.ymd = c.ymd
WHERE a.symbol = 'AAPL' AND b.symbol = 'IBM' AND c.symbol = 'GE';
```


LEFT OUTER JOIN
```
SELECT s.ymd, s.symbol, s.price_close, d.dividend
FROM stocks s LEFT OUTER JOIN dividends d ON s.ymd = d.ymd AND s.symbol = d.symbol
WHERE s.symbol = 'AAPL';
```

RIGHT OUTER JOIN
```
SELECT s.ymd, s.symbol, s.price_close, d.dividend
FROM dividends d RIGHT OUTER JOIN stocks s ON d.ymd = s.ymd AND d.symbol = s.symbol
WHERE s.symbol = 'AAPL';
```

FULL OUTER JOIN
```
SELECT s.ymd, s.symbol, s.price_close, d.dividend
FROM dividends d FULL OUTER JOIN stocks s ON d.ymd = s.ymd AND d.symbol = s.symbol
WHERE s.symbol = 'AAPL';
```

LEFT SEMI-JOIN
```
SELECT s.ymd, s.symbol, s.price_close
FROM stocks s LEFT SEMI JOIN dividends d ON s.ymd = d.ymd AND s.symbol = d.symbol;
```

Cartesian Product JOIN
```
SELECTS * FROM stocks JOIN dividends;
```

Map-side Joins

set hive.auto.convert.join=true;
hive.mapjoin.smalltable.filesize=25000000

set hive.input.format=org.apache.hadoop.hive.ql.io.BucketizedHiveInputFormat; set hive.optimize.bucketmapjoin=true;
set hive.optimize.bucketmapjoin.sortedmerge=true;

```
set hive.auto.convert.join=true;

SELECT s.ymd, s.symbol, s.price_close, d.dividend
    FROM stocks s JOIN dividends d ON s.ymd = d.ymd AND s.symbol = d.symbol
    WHERE s.symbol = 'AAPL';
```

ORDER BY and SORT BY

Slow global ordering:
```
SELECT s.ymd, s.symbol, s.price_close FROM stocks s
ORDER BY s.ymd ASC, s.symbol DESC;
```

Faster local ordering:
```
SELECT s.ymd, s.symbol, s.price_close FROM stocks s
SORT BY s.ymd ASC, s.symbol DESC;
```

DISTRIBUTE BY with SORT BY
```
SELECT s.ymd, s.symbol, s.price_close
FROM stocks s
DISTRIBUTE BY s.symbol
SORT BY s.symbol ASC, s.ymd ASC;
```

CLUSTER BY
```
SELECT s.ymd, s.symbol, s.price_close
FROM stocks s
CLUSTER BY s.symbol;
```

Casting
```
SELECT name, salary FROM employees
WHERE cast(salary AS FLOAT) < 100000.0;
````

Sampling
TODO




## 8. Views




## 9. Indexes




## 10. Schema Design




## 11. Tuning




## 12. Case Studies
