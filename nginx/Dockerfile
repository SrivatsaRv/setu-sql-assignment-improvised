# Dockerfile for traffic_switch

FROM python:3.8-slim

# Create application directory
WORKDIR /app

# Copy the traffic_switch.py script
COPY traffic_switch/traffic_switch.py /app/traffic_switch.py

# Copy the nginx configuration files (correct path relative to Docker build context)
COPY nginx/nginx.conf.template /app/nginx.conf.template
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Install any necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "/app/traffic_switch.py"]

