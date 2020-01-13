import findspark
import os
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars C:\spark\spark-2.4.4-bin-hadoop2.7\jars\postgresql-42.2.9.jar pyspark-shell'
os.environ['SPARK_HOME'] = 'C:\spark\spark-2.4.4-bin-hadoop2.7'
os.environ['SPARK_CLASSPATH'] = 'C:\spark\spark-2.4.4-bin-hadoop2.7\jars\postgresql-42.2.9.jar'

from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, udf 
from pyspark.sql.types import DateType

spark = SparkSession.builder.appName("Basic JDBC pipeline").getOrCreate()
            #.config("spark.driver.extraClassPath", "file:\\\C:\spark\spark-2.4.4-bin-hadoop2.7\jars\postgresql-42.2.9.jar") \
            #.config("spark.executor.extraClassPath", "file:\\\C:\spark\spark-2.4.4-bin-hadoop2.7\jars\postgresql-42.2.9.jar") \
            #.getOrCreate()
findspark.init('C:\spark\spark-2.4.4-bin-hadoop2.7')
#spark = SparkSession \
#    .builder \
#    .appName("Basic JDBC pipeline") \
#    .getOrCreate()

    #.config("spark.driver.extraClassPath", "/Users⁩/fmezaoba⁩/Documents/Coding⁩/BD⁩/1/postgresql-42.1.4.jar") \
    #.config("spark.executor.extraClassPath", "/Users⁩/fmezaoba⁩/Documents/Coding⁩/BD⁩/1/postgresql-42.1.4.jar") \

# Reading single DataFrame in Spark by retrieving all rows from a DB table.
url = "jdbc:postgresql://192.168.19.133/postgres"
table = "transactions"
db_properties={}
db_properties['username'] = "sergio"
db_properties['password'] = "postgres"
#db_properties['driver'] = "org.postgresql.Driver"

#df = spark.read.jdbc(url=url,table=table,properties=db_properties)

df = spark \
    .read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.19.133/postgres") \
    .option("user", "sergio") \
    .option("password", "postgres") \
    .option("dbtable", "transactions") \
    .load()


df.show()