from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import threading
import subprocess
import time
import logging

from consume_log_service import consume_and_store_logs

# Configure the logger
logging.basicConfig(level=logging.INFO)  # Set your desired logging level

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def publish_to_kafka():

    if request.method == 'GET':
        return jsonify({"error": "Invalid request GET method for this endpoint : This endpoint is used for ingesting data please use POST"}), 400

    log_data = request.json  # Assuming the incoming data is in JSON format
    logging.info(f'Incoming log data: {log_data}')

    # Example data for publishing to Kafka
    kafka_data = {
        "records": [
            {
                "value": {
                    "level": log_data.get("level", "info"),
                    "message": log_data.get("message", ""),
                    "resourceId": log_data.get("resourceId", ""),
                    "timestamp": log_data.get("timestamp", ""),
                    "traceId": log_data.get("traceId", ""),
                    "spanId": log_data.get("spanId", ""),
                    "commit": log_data.get("commit", ""),
                    "metadata": {
                        "parentResourceId": log_data.get("parentResourceId", "")
                    }
                }
            }
        ]
    }

    # Publishing data to Kafka
    kafka_url = "http://kafka-rest-proxy:8082/topics/log-ingestor"
    headers = {
        "Content-Type": "application/vnd.kafka.json.v2+json",
        "Accept": "application/vnd.kafka.v2+json"
    }

    try:
        response = requests.post(kafka_url, json=kafka_data, headers=headers)
        if response.status_code == 200:
            logging.info(f"Data published to Kafka successfully. Status code: {response.status_code}")
            return jsonify({"message": "Data published to Kafka successfully."}), 200
        else:
            logging.error(f"Failed to publish data to Kafka. Status code: {response.status_code}")
            return jsonify({"error": "Failed to publish data to Kafka."}), 500
    except requests.RequestException as e:
        logging.exception(f"RequestException occurred: {str(e)}")
        return jsonify({"error": f"RequestException: {str(e)}"}), 500

# Your Log model
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

# Establishing connection to the database
user = 'krishna'
password = 'krishna'
host = 'mysql-write'
port = 3306
database = 'log_ingestor_db'

DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Flask route to handle search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # print(f'for data {request.form}')
        search_field = request.form['searchField']
        search_query = request.form['searchQuery']

        # Create a session
        session = Session()

        # Query logs based on the search criteria
        if search_field in ['level', 'message', 'resourceId', 'traceId', 'spanId', 'commit']:
            # Filter logs based on the search criteria
            logs = session.query(Log).filter(getattr(Log, search_field) == search_query).all()
        elif search_field == 'timestamp':
            # Handle timestamp search
            search_query_dt = datetime.strptime(search_query, '%Y-%m-%d %H:%M:%S')
            logs = session.query(Log).filter(Log.timestamp == search_query_dt).all()

        session.close()  # Close the session

        row_classes = ['odd:bg-white odd:dark:bg-gray-900', 'even:bg-gray-50 even:dark:bg-gray-800']

        return render_template('index.html', logs=logs, row_classes=row_classes)

    return render_template('index.html')



if __name__ == '__main__':
    # Start the consumer in a separate thread
    consumer_thread = threading.Thread(target=consume_and_store_logs)
    consumer_thread.start()

    app.run(debug=True, port=3000)
