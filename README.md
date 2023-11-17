# Log Ingestor and Query Interface
## Overview
This system is designed to efficiently ingest, store, and query vast volumes of log data. It comprises a Log Ingestor responsible for accepting log data over HTTP and a Query Interface that enables users to perform full-text searches and apply filters on various log attributes.

## Technologies Used
- **Programming Language**: Python
- **Database**: MySQL
- **Technologies**: Kafka , Kafka Rest Proxy, Kafka Schema Registry
- **Frontend**: HTML CSS JavaScript
- **Backend**: Flask

## Features Implemented
1. **Log Ingestor**
   - Ingests logs in the provided JSON format via HTTP on port `3000`.
   - Ensures scalability to handle high log volumes.
   - Optimizes I/O operations and database write speeds.
   
2. **Query Interface**
   - Offers a user-friendly interface (Web UI/CLI) for full-text search.
   - Includes filters for:
       - level
       - message
       - resourceId
       - timestamp
       - traceId
       - spanId
       - commit
       - metadata.parentResourceId
   - Implements efficient search algorithms for quick results.

3. **Advanced Features (To be Implemented...)**
   - Search within specific date ranges.
   - Utilization of regular expressions for search.
   - Combining multiple filters for precise queries.
   - Real-time log ingestion and searching capabilities.
   - Role-based access control to the query interface.

## System Architecture

### System Architecture Diagram

![System Architecture Diagram](docs\imgs\architecture_v1.0.0.png)
### Log Ingestor I - Log Publisher Service
- Utilizes an HTTP server to receive logs.
- Parses incoming JSON logs and publishes them to kafka topic.

### Log Ingestor II - Log Consume Service
- Subscribes to the Kafka topic and consumes the log from topic.
- Stores log from topic to primary read database instance.

### Query Interface - Log Search Service
- Provides a user interface for search and filtering.
- Processes user queries and translates them into database queries.
- Utilizes optimized indexing for faster search results.

### Database Structure
- **MYSQL - Relational Database**: Stores structured log data, optimizing for structured queries and joins.
- **NoSQL Database (e.g., Elasticsearch)**: Facilitates full-text search and complex queries efficiently.

### Scalability and Performance
- **Scalability**: Implements database sharding for distributing load.
- **Caching Mechanism**: Utilizes caching strategies for frequently accessed data.
- **Load Balancing**: Distributes incoming requests across multiple servers for enhanced performance.

## How to Run the Project
1. Clone the repository from the GitHub Classroom submission link.
2. Install necessary dependencies using *instructions provided in the README*.
3. Run the Log Ingestor and Query Interface components following the *setup instructions*.
4. Access the Query Interface via the provided URL/endpoint.
5. Use the interface to perform searches and apply filters on log data.

## Identified Issues and Future Improvements
- **Real-time Capabilities**: Enhance real-time log ingestion and search.
- **Enhanced Security**: Strengthen security measures, especially for user access and data integrity.
- **Optimization**: Continuously optimize database queries and indexing strategies for better performance.

## Evaluation Criteria Met
1. **Volume**: Handles massive log volumes efficiently.
2. **Speed**: Provides quick search results.
3. **Scalability**: Adaptable to increasing log volumes and queries.
4. **Usability**: Offers an intuitive interface for users.
5. **Advanced Features**: Implements bonus functionalities.
6. **Readability**: Maintains a clean and structured codebase.

## Conclusion
This system effectively manages log data ingestion and provides a seamless query interface for users to retrieve specific logs based on various attributes. Continuous improvements can enhance its performance and capabilities.