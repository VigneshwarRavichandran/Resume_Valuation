from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

def create_event(email_ids, start_time, end_time, description):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './calendar_api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    EVENT = {
              "end": {
                "timeZone": "Asia/Kolkata",
                "dateTime": end_time
              },
              "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Kolkata"
              },
              "attendees": [],
              "reminders": {
                "useDefault": True
              },
              "description": description,
              "summary": "Interview Call",
              "location": "Chennai"
            }

    for email_id in email_ids:
        EVENT["attendees"].append({"email": email_id})

    event = service.events().insert(calendarId='primary', body=EVENT, sendNotifications=True).execute()
    return True
