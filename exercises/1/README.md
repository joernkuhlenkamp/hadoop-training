# Exercise 1 - HDFS



## **HDFS**

#### - Show Version [[Docs: version](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#version)]
```
hdfs version
```

#### - Display Computed Hadoop Environment Variables [[Docs: envvars](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#envvars)]
```
hdfs envvars
```

#### - Show Group Information [[Docs: groups](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#groups)]
```
hdfs groups
```

#### - Check FS Health [[Docs: fsck](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#fsck)]
```
hdfs fsck /exercise
```

#### - Gets Configuration Information [[Docs: getconf](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#getconf)]
```
hdfs getconf -namenodes
```

#### - Get Class Path [[Docs: classpath](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#classpath)]
```
hdfs classpath
```




## **HDFS DFS**

### **Directory Structure**

#### - Create Directory [[Docs: -mkdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#mkdir)]
```
hdfs dfs -mkdir /exercise
```


#### - Remove Directory [[Docs: -rmdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#rmdir)]
```
hdfs dfs -rmdir /exercise
```
- Empty vs not empty


#### - Remove Files [[Docs: -rm]](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#rm) Options: `[-f] [-r |-R] [-skipTrash] [-safely]`
```
hdfs dfs -rm
```



### **File Transfer**

#### - Upload Lokal File [[Docs: -copyFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyFromLocal)]
```
hdfs dfs -copyFromLocal /exercises/1/data/imdb.csv /exercise/1/input
```

#### - Copy File to Client [[Docs: -copyToLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyToLocal)] Options: `[-ignorecrc] [-crc]`
```
hdfs dfs URI
```


#### - Move File [[Docs: -moveFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#moveFromLocal)]
```
hdfs dfs -moveFromLocal <local> <src>
```


#### - Not Implemented [[Docs: -moveToLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#moveToLocal)]
```
hdfs dfs -moveToLocal

# moveToLocal: Option '-moveToLocal' is not implemented yet.
```


#### - Copy Files from FS to DFS [[Docs: -put](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#put)] Options: `[-f] [-p] [-l] [-d]`
```
hdfs dfs -put /exercises/0/data/imdb.csv /
```


#### - Copy Files from Source to Destination [[Docs: -cp](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#cp)] Options: `[-f] [-p]`
```
hdfs dfs -cp URI [URI ...] <dest>
```


#### - Append local fileto target file [[Docs: -appendToFile](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#appendToFile)]
```
hdfs dfs -appendToFile <localsrc> ... <dst>
```


### **File Metadata**
#### - Show Information on File or Directory [[Docs: -ls](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#ls)] Options: [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [-e]
```
hdfs dfs -ls
```



#### - Copies Source Paths [[Docs: -cat](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#cat)]
```
hdfs dfs -cat URI
```


#### - Get Checksum Information [[Docs: -checksum](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#checksum)]
```
hdfs dfs -checksum URI
```


#### - Count #Directories, #Files, and #Bytes [[Docs: -count]()] Options: `[-q] [-h] [-v] [-x] [-t [<storage type>]] [-u] [-e]`
```
hdfs dfs -count 
```


#### - Displays Free Space [[Docs: -df](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#df)] Options: `[-h]`
```
hdfs dfs -df URI
```


#### - Displays Sizes of Files and Directories [[Docs: -du]()] Options: `[-s] [-h] [-v] [-x]`
```
hadoop fs -du /
```



### **Manage File Access Rights**

#### - Change Group Association [[Docs: -chgrp](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chgrp)] Options: `[-R]`
```
hdfs dfs -chgrp URI
```


#### - Change Permission [[Docs: -chmod](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chmod)] Options: `[-R]`
```
hdfs dfs -chmod URI
```


#### - Change Owner [[Docs: -chown](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chmod)] Options: `[-R]`
```
hdfs dfs -chown URI
```
