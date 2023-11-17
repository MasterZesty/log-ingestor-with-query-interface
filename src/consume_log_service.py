from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import json
from datetime import datetime
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)  # Set your desired logging level

# MySQL database configuration
# DEFINE THE DATABASE CREDENTIALS
user = 'krishna'
password = 'krishna'
host = 'mysql-write'
port = 3306
database = 'log_ingestor_db'
 
DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    level = Column(String(50))
    message = Column(String(255))
    resourceId = Column(String(50))
    timestamp = Column(DateTime)
    traceId = Column(String(50))
    spanId = Column(String(50))
    commit = Column(String(50))
    parentResourceId = Column(String(50))

# Create an inspector
inspector = inspect(engine)

# Check if the table already exists
if not inspector.has_table('logs'):
    # If the table doesn't exist, create it
    Base.metadata.create_all(engine)
    print("Table 'logs' created successfully.")
else:
    print("Table 'logs' already exists.")

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'kafka1:19092',  # Replace with your Kafka broker(s)
    'group.id': 'log_consumer_group',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Read from the beginning of the topic on first start
}

def consume_and_store_logs():
    consumer = Consumer(conf)
    consumer.subscribe(['log-ingestor'])  # Replace 'log_topic' with your actual topic

    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll every 1 second for new messages

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                else:
                    raise KafkaException(msg.error())
            else:
                # Process the message and store in MySQL
                log_data = json.loads(msg.value().decode('utf-8'))

                Session = sessionmaker(bind=engine)
                session = Session()

                # check 1: Convert ISO 8601 timestamp to MySQL DateTime format
                parsed_timestamp = datetime.strptime(log_data.get('timestamp'), '%Y-%m-%dT%H:%M:%SZ')
                mysql_timestamp = parsed_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                new_log = Log(
                    level=log_data.get('level'),
                    message=log_data.get('message'),
                    resourceId=log_data.get('resourceId'),
                    timestamp=mysql_timestamp,
                    traceId=log_data.get('traceId'),
                    spanId=log_data.get('spanId'),
                    commit=log_data.get('commit'),
                    parentResourceId=log_data.get('metadata', {}).get('parentResourceId')
                )

                session.add(new_log)
                session.commit()
                session.close()

                logging.info(f'Logs stored in db: {log_data}')

    except KeyboardInterrupt:
        logging.info(f'Aborted by user')
        sys.stderr.write('%% Aborted by user\n')

    finally:
        consumer.close()

if __name__ == '__main__':
    consume_and_store_logs()
