import requests 


#Repalce Freshdesk URL with your companies URL.

def add_note(companyenv, ticket, reply, auth, pword):

    url = "https://"+ companyenv + ".freshdesk.com/api/v2/tickets/" + str(ticket) + "/notes"
    headers = {'Content-Type': 'application/json'}
    reply_no_number = reply.replace(ticket, "")
    #apikey only here until env-variables are set
    data = {'body': str(reply_no_number)}
    r = requests.post(url, auth = (auth, pword), json=data, headers=headers)
    print(r.text)

def custom_reply(companyenv, custreply, ticket, auth, pword):
    headers = {'Content-Type': 'application/json'}

    r = requests.get("https://"+ companyenv + ".freshdesk.com/api/v2/tickets/"+ticket+"?include=conversations",auth = (auth,pword),  headers=headers)
    
    data = r.json()
    print(data)
    agent_note = data['conversations'][-1]['body_text'] 
    if custreply in agent_note:
        agent_note_noparam = agent_note.replace("SMS-NOTIFY", "")
        return agent_note_noparam
    
    else:
        return ""


def create_ticket(companyenv, message, phone_number, auth, pword):

    url = "https://"+ companyenv + ".freshdesk.com/api/v2/tickets/"

    data = {"description": message, "source": 3, "status": 2, "priority": 3, "phone": phone_number, "subject": "SMS Ticket: Client Requesting Help"}
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, auth = (auth, pword), json=data, headers=headers)


