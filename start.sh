#!/bin/bash

# Function to display the countdown
function countdown {
    secs=$((60-$1))
    while [ $secs -gt 0 ]; do
        printf "\rRemaining: %02d seconds" $secs
        sleep 1
        : $((secs--))
    done
    printf "\nDone!\n"
}

# Start the countdown
countdown 0

# Get the cluster ID
cluster_id=$(curl -s http://localhost:8082/v3/clusters | grep -o '"cluster_id":"[^"]*' | awk -F ':"' '{print $2}')

# Get the local cluster information
# curl "http://localhost:8082/v3/clusters/$cluster_id"

# Get a list of topics
# curl "http://localhost:8082/v3/clusters/$cluster_id/topics"

# Create a topic
curl -X POST -H "Content-Type:application/json" -d '{"topic_name":"log-ingestor"}' "http://localhost:8082/v3/clusters/$cluster_id/topics"

# Post test data to topic
curl -X POST \
  -H "Content-Type: application/vnd.kafka.json.v2+json" \
  -H "Accept: application/vnd.kafka.v2+json" \
  --data '{
    "records": [
      {
        "value": {
          "level": "error",
          "message": "Failed to connect to DB",
          "resourceId": "server-1234",
          "timestamp": "2023-09-15T08:00:00Z",
          "traceId": "abc-xyz-123",
          "spanId": "span-456",
          "commit": "5e5342f",
          "metadata": {
            "parentResourceId": "server-0987"
          }
        }
      }
    ]
  }' \
  "http://localhost:8082/topics/log-ingestor"


# Print msg
# echo "Sample Data published successfully to 'log-ingestor' topic."


# Create consumer instance
curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" -H "Accept: application/vnd.kafka.v2+json" \
  -d '{"name": "log_consumer_instance", "format": "json", "auto.offset.reset": "earliest"}' \
  "http://localhost:8082/consumers/log_consumer"

# Subscribe the consumer to a topic
curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" \
  -d '{"topics":["log-ingestor"]}' \
  "http://localhost:8082/consumers/log_consumer/instances/log_consumer_instance/subscription"

# Consume data
#curl -X GET -H "Accept: application/vnd.kafka.json.v2+json" \
#  "http://localhost:8082/consumers/log_consumer/instances/log_consumer_instance/records"
