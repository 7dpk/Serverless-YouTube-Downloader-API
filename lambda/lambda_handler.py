import json
import yt_dlp
import boto3
import time
import requests
TABLE_NAME = "video_cache"
TTL_SECONDS = 14400  # 2 hrs

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Get the URL of the YouTube video from the input event
    url = event['queryStringParameters'].get('code', 'pW0eZRoQ86g')
    print(url)
    url = 'https://youtu.be/' + url
    print(url)
    try:
        # Check if the URL is already in the cache
        response = dynamodb.get_item(
            TableName=TABLE_NAME,
            Key={
                'url': {'S': str(url)}
            }
        )

        # If the URL is in the cache and has not expired, return the cached file URL
        if 'Item' in response:
            item = response['Item']
            timestamp = item['timestamp']['N']
            file_url_hd = item['file_url_hd']['S']
            file_url_sd = item['file_url_sd']['S']
            if time.time() - int(timestamp) < TTL_SECONDS:
                res = json.dumps({"hd": file_url_hd, "sd": file_url_sd})
                return {"statusCode": 200, "headers": { "Content-type": "text/html","X-Frame-Options": "ALLOWALL" }, "body": res}
            else:
                # Delete the expired item from the cache
                dynamodb.delete_item(
                    TableName=TABLE_NAME,
                    Key={
                        'url': {'S': url}
                    }
                )

        # If the URL is not in the cache or has expired, fetch the file URL and store it in the cache
        ydl = yt_dlp.YoutubeDL()
        info = ydl.extract_info(url, download=False)
        format_720p = next((f for f in info['formats'] if f['format_id'] == '22'), None)
        format_360p = next((f for f in info['formats'] if f['format_id'] == '18'), None)
        file_url_hd = format_720p['url'] if format_720p else None
        file_url_sd = format_360p['url'] if format_360p else None
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'url': {'S': url},
                'timestamp': {'N': str(int(time.time()))},
                'file_url_hd': {'S': file_url_hd},
                'file_url_sd': {'S': file_url_sd}
            }
        )
        res = json.dumps({"hd": file_url_hd, "sd": file_url_sd})
        return {
            'statusCode': 200,
            'body': res,
            "headers": { "Content-type": "text/html","X-Frame-Options": "ALLOWALL" }
        }

    except Exception as e:
        # Return an error message if an exception occurs
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'An error occurred while fetching the file URL: {str(e)}'})
        }
