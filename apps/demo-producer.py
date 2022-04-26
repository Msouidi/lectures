import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='192.168.33.13:9092')
with open('data/demo_data.csv') as file:
    while line := file.readline(): 
        producer.send('demo', line.rstrip().encode('utf-8'))
        time.sleep(1)

    