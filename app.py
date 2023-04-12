import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import openai
import pytz

# replace with your own credentials and calendar ID
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'
CALENDAR_ID = 'your.calendar.id@domain.com'

# authenticate with OpenAI
openai.api_key = 'your_openai_api_key'

def create_event(start_time, end_time, summary):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York',
        },
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    st.write('Event created: %s' % (event.get('htmlLink')))

st.title("Calendar Event Creator")

prompt = st.text_input("Enter your calendar event prompt:")

if st.button("Create Events"):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    events = response.choices[0].text.split('\n')

    start_time = datetime.now()
    start_time = pytz.timezone('America/New_York').localize(start_time)

    for i, summary in enumerate(events):
        end_time = start_time + timedelta(hours=1)
        create_event(start_time, end_time, summary.strip())
        start_time = start_time + timedelta(days=1)
