from flask import Flask, render_template, request
import boto3
from PIL import Image
import io

app = Flask(__name__)

# AWS configuration
S3_BUCKET_NAME = 'vishathira'
DYNAMODB_TABLE_NAME = 'DemoTable'
AWS_REGION = 'us-east-1'

# Initialize AWS clients
s3 = boto3.client('s3', region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    photo = request.files['photo']

    # Save the photo to S3
    photo_thumbnail = create_thumbnail(photo)
    save_photo_to_s3(photo_thumbnail)

    # Save the data to DynamoDB
    save_data_to_dynamodb(name, age)

    return 'Data submitted successfully!'

# Function to create a thumbnail from the photo
def create_thumbnail(photo):
    image = Image.open(photo)
    image.thumbnail((200, 200))
    thumbnail_bytes = io.BytesIO()
    image.save(thumbnail_bytes, format='JPEG')
    thumbnail_bytes.seek(0)
    return thumbnail_bytes

# Function to save the photo to S3
def save_photo_to_s3(photo):
    s3.upload_fileobj(photo, S3_BUCKET_NAME, photo.filename)

# Function to save the data to DynamoDB
def save_data_to_dynamodb(name, age):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(Item={'Name': name, 'Age': age})

# Main driver function
if __name__ == '__main__':
    app.run(debug=True)
