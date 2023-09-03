from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("Kafka Pyspark Streaming Learning")
    .master("local[*]")
    .getOrCreate()
)

KAFKA_TOPIC_NAME = "hello_world1"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
KAFKA_MESSAGE_SCHEMA = StructType([
    StructField('number', IntegerType(), True)
])

sampleDataframe = (
    spark.read.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
    .option("subscribe", KAFKA_TOPIC_NAME)
    .option("startingOffsets", "earliest")
    .load()
)

df = (
    sampleDataframe
    .withColumn('str_value', f.col('value').cast('string'))
    .withColumn('json_col', f.from_json(f.col('str_value'), KAFKA_MESSAGE_SCHEMA))
    .withColumn('number', f.col('json_col.number'))
)

df.show(truncate=False)

# root
#  |-- key: binary (nullable = true)
#  |-- value: binary (nullable = true)
#  |-- topic: string (nullable = true)
#  |-- partition: integer (nullable = true)
#  |-- offset: long (nullable = true)
#  |-- timestamp: timestamp (nullable = true)
#  |-- timestampType: integer (nullable = true)
