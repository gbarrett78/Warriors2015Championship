import boto3
import os
from contextlib import closing

# Configure the Polly client
# boto3 automatically uses credentials configured via 'aws configure'
# or environment variables
polly_client = boto3.client('polly', region_name='us-east-1') # Use your desired region

# File names
text_file_name = "speech.txt"
audio_file_name = os.environ.get('OUTPUT_FILENAME', 'speech.mp3')  # Use env var or default to speech.mp3

def synthesize_text_file(text_file, audio_file):
    """Reads text from a file and synthesizes it into an MP3 audio file."""
    try:
        # Read the text from the input file
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text:
            print(f"Error: {text_file} is empty.")
            return
        
        # Request speech synthesis from Amazon Polly
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna" # Choose a voice, e.g., Joanna, Matthew, Sally, etc.
        )
        
        # Save the audio stream to a file
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                with open(audio_file, "wb") as file:
                    file.write(stream.read())
            print(f"Successfully saved speech to {audio_file}")
            
            # Upload to S3
            bucket_name = os.environ.get('S3_BUCKET_NAME')
            if bucket_name:
                s3_client = boto3.client('s3')
                s3_key = f'polly-audio/{audio_file}'
                
                try:
                    s3_client.upload_file(audio_file, bucket_name, s3_key)
                    print(f"Successfully uploaded to s3://{bucket_name}/{s3_key}")
                except Exception as upload_error:
                    print(f"Error uploading to S3: {upload_error}")
            else:
                print("Warning: S3_BUCKET_NAME not set, skipping S3 upload")
                
        else:
            print("Error: AudioStream not found in the response.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    synthesize_text_file(text_file_name, audio_file_name)
