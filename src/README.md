src/
├── backend/
│   ├── __init__.py             # Initialization file for the backend
│   ├── app.py                  # Main Flask application setup
│   ├── database.py             # Database configurations and models
│   ├── log_ingestor.py         # Kafka ingestion functions
│   ├── query_interface.py      # Functions for querying logs
│   └── routes.py               # Route definitions for the Flask app
├── frontend/
│   ├── __init__.py             # Initialization file for the frontend
│   ├── assets/                 # Folder for static assets
│   │   ├── css/
│   │   │   ├── main.css        # Main CSS styles
│   │   │   └── normalize.css   # Normalize CSS
│   │   └── js/
│   │       ├── main.js         # Main JavaScript file
│   │       └── script.js       # Additional scripts
│   ├── index.html              # Main HTML file
│   └── templates/              # Folder for HTML templates
│       ├── error.html          # Template for error pages
│       ├── ingestor.html       # Template for ingestion interface
│       ├── main.html           # Main layout template
│       ├── query.html          # Template for querying logs
│       └── results.html        # Template for displaying search results
├── README.md                  # Documentation about the project
├── requirements.txt            # List of project dependencies
|── run.sh                      # Script to run the application
└── Dockerfile                  # Dockerfile

#### run application with
`flask --app=backend.app run -p 3000`