# DoorBot
Virtual home security doorbell system powered by facial and speech recognition. 

Ryan Hebert, Daniel Kantor & Patrick Kim
CSI 370

## Requirements
```
pip3 install cmake
pip3 install face_recognition
pip3 install numpy
pip3 install dlib
pip3 install opencv-python
pip3 install maria-db
pip3 install pyimgur
```

## Ngrok Set Up
Navigate to the [ngrok site](www.ngrok.com) to create an account and download the [ngrok client](www.ngrok.com/download). Run the commands below to unzip and authenticate your account with the provided auth token:
```
unzip /path/to/ngrok.zip
ngrok config add-authtoken <YOUR-TOKEN-HERE>
```
When completed, run the command below to begin the local host tunnel.
```
ngrok http <PORT>
```
Make sure the port used in the command is the same port that the Flask app runs in your code. After connected, copy the value of the `forwarding` key and save it for the next step. 

## Twilio Set Up
To create a Twilio account, go to [their website](www.twilio.com/) and create a trial account. Once granted a number, save the 10 digit (including the +1) for the `from_number` parameter in send message methods. Navigate to the Active Numbers tab and select your provided phone number. At the bottom of the page, enter the ngrok subdomain concatenated with "/sms" in the field that reads "A message comes in". This value is the address to which the webhook will look for to retrieve messages. 

## Running the Bot
To run DoorBot, ensure a camera is connected to the machine. First, make sure ngrok is connected and running. Next, run the Flask-server.py script and wait for a success message. Finally, run Bot.py in a separate shell.

## Developer Notes
This code is meant to be run on a Raspberry Pi 4, model B. Minor complciations may arise with different machines or operating systems. The Bot has a limited understanding of natural language. If your response seems to stump the Bot, please restart. The Bot expects single text responses. 

