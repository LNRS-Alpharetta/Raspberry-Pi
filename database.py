import boto3

db = boto3.client('dynamodb')


def inc_label(label):
    db.update_item(
        TableName='raspberry-pi-camera',
        Key={'label': {'S': label}},
        UpdateExpression='ADD #count :count',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':count': {'N': '1', }, })


def inc(labels):
    if labels:
        for label in labels:
            inc_label(label)
