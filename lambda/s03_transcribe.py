import boto3
import os
import random
import string

def generate_random_string(length):
    alphanumeric_characters = string.ascii_letters + string.digits
    return 'r'.join(random.choice(alphanumeric_characters) for _ in range(length))


def start_transcription_job(bucket_name, remote_audio_path):

    transcribe = boto3.client('transcribe')
    
    audio_file_name = os.path.basename(remote_audio_path)
    audio_file_name_wo_ext = os.path.splitext(audio_file_name)[0]
    job_name = generate_random_string(10)
    
    try:
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            IdentifyLanguage=True,  # Modify this according to your audio language
            MediaFormat=audio_file_name.split('.')[-1],  # Extract media format from file extension
            Media={
                'MediaFileUri': f's3://{bucket_name}/{remote_audio_path}'
            },
            OutputBucketName=bucket_name,
            OutputKey=f'srt/{audio_file_name_wo_ext}',
            Subtitles={
                'Formats': ['srt']
            }
        )
        
        return response['TranscriptionJob']['TranscriptionJobName']
    
    except Exception as e:
        print(f"Error starting transcription job: {e}")
        raise e

    
    except Exception as e:
        print(f"Error starting transcription job: {e}")
        raise e

def lambda_handler(event, context):
    # Extract parameters from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    remote_audio_path = event['Records'][0]['s3']['object']['key']
    
    # Start the transcription job
    transcription_job_name = start_transcription_job(bucket_name, remote_audio_path)
    
    return {
        'statusCode': 200,
        'body': f"Transcription job '{transcription_job_name}' started successfully."
    }
