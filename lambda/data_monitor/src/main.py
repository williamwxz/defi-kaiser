import os
import time
import boto3
import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE', 'RWA_Market_Data'))

def lambda_handler(event, context):
    try:
        # 从 DefiLlama 获取数据
        response = requests.get('https://api.defillama.com/rwa/ondo')
        data = response.json()

        # 存储到 DynamoDB
        item = {
            'timestamp': int(time.time()),
            'protocol': 'ondo',
            'discount': data['discount'],
            'tvl': data['tvl']
        }
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': 'Data stored successfully'
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }