from time import sleep
from json import dumps
from kafka import KafkaProducer


def custom_partitioner(key, all_partitions, available):
    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """
    print("The key is  : {}".format(key))
    print("All partitions : {}".format(all_partitions))
    print("After decoding of the key : {}".format(key.decode('UTF-8')))
    return int(key.decode('UTF-8')) % len(all_partitions)


producer = KafkaProducer(bootstrap_servers=['localhost:9092'], partitioner=custom_partitioner)
topic_name = 'hello_world4'

producer.send(topic_name, key=b'3', value=b'Hello Partitioner')
producer.send(topic_name, key=b'2', value=b'Hello Partitioner123')
producer.send(topic_name, key=b'369', value=b'Hello Partitioner')
producer.send(topic_name, key=b'301', value=b'Hello Partitioner')
