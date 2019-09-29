import boto3

db = boto3.client('dynamodb')


def insert_label(label):
    db.update_item(
        TableName='raspberry-pi-camera',
        Key={'label': {'S': label}},
        UpdateExpression='ADD #count :count',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':count': {'N': '1', }, })


def insert_labels(labels):
    if labels:
        for label in labels:
            insert_label(label)
