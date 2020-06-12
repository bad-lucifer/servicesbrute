from kafka import KafkaProducer
import json
import configparser


'''
    producer
    写入json数据需加上value_serializer参数
'''


def send_to_kafka(data):

    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")

    topic = config['services']['name']

    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        bootstrap_servers= config['kafka']['servers']
    )
    producer.send(topic, data)
    producer.close()
