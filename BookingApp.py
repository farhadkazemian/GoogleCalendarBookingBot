from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate and return the Google Calendar API service."""
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
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

def get_free_slots(service, calendar_id='primary', days=7):
    """Get free 30-minute slots from 6 PM to 8 PM daily, excluding busy times in Google Calendar."""
    # Define Iran Standard Time (UTC+3:30)
    IRST = timezone(timedelta(hours=3, minutes=30))

    # Get the current time in UTC and calculate the time range
    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=days)).isoformat()

    # Fetch events from the calendar
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # Collect busy times
    busy_times = []
    for event in events:
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        if start and end:
            start = datetime.fromisoformat(start).astimezone(IRST)
            end = datetime.fromisoformat(end).astimezone(IRST)
            busy_times.append((start, end))

    # Define 30-minute slots (6 PM to 8 PM daily)
    free_slots = []
    for day in range(days):
        day_start = (now + timedelta(days=day)).astimezone(IRST).replace(hour=18, minute=0, second=0, microsecond=0)
        for i in range(4):  # Four 30-minute slots
            slot_start = day_start + timedelta(minutes=30 * i)
            slot_end = slot_start + timedelta(minutes=30)

            # Check if the slot conflicts with any busy time
            conflict = False
            for busy_start, busy_end in busy_times:
                if slot_start < busy_end and slot_end > busy_start:
                    conflict = True
                    break

            if not conflict:
                free_slots.append((slot_start, slot_end))

    return free_slots

def book_demo(service, calendar_id, start, end, participants):
    """Book a demo by creating an event in Google Calendar with participants and notifications."""
    event = {
        'summary': 'ITvisa Meeting',
        'description': 'We are looking forward to show the demo!',
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Tehran'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Tehran'},
        'attendees': [{'email': email} for email in participants],
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string',  # Unique string to avoid duplicate requests
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 30},  # Email reminder 30 minutes before
                {'method': 'popup', 'minutes': 30},  # Popup reminder 30 minutes before
            ],
        },
    }
    created_event = service.events().insert(
        calendarId=calendar_id, body=event, conferenceDataVersion=1, sendUpdates='all'
    ).execute()
    return created_event

def chatbot():
    """Simple chatbot to suggest free slots, add participants, and book a demo."""
    service = authenticate_google_calendar()
    free_slots = get_free_slots(service)

    if not free_slots:
        print("No free slots available for the next 7 days.")
        return

    print("Welcome to the Demo Booking Chatbot!")
    print("Here are the available 30-minute slots for the next 7 days (in IRST):")
    for i, (start, end) in enumerate(free_slots):
        print(f"{i + 1}. {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')}")

    choice = int(input("Please select a slot (enter the number): ")) - 1
    if 0 <= choice < len(free_slots):
        start, end = free_slots[choice]

        # Get participant emails
        participants = input(
            "Enter participant email addresses (comma-separated): "
        ).split(',')

        # Book the demo
        event = book_demo(service, 'primary', start, end, participants)
        print(f"Demo booked successfully! Event ID: {event['id']}")
        print(f"Google Meet Link: {event['hangoutLink']}")
    else:
        print("Invalid choice. Please try again.")

if __name__ == '__main__':
    chatbot()


