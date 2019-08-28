#!/bin/bash

##统计hive数仓所有表的文件数量，但不包括外部表和映射表

warehouse=/apps/hive/warehouse/tablespace
echo " For partition table show the directories numbers, not file numbers"

hadoop fs -ls $warehouse |  awk '{print $8}' | grep -v '^$'| while read database_path
do
    hadoop fs -ls $database_path | awk '{print $8}' | grep -v '^$' | while read table_path
    do
        database=`basename ${database_path} | sed 's/.db$//g'`
        if [[ x$database != x ]]
        then
            echo "${database}.`basename ${table_path}` : `hadoop fs -ls $table_path | wc -l`"
        fi
    done
done
