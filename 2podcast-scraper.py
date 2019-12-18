import time
import json
import sys
from requests import Session
from bs4 import BeautifulSoup as bs
from furl import furl

def update_url(previous_url, new_next_pub_date):
    """
    Updates the url's next_pub_date query parameters the data provided by the last
    query that was executed.
    """
    u = furl(previous_url)
    u.args['next_pub_date'] = new_next_pub_date
    return u.url

XHR = "https://www.listennotes.com/endpoints/v1/channels/4104fab13a6f4cb39b90a09a8c25d8d8/episodes?next_pub_date=1573825131000&prev_pub_date=1576589987000&sort_type=recent_first"

# get first episodes with bs
# acquire next_pub_date from that episode-pagination div
# use it to update_url()
# keep making requests to our special url as long as in the response, bundle.next=True

# next pub data value is todays datetime in unix millisecond
# updating next_pub_date to the response's next pub date should give us the
# next ten items from ajax

session = Session()

# head requests ask for *just* the headers, which is all you need to grab the
# session cookie to make ajax requests as if you are clicking the "load more"
# button
URL = 'https://www.listennotes.com/podcasts/the-what-bitcoin-did-podcast-peter-mccormack-4n2D3d67Yxk/'
session.head(URL)

def scrape(session, url, last_json=None, episodes=None):
    if last_json is not None:
        url = update_url(url, last_json['bundle']['next_pub_date'])
    if episodes is None:
        episodes = []

    response = session.get(
        url=url,
        headers={
            'referer': 'https://www.listennotes.com/'
        }
    )
    j = response.json()
    for episode in j['bundle']['episodes']:
            # episodes.append(episode) TODO why doesn't this work
            episodes.append(episode['title'])
            print(episode['title'])

    if j['bundle']['has_next']:
        return scrape(session, url, j, episodes)

    return episodes

episodes = scrape(session=session, url=XHR)
print(f"FINAL EPISODES LIST: {episodes}")
print(f"{len(episodes)} EPISODES SCRAPED")
sys.exit(0)
