from fastapi import Body, FastAPI, Response, Form
from twilio.rest import Client
import os
import re
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from freshdesk import add_note, custom_reply


#basic SQLite implementation, not intended for production use.
conn = sqlite3.connect("sms.db")

c = conn.cursor()

table = """CREATE TABLE sms (
           Phone VARCHAR(25), Ticket VARCHAR(10), status VARCHAR(255))"""

#freshdesk auth & password
fauth = ""
fpword = ""

#freshdesk environment, the first part of your companies freshdesk URL ie yourcompanyhere.freshdesk.com

freshenv = "yourcompanyhere"

#add twilio to your env variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

app = FastAPI()

class clientNumber(BaseModel):
    phoneNum: str
    ticket_status: str
    ticket_number: str


@app.get("/")
async def root():
    return {"message": "Hi"}


@app.post("/sms/notif")
async def sendNotif(item: clientNumber):
    custreply = "SMS-NOTIFY"
    client_number = item.phoneNum
    if "+1" in client_number:
        pass
    else:
        client_number = "+1"+str(client_number)
    print(item.ticket_status)
    c.execute("INSERT INTO sms VALUES ('"+str(client_number)+"','"+ str(item.ticket_number)+"','"+ str(item.ticket_status)+"')")
    conn.commit()

    print(c.fetchall())
    print(item)
    agent_response = custom_reply(freshenv, custreply, item.ticket_number, fauth, fpword)
    message = client.messages.create(
                                body='This is a notification from Dimmerdome Support about ticket #'+item.ticket_number+'. Your ticket has been set to ' + item.ticket_status + '. Your Support Agent left this note:\n "'+str(agent_response)+'" You can reply to this message by typing your ticket number, followed by your message.',
                                #Your Twilio Number here
                                from_='',
                                to=item.phoneNum
                            )

    print(message.sid)

    return {"message": "Message Sent!"}
    
@app.post("/sms/reply")
async def reply(From: str = Form(...), Body: str = Form(...)):
    
    resp = MessagingResponse()

    ticket_number = re.findall(r'(\d{6})', Body)
    print(str(ticket_number[0]))
    print(Body)
    if str(ticket_number[0]) in str(Body):

        #testing params to avoid any injections
        sql = "SELECT * FROM sms WHERE ticket = ?"
        args = str(ticket_number[0])
        c.execute(sql, (args,))
        conn.commit()
        ticket = c.fetchone()

        if ticket is None:
            resp.message(f"No ticket found.")
        elif str(ticket_number[0]) in str(ticket[1]):
            print(From)
            print(ticket[0])
            
            if str(ticket[0]) == str(From):
                resp.message(f"Response recieved! If your Support Agent has anymore questions they will contact you again. ")
                print(Body)
                add_note(freshenv, str(ticket_number[0]), Body, fauth, fpword)
            
            else:
                resp.message(f"You're trying to access this ticket from a different number. Please text using the original phone number.")


        
        else:
            resp.message(f"Ticket number not found!")
            
    else:
        resp.message(f"I'm sorry, your ticket hasn't been found. Please reply with your ticket number seperated by a space from the rest of your message.")


    return Response(content=str(resp), media_type="application/xml")