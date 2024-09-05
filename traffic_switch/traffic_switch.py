import time
import csv
import os

# File paths
metrics_file = '/home/ec2-user/project-docker/docker_metrics.csv'
failover_file = '/home/ec2-user/project-docker/failover_history.txt'
nginx_template_file = '/home/ec2-user/project-docker/nginx/nginx.conf.template'
nginx_config_file = '/etc/nginx/nginx.conf'

# Function to log the failover event
def log_failover(failover_to):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(failover_file, 'a') as log_file:
        log_file.write(f"{timestamp} - Failed over to {failover_to}\n")
    print(f"Logged failover to {failover_to}")

# Function to update the NGINX configuration using a template
def update_nginx_config(active_server):
    backup_server = 'sql1' if active_server == 'sql2' else 'sql2'
    
    # Read the NGINX config template
    with open(nginx_template_file, 'r') as template_file:
        nginx_config = template_file.read()
    
    # Replace placeholders with actual server names
    nginx_config = nginx_config.replace('{{active_server}}', active_server)
    nginx_config = nginx_config.replace('{{backup_server}}', backup_server)

    # Write the updated config to the actual NGINX config file
    with open(nginx_config_file, 'w') as config_file:
        config_file.write(nginx_config)
    
    print(f"NGINX config updated to failover to {active_server}")
    # Reload NGINX to apply the new config
    os.system('nginx -s reload')

# Function to monitor docker_metrics.csv and trigger failover
def monitor_metrics():
    active_db = 'sql1'  # Start with sql1 as the primary database
    while True:
        with open(metrics_file, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)
            if len(lines) > 1:
                latest_metrics = lines[-1]
                timestamp, sql1_cpu, sql1_mem, sql2_cpu, sql2_mem, sql1_sessions, sql2_sessions = latest_metrics
                sql1_sessions = int(sql1_sessions)
                sql2_sessions = int(sql2_sessions)
                sql1_cpu = float(sql1_cpu.strip('%'))
                sql2_cpu = float(sql2_cpu.strip('%'))

                # Check if we are monitoring sql1 and need to failover to sql2
                if active_db == 'sql1' and (sql1_cpu > 50.0 or sql1_sessions > 30):
                    log_failover('sql2')
                    update_nginx_config('sql2')  # Failover to sql2
                    active_db = 'sql2'  # Switch to monitoring sql2

                # Check if we are monitoring sql2 and need to failback to sql1
                elif active_db == 'sql2' and (sql2_cpu > 50.0 or sql2_sessions > 30):
                    log_failover('sql1')
                    update_nginx_config('sql1')  # Failback to sql1
                    active_db = 'sql1'  # Switch back to monitoring sql1

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    monitor_metrics()
