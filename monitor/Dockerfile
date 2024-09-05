FROM python:3.9-slim

# Install Docker SDK for Python and Docker CLI
RUN apt-get update && apt-get install -y docker.io && pip install docker mysql-connector-python

# Copy the monitor script
COPY monitor.py /monitor.py

# Set the default command to run the script
CMD ["python", "/monitor.py"]

