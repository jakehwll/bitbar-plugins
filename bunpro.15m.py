#! /usr/bin/python3
import requests

USER_API_KEY = ""

# reviews

_review_response = requests.request(
    "GET", f"https://bunpro.jp/api/user/{USER_API_KEY}/study_queue")
_review_json = _review_response.json()
_review_length = str(_review_json['requested_information']['reviews_available'])

if int(_review_length) > 0:
  print(f'🈸 R{_review_length} | size=12')
else:
  print('🈸 | size=12')

print('---')

print(f'Reviews: {_review_length} | href=https://bunpro.jp/study')
