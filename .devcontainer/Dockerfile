FROM python:3.13-slim

# Copy requirements file (from host to container)
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Set working directory AFTER installing packages
WORKDIR /workspace
