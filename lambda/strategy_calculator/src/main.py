import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE', 'RWA_Market_Data'))
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        # 查询最新数据
        response = table.scan()
        items = response['Items']
        latest_item = max(items, key=lambda x: x['timestamp'])

        # 判断套利条件
        if latest_item['discount'] > 0.08:
            # 触发交易执行 Lambda
            lambda_client.invoke(
                FunctionName='TradeExecutor',
                InvocationType='Event',
                Payload=bytes('{"action": "buy", "asset": "OUSG", "amount": 10000}', 'utf-8')
            )

        return {
            'statusCode': 200,
            'body': 'Strategy check completed'
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }