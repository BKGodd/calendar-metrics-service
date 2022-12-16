from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os
import datetime


def auth_google():
    """
    Authenticates the Google Calendar API

    Returns:
        Credential object: for creating and using API services
    """
    # This scope needs to be changed depending on which API we are accessing
    scope = 'https://www.googleapis.com/auth/calendar.events'
    creds = None
    # Read from local token file, create from credential JSON if DNE
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def webhook(creds, uuid, address):
    """
    Creates a webhook with the Google Calendar API

    Inputs:
        creds (Credential object): used for authenticating the service
        uuid (str): identifier for creating a webhook channel
        address (str): public-facing web address where Calendar updates will be received

    Returns:
        None
    """
    # Watch the calendar events, resulting in POST updates to the provided address
    service = build('calendar', 'v3', credentials=creds)
    data = {'id': uuid,
            'type': 'web_hook',
            'address': address}
    watch_result = service.events().watch(calendarId=os.environ['CAL_ID'], body=data).execute()

    # Check response if channel was correctly created
    assert watch_result['kind'] == 'api#channel', f'Error occurred when requesting webhook: {watch_result}'
        

def calc_metrics(creds):
    """
    Calculates common metrics for the user, using the Google Calendar API

    Inputs:
        creds (Credential object): used for authenticating the service

    Returns:
        None
    """
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API ("Z" indicates UTC time)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=os.environ['CAL_ID'], timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    # TODO: Instead of simply printing to the console, you can do anything 
    #       you want at this point!

    # Prints the start time and name of the next 10 events to the console
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event.get('summary', '(no title)'))
