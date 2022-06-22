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
hdfs fsck /
hdfs fsck / -files -blocks
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

#### - Create Directory [[Docs: -mkdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#mkdir)] Options: [-p]
```
hdfs dfs -mkdir /exercise
hdfs dfs -mkdir /exercise/1
hdfs dfs -mkdir /exercise/1/input
```

```
hdfs dfs -mkdir -p /exercise/1/test/with/subfolder
```


#### - Remove Directory [[Docs: -rmdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#rmdir)] Options: `[--ignore-fail-on-non-empty]`
```
hdfs dfs -rmdir /exercise/1/test/with/subfolder

# will fail with `Directory is not empty`
hdfs dfs -rmdir /exercise/1/test

# ignores fails
hdfs dfs -rmdir --ignore-fail-on-non-empty /exercise/1/test
```


### **File Transfer**

#### - Upload Lokal File [[Docs: -copyFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyFromLocal)] Options: `[-p] [-f] [-l] [-d]`
```
hdfs dfs -copyFromLocal /exercises/1/data/2022-06-03-wrong.log /exercise/1/input/2022-06-03.log

# inspect file input locally
cat /exercises/1/data/2022-06-03-wrong.log

# overwrite file: fails with `File exists
hdfs dfs -copyFromLocal /exercises/1/data/2022-06-03.log /exercise/1/input

# overwrite file with `-f`option
hdfs dfs -copyFromLocal -f /exercises/1/data/2022-06-03.log /exercise/1/input

# inspect file
hdfs dfs -cat /exercise/1/input/2022-06-03.log
```

```
# lazy persistence on DataNode.
hdfs dfs -copyFromLocal -f -l /exercises/1/data/2022-06-03.log /exercise/1/input
```

```
# inspect access
ls -lsa /exercises/1/data

# set strict readonly
chmod 444 /exercises/1/data/2022-06-03-readonly.log

# preserve access rights
hdfs dfs -copyFromLocal -f -p /exercises/1/data/2022-06-03-readonly.log /exercise/1/input

# advanced question: why does this still work?
hdfs dfs -copyFromLocal -f -l /exercises/1/data/2022-06-03.log /exercise/1/input/2022-06-03-readonly.log
```

#### - Copy File to Client [[Docs: -copyToLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyToLocal)] Options: `[-ignorecrc] [-crc]`
```
# try copy to not existing local folder
hdfs dfs -copyToLocal /exercise/1/input/2022-06-03-readonly.log /exercise/1/output/

# create local folder
mkdir -p /exercise/1/output

# try copy to existing local folder
hdfs dfs -copyToLocal /exercise/1/input/2022-06-03-readonly.log /exercise/1/output/
```


#### - Move File from Client [[Docs: -moveFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#moveFromLocal)]
```
# 
ls -lsa exercise/1/output

# Move
hdfs dfs -moveFromLocal /exercise/1/output/2022-06-03-readonly.log  /exercise/1/input/2022-06-03-part-2.log

# 
ls -lsa exercise/1/output
```


#### - Not Implemented [[Docs: -moveToLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#moveToLocal)]
```
# moveToLocal: Option '-moveToLocal' is not implemented yet.
hdfs dfs -moveToLocal /exercise/1/input/2022-06-03-part-2.log /exercise/1/output/2022-06-03-readonly.log
```


#### - Copy Files from FS to DFS [[Docs: -put](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#put)] Options: `[-f] [-p] [-l] [-d]`
```
hdfs dfs -put /exercises/1/data/2022-06-03-wrong.log /exercise/1/input
```


#### - Copy Files from Source to Destination [[Docs: -cp](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#cp)] Options: `[-f] [-p]`
```
hdfs dfs -cp /exercise/1/input/2022-06-03.log file:///exercise/1/output/
```


#### - Append local fileto target file [[Docs: -appendToFile](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#appendToFile)]
```
hdfs dfs -appendToFile /exercises/1/data/2022-06-03-missing.log /exercise/1/input/2022-06-03-part.log
```

#### - Remove Files [[Docs: -rm]](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#rm) Options: `[-f] [-r |-R] [-skipTrash] [-safely]`
```
hdfs dfs -rm /exercise/1/input/2022-06-03-wrong.log
```

### **File Metadata**
#### - Show Information on File or Directory [[Docs: -ls](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#ls)] Options: [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [-e]
```
hdfs dfs -ls /

# display the paths of files and directories only.
hdfs dfs -ls -C /

# directories are listed as plain files.
hdfs dfs -ls -d /

# directories are listed as plain files.
hdfs dfs -ls -h /exercise/1/input

# recursively list subdirectories encountered.
hdfs dfs -ls -R /

# sort output by modification time (most recent first).
hdfs dfs -ls -R -t /

# sort output by file size.
hdfs dfs -ls -S /

# reverse sort order
hdfs dfs -ls -r /
```



#### - Copies Source Paths to STDOUT [[Docs: -cat](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#cat)]
```
hdfs dfs -cat /exercise/1/input/2022-06-03-readonly.log
```


#### - Get Checksum Information [[Docs: -checksum](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#checksum)]
```
hdfs dfs -checksum /exercise/1/input/2022-06-03-readonly.log
```


#### - Count #Directories, #Files, and #Bytes [[Docs: -count]()] Options: `[-q] [-h] [-v] [-x] [-t [<storage type>]] [-u] [-e]`
```
# DIR_COUNT, FILE_COUNT, CONTENT_SIZE, PATHNAME
hdfs dfs -count /

# show quotas
# QUOTA, REMAINING_QUOTA, SPACE_QUOTA, REMAINING_SPACE_QUOTA, DIR_COUNT, FILE_COUNT, CONTENT_SIZE, PATHNAME
hdfs dfs -count -q /

# show quotas and usage only
# QUOTA, REMAINING_QUOTA, SPACE_QUOTA, REMAINING_SPACE_QUOTA, PATHNAME
hdfs dfs -count -u /

# human readable
hdfs dfs -count -u -h /

# display header line
hdfs dfs -count -h -v /
```


#### - Displays Free Space [[Docs: -df](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#df)] Options: `[-h]`
```
hdfs dfs -df /

#human readable
hdfs dfs -df /
```


#### - Displays Sizes of Files and Directories [[Docs: -du]()] Options: `[-s] [-h] [-v] [-x]`
```
hdfs dfs -du /exercise/1/input

# human readable
hdfs dfs -du -h /exercise/1/input

# aggregate file sizes
hdfs dfs -du -s -h /exercise/1/input

# display column headers
hdfs dfs -du -s -v /exercise/1/input
```



### **Manage File Access Rights**

#### - Change Group [[Docs: -chgrp](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chgrp)] Options: `[-R]`
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
