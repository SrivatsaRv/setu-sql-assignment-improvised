import docker
import csv
import subprocess
import time
import mysql.connector

# Initialize Docker client
client = docker.from_env()

# File to store metrics
CSV_FILE = '/home/ec2-user/project-docker/docker_metrics.csv'

#Connecting to the db instance sql1 and sql2
sql1_db_config = {
    'user': 'root',
    'password': 'root_password',
    'host': 'sql1',
    'database': 'testdb'
}

sql2_db_config = {
    'user': 'root',
    'password': 'root_password',
    'host': 'sql2',
    'database': 'testdb'
}

def get_container_stats(container_name):
    """Get CPU and memory stats for a container using 'docker stats'."""
    result = subprocess.run(
        ['docker', 'stats', '--no-stream', '--format', 
         '{{.CPUPerc}},{{.MemPerc}}', container_name],
        capture_output=True, text=True
    )
    return result.stdout.strip().split(',')

def get_active_sessions(db_config):
    """Get the number of active sessions (connections) in a MySQL container."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SHOW STATUS WHERE `variable_name` = 'Threads_connected';")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return int(result[1])  # Return the number of active sessions
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 0

def collect_metrics():
    """Collect CPU, memory, and session stats from the containers."""
    # Get CPU and memory stats
    sql1_cpu_mem_stats = get_container_stats('sql1')
    sql2_cpu_mem_stats = get_container_stats('sql2')

    # Get active sessions from MySQL
    sql1_active_sessions = get_active_sessions(sql1_db_config)
    sql2_active_sessions = get_active_sessions(sql2_db_config)

    # Log to CSV
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            time.strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
            sql1_cpu_mem_stats[0],  # CPU % for sql1
            sql1_cpu_mem_stats[1],  # Memory % for sql1
            sql2_cpu_mem_stats[0],  # CPU % for sql2
            sql2_cpu_mem_stats[1],  # Memory % for sql2
            sql1_active_sessions,   # Sessions for sql1
            sql2_active_sessions    # Sessions for sql2
        ])

if __name__ == "__main__":
    # Write header to CSV file
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Timestamp', 
            'SQL1 CPU (%)', 'SQL1 Memory (%)', 
            'SQL2 CPU (%)', 'SQL2 Memory (%)',
            'SQL1 Active Sessions', 'SQL2 Active Sessions'
        ])

    while True:
        collect_metrics()
        time.sleep(5)  # Collect every 5 seconds

