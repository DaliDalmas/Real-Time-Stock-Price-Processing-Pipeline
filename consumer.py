import spark
df = spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("subscribe", "demo")\
        .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

