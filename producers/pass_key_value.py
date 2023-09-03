from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
topic_name = 'hello_world2'
producer.send(topic_name, key=b'foo', value=b'bar')

# Note :key & value serialization we are doing while publishing the message itself ,
# so explicitly not mentioning the key or value serializer

producer.send(topic_name, key=b'foo', value=b'bar')
producer.close()
