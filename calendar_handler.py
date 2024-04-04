import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Union

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

PERSONAL_CALENDAR_IDS = [
    'addressbook#contacts@group.v.calendar.google.com',
    'rickycrvt@gmail.com',
    'en.usa#holiday@group.v.calendar.google.com'
]


class CalendarScraperHandler:
    def __init__(self):
        self.creds = None
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        self.events_dict_list = []
        self.calendar_id_list = []

    def get_calendar_events(self, calendar_id: str) -> List[Dict[str, Union[str, int]]]:
        try:
            service = build("calendar", "v3", credentials=self.creds)

            # Call the Calendar API

            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=now,
                    maxResults=2,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            events_dict_list = []
            for event in events:
                event_dict = {
                    "host_event_id": event["id"],
                    "event_name": event["summary"],
                    "event_description": event["description"],
                    "event_price": 0,
                    "event_start_date": event["start"].get("dateTime", event["start"].get("date")),
                    "event_end_date": event["end"].get("dateTime", event["end"].get("date")),
                    "event_location": event["location"] if "location" in event else "Online",
                }
                print(event_dict)
                events_dict_list.append(event_dict)
            return events_dict_list

        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_calendar_list(self) -> List[Dict[str, Union[str, int]]]:
        try:
            service = build("calendar", "v3", credentials=self.creds)
            print("Getting CalendarIDs")
            page_token = None
            calendars = []
            while True:
                calendar_list = service.calendarList().list(pageToken=page_token).execute()
                for calendar_list_entry in calendar_list['items']:
                    if calendar_list_entry['id'] not in PERSONAL_CALENDAR_IDS:
                        calendars.append(
                            {
                                "host_calendar_id": calendar_list_entry['id'],
                                "host_name": calendar_list_entry['summary'],
                                "host_description": calendar_list_entry['description'],
                            }
                        )
                page_token = calendar_list.get('nextPageToken')
                if not page_token:
                    break
            print("Calendars: ", calendars)
            return calendars
        except HttpError as error:
            print(f"An error occurred: {error}")
