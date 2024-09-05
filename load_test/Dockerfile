FROM python:3.9-slim

# Install MySQL connector
RUN pip install mysql-connector-python

# Copy load test script
COPY load_test.py /load_test.py

# Set the default command
CMD ["python", "/load_test.py"]

