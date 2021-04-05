import pprint
import time
import typing

import requests

def is_error_response(http_response, seconds_to_sleep: float = 1) -> bool:
  if http_response.status_code == 503:
    time.sleep(seconds_to_sleep)
    return False

  return http_response.status_code != 200


def get_json(url) -> typing.Union[dict, None]:
  response = requests.get(url)
  if is_error_response(response):
    return None
  json_response = response.json()
  return json_response


def get_reviews(app_id, page=1) -> typing.List[dict]:
  reviews: typing.List[dict] = [{}]

  while True:
    url = (f'https://itunes.apple.com/us/rss/customerreviews/page={page}/id={app_id}/sortBy=mostRecent/json')
    json = get_json(url)

    if not json:
      return reviews

    data_feed = json.get('feed')

    try:
      if not data_feed.get('entry'):
        get_reviews(app_id, page + 1)

      reviews += [{
        'review_id': entry.get('id').get('label'),
        'title': entry.get('title').get('label'),
        'author': entry.get('author').get('name').get('label'),
        'author_url': entry.get('author').get('uri').get('label'),
        'version': entry.get('im:version').get('label'),
        'rating': entry.get('im:rating').get('label'),
        'review': entry.get('content').get('label'),
        'vote_count': entry.get('im:voteCount').get('label'),
        'page': page
      } for entry in data_feed.get('entry') if not entry.get('im:name')]
      page += 1
    except Exception:
      return reviews

reviews = get_reviews('1447099435')
print(len(reviews))
pprint.pprint(reviews)