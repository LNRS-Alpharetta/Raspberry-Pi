import boto3

db = boto3.client('dynamodb')


def increment_label_count(label):
    db.update_item(
        TableName='raspberry-pi-camera',
        Key={'label': {'S': label}},
        UpdateExpression='ADD #count :count',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':count': {'N': '1', }, })


def increment_label_counts(labels):
    if labels:
        for label in labels:
            increment_label_count(label)
