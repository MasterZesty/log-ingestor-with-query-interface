from typing import Optional, Dict, Any
import json
from datetime import datetime
import logging
import sys
from confluent_kafka import Consumer, KafkaException, KafkaError

try:
    from .query_interface import Database
except:
    from query_interface import Database

class KafkaLogConsumer:
    def __init__(self, user: str, password: str, host: str, port: int, database_name: str, kafka_bootstrap_servers: str, consumer_group: str, kafka_topic: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database_name
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.consumer_group = consumer_group
        self.kafka_topic = kafka_topic
        self.db = Database(user, password, host, port, database_name)
        self.db.create_tables()

    def consume_and_store_logs(self) -> None:
        conf = {
            'bootstrap.servers': self.kafka_bootstrap_servers,
            'group.id': self.consumer_group,
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(conf)
        consumer.subscribe([self.kafka_topic])

        try:
            while True:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    else:
                        raise KafkaException(msg.error())
                else:
                    log_data = json.loads(msg.value().decode('utf-8'))
                    # print(log_data)
                    # check 1: Convert ISO 8601 timestamp to MySQL DateTime format
                    parsed_timestamp = datetime.strptime(log_data.get('timestamp'), '%Y-%m-%dT%H:%M:%SZ')
                    mysql_timestamp = parsed_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                    new_log = {
                        'level':log_data.get('level'),
                        'message':log_data.get('message'),
                        'resourceId':log_data.get('resourceId'),
                        'timestamp':mysql_timestamp,
                        'traceId':log_data.get('traceId'),
                        'spanId':log_data.get('spanId'),
                        'commit':log_data.get('commit'),
                        'parentResourceId':log_data.get('metadata', {}).get('parentResourceId')
                    }
                    
                    self.db.insert_log(new_log)  # Use the insert_log method from your Database class

        except KeyboardInterrupt:
            logging.info(f'Aborted by user')
            sys.stderr.write('%% Aborted by user\n')

        finally:
            consumer.close()

if __name__ == '__main__':
    consumer = KafkaLogConsumer(
        user='krishna',
        password='krishna',
        # host='mysql-write',
        host='localhost',
        port=3306,
        database_name='log_ingestor_db',
        # kafka_bootstrap_servers='kafka1:19092',
        kafka_bootstrap_servers='localhost:9092',
        consumer_group='log_consumer_group',
        kafka_topic='log-ingestor'
    )
    consumer.consume_and_store_logs()
