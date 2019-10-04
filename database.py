import boto3
import vars

db = boto3.client('dynamodb')

# add timestamp and confidence score to database


def inc_label(label):
    db.update_item(
        TableName=vars.get('stats_table'),
        Key={vars.get('stats_key'): {'S': label}},
        UpdateExpression='ADD #count :count',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':count': {'N': '1', }, })


def inc(labels):
    if labels:
        for label in labels:
            inc_label(label)
