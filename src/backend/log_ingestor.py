"""
LogIngestor Class for Kafka Log Ingestion.

This class handles the ingestion of log data into Kafka using the provided Kafka REST Proxy URL.

Dependencies:
    - requests
    - logging

Author: Krishna Nimbalkar
Date: 17/11/2023

"""

import requests
import logging

class LogIngestor:
    """
    A class to handle log ingestion to Kafka.

    Attributes:
        kafka_url (str): The URL to the Kafka REST Proxy.
        headers (dict): Headers required for Kafka REST requests.
    """

    def __init__(self, kafka_url: str) -> None:
        """
        Initializes the LogIngestor class.

        Args:
            kafka_url (str): The URL to the Kafka REST Proxy.
        """
        self.kafka_url = kafka_url
        self.headers = {
            "Content-Type": "application/vnd.kafka.json.v2+json",
            "Accept": "application/vnd.kafka.v2+json"
        }

    def publish_to_kafka(self, log_data: dict) -> bool:
        """
        Publishes log data to Kafka.

        Args:
            log_data (dict): A dictionary containing log data.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            response = requests.post(self.kafka_url, json=log_data, headers=self.headers)
            if response.status_code == 200:
                logging.info(f"Data published to Kafka successfully. Status code: {response.status_code}")
                return True
            else:
                logging.error(f"Failed to publish data to Kafka. Status code: {response.status_code}")
                return False
        except requests.RequestException as e:
            logging.exception(f"RequestException occurred: {str(e)}")
            return False
