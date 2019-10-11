import boto3
import vars
import datetime

db_client = boto3.client('dynamodb')
db_resource = boto3.resource('dynamodb')
table = db_resource.Table(vars.get('trend_table'))


def inc_label(label):
    db_client.update_item(
        TableName=vars.get('stats_table'),
        Key={vars.get('stats_key'): {'S': label}},
        UpdateExpression='ADD #count :count',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':count': {'N': '1', }, })


def inc(labels):
    if labels:
        for label in labels:
            inc_label(label)


def insert_trend(confidence):
    table.put_item(
        Item={vars.get('trend_key'): str(datetime.datetime.now()),
              'confidence': confidence})
