# Raspberry-Pi

HPCC Conference Raspberry Pi competition project

## Device
![Device](/img/imapi.jpg)

## Architecture
![Architecture](/img/architecture.png)

## AWS Resources

Create the S3 buckets and the DynamoDB instance using Terraform. 
The file main.tf defines the cloud infrastructure needed.

```
> terraform plan
> terraform apply
```

## Running

This application uses Python 3. You should not be using Python 2 anymore, EOL 2020.

There are many ways to setup AWS credentials, most typical is environment variables and .aws/config files. Credentials are expected to already be sourced.

Required pip modules
- boto3
- Pillow
- IMDbPy
- gpiozero
- picamera
- pygame
- google_images_download

```
> python main.py
```

## AWS Services
- Rekognition
- Polly
- DynamoDB
- Route 53
- S3

## Flow
1. power on the unit with AC or battery pack
1. boots into command prompt
1. Linux init.d system runs python script "main.py"
1. speaker will emit a ready signal when the system is initialized  
1. object is triggered by a mechanical action - button push
1. speaker emits a countdown 
1. capture picture from camera
1. save picture to /tmp/image.jpg
1. upload picture to S3
1. delete /tmp/image.jpg
1. call apis and store label counts
    1. detect_faces
    1. recognize_celebrities
    1. detect_labels
    1. detect_text
1. JavaScript generated on stats
1. website updated with graph and photo booth
1. speaker emits voice of what is analyzed
1. return script to ready state
