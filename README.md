
### Files and Directories

- **`docker-compose.yml`**: Defines the Docker services for MySQL containers, load testing, and monitoring.
- **`docker_metrics.csv`**: CSV file where monitoring metrics are recorded.
- **`init.sql`**: SQL script for initializing the MySQL databases and creating the `users` table.
- **`load_test/`**: Contains the Dockerfile and Python script for generating load on `sql1`.
- **`monitor/`**: Contains the Dockerfile and Python script for monitoring container metrics and MySQL sessions.

## Services

### MySQL Containers (`sql1` and `sql2`)

- **`sql1`**: MySQL container exposed on port `3306`.
- **`sql2`**: MySQL container exposed on port `3307`.

### Load Testing (`load_test`)

- **Image**: Python 3.9 with MySQL connector.
- **Script**: `load_test.py` inserts random data into the `users` table in the `sql1` database every second.

### Monitoring (`monitor`)

- **Image**: Python 3.9 with Docker SDK and MySQL connector.
- **Script**: `monitor.py` collects and logs metrics such as CPU usage, memory usage, and active MySQL sessions to `docker_metrics.csv` every 5 seconds.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup and Running

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd project-docker
# setu-sql-assignment-improvised
