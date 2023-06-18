# Serverless YouTube Downloader API

The Serverless YouTube Downloader API project aims to create an AWS Lambda function that takes a YouTube video ID as input and returns the URL to download the video in either HD or SD format.

## Deployment Steps

To deploy the Serverless YouTube Downloader API, follow these steps:

1. Set up CDK:
   - Install the AWS CDK CLI if you haven't already: `npm install -g aws-cdk`
   - Create a new directory for your CDK project: `mkdir my-cdk-project && cd my-cdk-project`
   - Initialize a new CDK project: `cdk init app --language python`

2. Install dependencies:
   - Install the required Python dependencies: `pip install aws-cdk.aws-lambda aws-cdk.aws-dynamodb`

3. Write the CDK code:
   - Open the `app.py` file in your text editor and replace its contents with the provided code.

   Make sure to replace `REGION`, `ACCOUNT_ID`, and `VERSION` with the appropriate values for your AWS environment.

4. Build and deploy the CDK stack:
   - Build the CDK project: `cdk synth`
   - Deploy the CDK stack: `cdk deploy`

   The CDK will create the necessary resources, including the Lambda function and DynamoDB table, with the specified permissions.

## Running the Lambda

To use the Lambda function, append `?code=VIDEOID` to the end of the Lambda URL. The Lambda will process your request and respond with HD and SD URLs to play/download the video.

## TODOs

- [x] Add Caching using DynamoDB
- [ ] Add authorization/authentication
- [ ] Add support for multiple video formats
- [ ] Add an interactive UI to leverage the API and create a full-fledged YouTube downloader

Please note that the above TODOs outline future enhancements for the project.