from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import os

# Define the schema
schema = StructType([
    StructField("ts", DoubleType(), True),
    StructField("device", StringType(), True),
    StructField("co", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("lpg", DoubleType(), True),
    StructField("smoke", DoubleType(), True),
    StructField("temp", DoubleType(), True)
])

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaIoTConsumer") \
    .getOrCreate()

# Read from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", os.environ['KAFKA_BOOTSTRAP_SERVERS']) \
    .option("subscribe", "iot_telemetry") \
    .load()

# Convert the binary value column to string and apply schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write the data to console (or any other sink)
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()

