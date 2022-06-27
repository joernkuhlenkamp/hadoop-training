# Exercise 1 - HDFS
## **1. HDFS Basics**

#### - Show version: [version](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#version)
```
hdfs version
```

#### - Display environment variables [envvars](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#envvars)
```
hdfs envvars
```

#### - Show group information [groups](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#groups)
```
hdfs groups
```

#### - Check FS health [fsck](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#fsck)
```
hdfs fsck /
hdfs fsck / -files -blocks
```

#### - Gets configuration information [getconf](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#getconf)
```
hdfs getconf -namenodes
```

#### - Get class path [classpath](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html#classpath)
```
hdfs classpath
```




## **2. HDFS DFS**

### **2.1 Directory Structure**

#### - Create directory: [-mkdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#mkdir) Options: [-p]
```
hdfs dfs -mkdir /exercise
hdfs dfs -mkdir /exercise/1
hdfs dfs -mkdir /exercise/1/input
```

```
hdfs dfs -mkdir -p /exercise/1/test/with/subfolder
```


#### - Remove directory [-rmdir](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#rmdir) Options: `[--ignore-fail-on-non-empty]`
```
hdfs dfs -rmdir /exercise/1/test/with/subfolder

# will fail with `Directory is not empty`
hdfs dfs -rmdir /exercise/1/test

# ignores fails
hdfs dfs -rmdir --ignore-fail-on-non-empty /exercise/1/test
```


### **2.2 File Transfer**

#### - Upload lokal file [-copyFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyFromLocal) Options: `[-p] [-f] [-l] [-d]`
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

# does this still work?
hdfs dfs -copyFromLocal -f -l /exercises/1/data/2022-06-03.log /exercise/1/input/2022-06-03-readonly.log
```

#### - Copy File to Client [-copyToLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#copyToLocal) Options: `[-ignorecrc] [-crc]`
```
# try copy to not existing local folder
hdfs dfs -copyToLocal /exercise/1/input/2022-06-03-readonly.log /exercise/1/output/

# create local folder
mkdir -p /exercise/1/output

# try copy to existing local folder
hdfs dfs -copyToLocal /exercise/1/input/2022-06-03-readonly.log /exercise/1/output/
```


#### - Move file from client [-moveFromLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#moveFromLocal)
```
# 
ls -lsa exercise/1/output

# Move
hdfs dfs -moveFromLocal /exercise/1/output/2022-06-03-readonly.log  /exercise/1/input/2022-06-03-part-2.log

# 
ls -lsa exercise/1/output
```


#### - Not implemented [-moveToLocal](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#moveToLocal)
```
# moveToLocal: Option '-moveToLocal' is not implemented yet.
hdfs dfs -moveToLocal /exercise/1/input/2022-06-03-part-2.log /exercise/1/output/2022-06-03-readonly.log
```


#### - Copy files from FS to DFS [Docs: -put](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#put) Options: `[-f] [-p] [-l] [-d]`
```
hdfs dfs -put /exercises/1/data/2022-06-03-wrong.log /exercise/1/input
```


#### - Copy files from source to destination [-cp](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#cp) Options: `[-f] [-p]`
```
hdfs dfs -cp /exercise/1/input/2022-06-03.log file:///exercise/1/output/
```


#### - Append local file to target file [-appendToFile](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#appendToFile)
```
hdfs dfs -appendToFile /exercises/1/data/2022-06-03-missing.log /exercise/1/input/2022-06-03-part.log
```

#### - Remove files [-rm](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#rm) Options: `[-f] [-r |-R] [-skipTrash] [-safely]`
```
hdfs dfs -rm /exercise/1/input/2022-06-03-wrong.log
```

### **2.3 File Metadata**
#### - Show information on file or directory: [-ls](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#ls) Options: [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [-e]
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



#### - Copies source paths to STDOUT: [-cat](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#cat)
```
hdfs dfs -cat /exercise/1/input/2022-06-03-readonly.log
```


#### - Get checksum information [-checksum](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#checksum)
```
hdfs dfs -checksum /exercise/1/input/2022-06-03-readonly.log
```


#### - Count #directories, #files, and #bytes: [-count]() Options: `[-q] [-h] [-v] [-x] [-t [<storage type>]] [-u] [-e]`
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


#### - Displays free space: [-df](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#df) Options: `[-h]`
```
hdfs dfs -df /

#human readable
hdfs dfs -df /
```


#### - Displays sizes of files and directories: [-du](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#du) Options: `[-s] [-h] [-v] [-x]`
```
hdfs dfs -du /exercise/1/input

# human readable
hdfs dfs -du -h /exercise/1/input

# aggregate file sizes
hdfs dfs -du -s -h /exercise/1/input

# display column headers
hdfs dfs -du -s -v /exercise/1/input
```



### **2.4 Manage File Access Rights**

#### - Change group: [-chgrp](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chgrp) Options: `[-R]`
```
hdfs dfs -chgrp URI
```


#### - Change permission: [-chmod](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chmod) Options: `[-R]`
```
hdfs dfs -chmod URI
```


#### - Change owner: [-chown](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#chmod) Options: `[-R]`
```
hdfs dfs -chown URI
```

### **3. Trade-offs**

#### - Replication factor: [-setrep](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#setrep) Options: `[-R] [-w]`
```
hdfs dfs -setrep 1 /exercise/1/input/2022-06-03.log
```