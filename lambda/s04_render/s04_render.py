import json
import boto3
import os
import subprocess

def lambda_handler(event, context):
    # Extracting information from the event
    # record = event['Records'][0]
    # bucket_name = record['s3']['bucket']['name']
    # remote_srt_path = record['s3']['object']['key']
    bucket_name = 'webinar001'
    remote_srt_path = 'srt/white_house_trump_s_remarks_that_he_would_allow_russia_to_attack_nato_allies_was_unhinged.srt'
    file_name_wo_ext = os.path.splitext(os.path.basename(remote_srt_path))[0]
    
    # Define local paths
    local_video_path = f'/tmp/{file_name_wo_ext}.mp4'
    local_srt_path = f'/tmp/{file_name_wo_ext}.srt'
    local_out_video_path = f'/tmp/out_{file_name_wo_ext}.mp4'
    
    # Download files from S3
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, f'video/{file_name_wo_ext}.mp4', local_video_path)
    s3.download_file(bucket_name, remote_srt_path, local_srt_path)
    
    # Execute ffmpeg command with custom font file
    font_path = os.path.join(os.path.dirname(__file__), 'Arial.ttf')
    command = f"ffmpeg -i {local_video_path} -vf subtitles={local_srt_path}:force_style='FontName={font_path}' {local_out_video_path}"
    subprocess.run(command, shell=True, check=True)
    
    # Upload output video to S3
    remote_out_video_path = f'out/{file_name_wo_ext}.mp4'
    s3.upload_file(local_out_video_path, bucket_name, remote_out_video_path)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Video processing complete!')
    }
