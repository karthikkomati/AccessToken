from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


            

def AccessEmail():    
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    creds = None
    
    if os.path.exists('tokene.pickle'):
        with open('tokene.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('tokene.pickle', 'wb') as token:
            print("1")
            pickle.dump(creds, token)
    
    
    service = build('gmail', 'v1', credentials=creds)

    
    results = service.users().messages().list(userId='me').execute()
    #print(results)
    labels = results.get('messages', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        i = 0
        for label in labels:
            #print(label['id'])
            re = service.users().messages().get(userId='me',id=label['id']).execute()
            print(re['snippet'])
            print("---------------------------------------------")
            if i>10:
                break
            i+=1
def AccessCalender():
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.pickle', 'wb') as token:
            print("1")
            pickle.dump(creds, token)
    
    
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    


#AccessCalender()
AccessEmail()
