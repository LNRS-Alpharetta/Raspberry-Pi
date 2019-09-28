# Raspberry-Pi

HPCC Conference Raspberry Pi competition project

## Hardware

### Stores
- MicroCenter
    - Duluth (has a better DIY/Maker section)
    - Marietta

### Parts
- needed
  - battery pack
  - mini speaker - 3.5 mm
  - button integration
    - IO ribbon - small
    - wire with square female ends, 2-6, connected is better
- nice to have
  - LED/visual dial for confidence threshold
- purchased
  - Raspberry PI - [$45.00] 
  - case - $6.99
  - power adapter - $7.99
  - camera - $21.99
  - HDMI to micro-HDMI adapter - $5.00
  - Lego for jar - 2 colors - $0.00
 
## AWS Services
- Rekognition
- Polly
- DynamoDB
- Lambda
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
1. call apis
    1. detect_faces
    1. recognize_celebrities
    1. detect_labels
    1. detect_text
1. store labels and counts to DynamoDB
    1. lambda triggered
    1. JavaScript generated on stats
    1. website updated with graph and photo booth
1. speaker emits voice of what is analyzed
1. return script to ready state

## Tasks
- direct and film video [GR]
- write screenplay for video [GR][JC]
- metric visualization [AS] 
  - dump the table to static JavaScript
  - bar charts on data frequency
  - other visualizations of the data collected
  - copy JavaScript to S3
- website [AS][SM]
  - configure S3 bucket for static hosting
  - open web gateway to S3 bucket
  - register and configure domain name with Route 53
  - build website with generated JavaScript
  - build photo booth with uploaded pictures in S3 bucket
- AWS Polly [KK][SM]
   - api call to render text-to-voice 
   - emit audio from mini-plug speaker
- IMDB [KK][MV]
  - code to crawl IMDB tiny URL to scrape data for celebrity
  - identity data to present - succinct and consistent
- fix camera fuzzy image [MV]
  - clean lens
  - check for focus api calls
- wire button [MV]
- code to interact with mechanical button and GPIO pinout [MV]
- GitHub [JC]
  - setup group and project
  - upload pilot code to GitHub 
    - api calls
    - motion sensor code (from old RaspPi)
  - add readme page
- setup init.d auto-run of main.py [JC]
- code to emit signal on main script start [JC]
- assemble main.py with nested while loops [JC]
- code to call detect_text [JC]
- update code to make api calls using uploaded S3 image
- upload image to S3 bucket [JC]
- DynamoDB [JC]
  - key: label or attribute
  - value: counter
  - code to insert data
            
## If we have time
- light source inside jar - led, rgb
- physical dial for confidence threshold
  - LED display % value [30%]
  - other visual representation of threshold gauges
    - thermometer - cylinder fill
    - rating meter
    - speedometer
- natural language processing with Lex
  - make the speech as humanlike as possible
    - inflections 
    - conversational
    - story telling
    - customized, personal, and unique
- 3D render animated face speaking with Polly
  - Apple memoji
  
## Types of pictures
- people
- name badges
- cell phone screen pictures (celebrities)
- objects
- signs
- rare items
- odd items
- scenery

