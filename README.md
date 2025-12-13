# Amazon Polly Text-to-Speech CI/CD Pipeline

A GitHub Actions-based CI/CD pipeline that automatically converts text to speech using Amazon Polly and uploads the audio files to Amazon S3.

## Project Overview

This project demonstrates a complete DevOps workflow that:
- Reads text from a file (`speech.txt`)
- Uses Amazon Polly to synthesize speech into MP3 format
- Automatically uploads audio files to S3 based on the workflow trigger
- Implements separate environments (beta/prod) using GitHub Actions

## Architecture

- **Pull Request Workflow**: Triggers on PRs to `main` branch → generates `beta.mp3`
- **Merge Workflow**: Triggers on push to `main` branch → generates `prod.mp3`
- **AWS Services**: Amazon Polly (text-to-speech), Amazon S3 (storage)
- **Automation**: GitHub Actions workflows

## Prerequisites

- AWS Account with access to Polly and S3
- GitHub account
- IAM user with appropriate permissions

## AWS Setup

### 1. Create S3 Bucket
```bash
# Via AWS Console:
# Navigate to S3 → Create bucket → Name it (e.g., 'your-bucket-name')
# Keep default settings
```

### 2. Create IAM User and Policies

Create an IAM user with the following permissions:

**Polly Permission:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "polly:SynthesizeSpeech",
            "Resource": "*"
        }
    ]
}
```

**S3 Permission:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/polly-audio/*"
        }
    ]
}
```

### 3. Generate Access Keys

- Go to IAM → Users → Your User → Security Credentials
- Create Access Key → Choose "CLI" use case
- **Save the Access Key ID and Secret Access Key** (you'll need these for GitHub Secrets)

## GitHub Setup

### 1. Clone or Fork This Repository
```bash
git clone https://github.com/gbarrett78/Warriors2015Championship.git
cd Warriors2015Championship
```

### 2. Configure GitHub Secrets

Navigate to: **Repository Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

- `AWS_ACCESS_KEY_ID`: Your IAM user access key ID
- `AWS_SECRET_ACCESS_KEY`: Your IAM user secret access key
- `S3_BUCKET_BETA`: Your S3 bucket name (for beta environment)
- `S3_BUCKET_PROD`: Your S3 bucket name (for prod environment)
- `AWS_DEFAULT_REGION`: Your AWS region (e.g., `us-east-1`)

## Project Structure
```
.
├── .github/
│   └── workflows/
│       ├── on_pull_request.yml    # Beta environment workflow
│       └── on_merge.yml            # Production environment workflow
├── synthesize.py                   # Main Python script
├── speech.txt                      # Text content to convert
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## How It Works

### Modifying the Text Content

1. Edit `speech.txt` with your desired text:
```bash
   echo "Your text here" > speech.txt
```

2. The text will be converted to speech using Amazon Polly's "Joanna" voice

### Triggering the Workflows

**Beta Environment (Pull Request):**
```bash
# Create a new branch
git checkout -b feature-branch

# Make changes to speech.txt
echo "Testing beta workflow" > speech.txt

# Commit and push
git add speech.txt
git commit -m "Update speech content"
git push origin feature-branch

# Create Pull Request on GitHub
# → Workflow triggers automatically
# → Creates polly-audio/beta.mp3 in S3
```

**Production Environment (Merge to Main):**
```bash
# Merge the pull request on GitHub
# → Workflow triggers automatically
# → Creates polly-audio/prod.mp3 in S3
```

### Verifying Uploaded Files

1. **Via AWS Console:**
   - Navigate to S3 → Your Bucket → `polly-audio/` folder
   - You should see:
     - `beta.mp3` (from pull requests)
     - `prod.mp3` (from merges to main)

2. **Via AWS CLI:**
```bash
   aws s3 ls s3://YOUR-BUCKET-NAME/polly-audio/
```

3. **Via GitHub Actions:**
   - Go to Actions tab in your repository
   - Click on the workflow run
   - Check the "Run Python script" step logs
   - Look for: `Successfully uploaded to s3://...`

## Local Testing

### Prerequisites
```bash
pip install boto3
```

### Configure AWS Credentials
```bash
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter your region (e.g., us-east-1)
# Enter output format (json)
```

### Run Locally
```bash
export S3_BUCKET_NAME='your-bucket-name'
export OUTPUT_FILENAME='test.mp3'
python3 synthesize.py
```

## Workflows Explained

### on_pull_request.yml

- **Trigger**: Pull requests targeting `main` branch
- **Environment Variables**:
  - Uses `S3_BUCKET_BETA` secret
  - Sets `OUTPUT_FILENAME=beta.mp3`
- **Output**: `s3://bucket/polly-audio/beta.mp3`

### on_merge.yml

- **Trigger**: Push events to `main` branch (after PR merge)
- **Environment Variables**:
  - Uses `S3_BUCKET_PROD` secret
  - Sets `OUTPUT_FILENAME=prod.mp3`
- **Output**: `s3://bucket/polly-audio/prod.mp3`

## Troubleshooting

### Workflow Fails with "Access Denied"
- Verify IAM permissions are correctly set
- Check that GitHub Secrets are properly configured
- Ensure S3 bucket name matches the secret value

### Audio File Not Generated
- Check GitHub Actions logs for error messages
- Verify `speech.txt` is not empty
- Confirm boto3 is installed in the workflow

### Wrong File Name in S3
- Verify `OUTPUT_FILENAME` environment variable is set in workflow
- Check workflow logs to see what filename was used

## Technologies Used

- **Amazon Polly**: Text-to-speech synthesis
- **Amazon S3**: Object storage
- **GitHub Actions**: CI/CD automation
- **Python 3.x**: Scripting language
- **boto3**: AWS SDK for Python

## Security Best Practices

- ✅ AWS credentials stored as GitHub Secrets (never in code)
- ✅ Least privilege IAM permissions
- ✅ S3 bucket access restricted to specific prefix
- ✅ No hardcoded values in source code

## Future Enhancements

- [ ] Add support for multiple voices
- [ ] Implement audio quality variations
- [ ] Add automated testing for audio files
- [ ] Create cleanup workflow for old audio files
- [ ] Add notification system for workflow completion

## License

This project is part of the Level Up in Tech DevOps program.

## Author

**Granville Barrett**  
DevOps Engineer | Systems Administrator  
[LinkedIn](https://linkedin.com/in/granvillebarrett) | [GitHub](https://github.com/gbarrett78)