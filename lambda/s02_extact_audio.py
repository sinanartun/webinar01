import json
import os
import subprocess
import boto3

def lambda_handler(event, context):
    # print(os.system('ls /opt/bin/bin'))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    remote_video_path = event['Records'][0]['s3']['object']['key']
    video_file_name = os.path.basename(remote_video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]

    local_video_path = f'/tmp/{video_file_name}'
    remote_audio_path = f'audio/{video_file_name_wo_ext}.flac'
    local_audio_path = f'/tmp/{video_file_name_wo_ext}.flac'
    
    # Download the MP4 file from S3
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, remote_video_path, local_video_path)
    if os.path.exists(local_audio_path):
        os.remove(local_audio_path)

    # Run ffmpeg to extract audio and convert to FLAC
    command = f'ffmpeg -i {local_video_path} -vn -acodec flac {local_audio_path}'
    subprocess.run(command, shell=True, check=True)

    # Upload the FLAC file to S3
    s3.upload_file(local_audio_path, bucket_name, remote_audio_path)

    return {
        'statusCode': 200,
        'body': f"Audio extracted and converted to FLAC. Uploaded to S3 bucket: {bucket_name}/{remote_audio_path}"
    }