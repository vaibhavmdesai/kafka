from kafka import KafkaConsumer
import json


consumer = KafkaConsumer('hello_world4'
                         ,bootstrap_servers = ['localhost:9092']
                         ,value_deserializer = lambda m: json.loads(m.decode('utf-8'))
                         ,group_id = 'demo112215sgtrjwrykvjh'
                         ,auto_offset_reset = 'earliest'
                         )


for message in consumer:
    print(message)