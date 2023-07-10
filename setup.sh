#!/bin/bash

# Update system packages
sudo apt-get update

# Install Python and necessary packages
sudo apt-get install -y python3 python3-pip

# Install Flask and other dependencies
pip3 install flask boto3 Pillow

# Set environment variables
export AWS_REGION='us-east-1'
export S3_BUCKET_NAME='vishathira'
export DYNAMODB_TABLE_NAME='DemoTable'

# Run the Flask application
python3 app.py
