#Freshdesk SMS Notification System

This app is a basic implementation of a Freshdesk SMS notification system. The way that the notifications work, is that if you add a note to your ticket with the words SMS-NOTIFY at the top, it will send a text message notification with the text of the note. The client who recieved the notification could then reply to the message using their ticket number, and their message will be added as a note to the ticket.




##NOTE
 
 This will require a much more robust Database system to be used within any production environment! This is a very basic SQLite3 implementation and is used for proof of concept. 

###Authentication

To authenticate with Twilio, add your twilio api credentials to your env variables as labled in the script. To authenticated with Freshdesk, place your apikey and password within the fauth and fpword variables. (Note, not everyone has a password to use your personal Freshdesk API Key, if you don't just pass through random characters as it still requires something in the password field.)

###Twilio Config

Place your Twilio Programmable phone number under the #your phone number here comment block. To link the API to your Twilio number, using NGROK, create a self-hosted server and take the url of the server and place it in your twilio phone numbers message webhook config with https://your.url.here/sms/reply afterwards so we can trigger the reply function. 

I use NGROK in the example as its easy to use, and most people know how to use it, however this would work with literally any selfhosted solution.


###Freshdek Config
To grab customer information based on the Customers Freshdesk profile, you will need to create an automation on Freshdesk. Bind the automation a Status update, and create it triggers when you update the ticket to a specific status of your choosing. Finally set the POST request webhook url to the https://yourlinkhere/sms/notif. You can use the schema in the JSON file in this Repo to pull the correct Data from freshdesk. This will mean that when you update the Ticket with your status, it will trigger the webhook to send a POST request to the API with the information of the ticket. The API Then looks at the last note created on the ticket and Checks for the words SMS-NOTIFY in the field. If found, the API will take the phone number of the client, and text the client the note created.



##NOTE

This requires the client to have their Cellphone under the Mobile field in their Contact details. This will not grab the default phone number, in an attempt to avoid sending messages to landlines.


once running start up your NGROK instance, and test out the API!
