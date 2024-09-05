# Dockerfile for traffic_switch

FROM python:3.8-slim

# Create application directory
WORKDIR /app

# Copy the traffic_switch.py script
COPY traffic_switch/traffic_switch.py /app/traffic_switch.py

# Copy the nginx configuration files
COPY nginx/nginx.conf.template /app/nginx.conf.template
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Command to run the application
CMD ["python", "/app/traffic_switch.py"]
