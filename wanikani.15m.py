#! /usr/bin/python3
from datetime import timedelta

import pandas as pd
import requests
from dateutil import tz
from dateutil.parser import parse
from pytz import timezone

USER_API_KEY = ""
USER_TIMEZONE = "Australia/Melbourne"

headers = {
    'Authorization': f'Bearer {USER_API_KEY}'
}

# lessons

_lesson_response = requests.request(
    "GET", "https://api.wanikani.com/v2/assignments?immediately_available_for_lessons", headers=headers)
_lesson_json = _lesson_response.json()
_lesson_length = str(len(_lesson_json['data']))

# reviews

_review_response = requests.request(
    "GET", "https://api.wanikani.com/v2/assignments?immediately_available_for_review", headers=headers)
_review_json = _review_response.json()
_review_length = str(len(_review_json['data']))

# upcoming

_upcoming_response = requests.request(
    "GET", "https://api.wanikani.com/v2/summary", headers=headers)
_upcoming_json = _upcoming_response.json()

if int(_review_length) > 0:
  print(f'🐊🦀 R{_review_length} | size=12')
elif int(_lesson_length) > 0:
  print(f'🐊🦀 L{_lesson_length} | size=12')
else:
  print('🐊🦀')

print('---')

print(f'Lessons: {_lesson_length} | href=https://www.wanikani.com/lesson')
print(f'Reviews: {_review_length} | href=https://www.wanikani.com/review')

# https://stackoverflow.com/questions/46736529/how-to-compute-the-time-difference-between-two-time-zones-in-python


def tz_diff(date, tz1, tz2):
    '''
    Returns the difference in hours between timezone1 and timezone2
    for a given date.
    '''
    date = pd.to_datetime(date)
    return (tz1.localize(date) -
            tz2.localize(date).astimezone(tz1))\
        .seconds/3600


DELTA = tz_diff('2022-01-01', timezone('UTC'), timezone(USER_TIMEZONE))
latest_date = parse('2022-01-01T00:00:00.000000Z')

for review in _upcoming_json['data']['reviews']:
  if (len(review['subject_ids']) > 0):
    date = parse(review['available_at']) + timedelta(DELTA)
    if (date.replace(hour=0, minute=0, second=0, microsecond=0) > latest_date.replace(hour=0, minute=0, second=0, microsecond=0)):
      latest_date = date
      print('---')
      print(f'{date.strftime("%A %d %b")} | size=10')
    subjects = len(review['subject_ids'])
    print(f'{date.strftime("%I:%M%p")} - {subjects} Reviews')
