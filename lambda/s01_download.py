import json
import os
import boto3
from pytube import YouTube
from slugify import slugify

def lambda_handler(event, context):
    try:
        url = event['queryStringParameters']['url']
        output_path = '/tmp/'  # Lambda allows writing to /tmp directory

        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        # Generate a URL-friendly filename
        filename = slugify(yt.title, separator='_') + '.mp4'
        remote_path = "video/" + filename
        filepath = os.path.join(output_path, filename)

        # Download the video
        stream.download(output_path, filename=filename)

        # Upload the video to S3
        s3 = boto3.client('s3')
        bucket_name = 'webinar001'
        s3.upload_file(filepath, bucket_name, remote_path)

        return {"statusCode": 200, "body": "Video downloaded and uploaded to S3 successfully!"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}