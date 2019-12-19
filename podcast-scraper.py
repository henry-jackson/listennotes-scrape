import time # necessary?
from requests import Session
from bs4 import BeautifulSoup as bs

from scrape import scrape


XHR = 'https://www.listennotes.com/endpoints/v1/channels/4104fab13a6f4cb39b90a09a8c25d8d8/episodes?next_pub_date=1573825131000&prev_pub_date=1576589987000&sort_type=recent_first'

# get first episodes with bs ?
# acquire next_pub_date from that episode-pagination div
# use it to update_url()
# keep making requests to our special url as long as in the response, bundle.next=True

# next pub data value is todays datetime in unix millisecond
# updating next_pub_date to the response's next pub date should give us the
# next ten items from ajax

session = Session()

# head requests ask for *just* the headers, which is all you need to grab the
# session cookie to make ajax requests as if you are clicking the 'load more'
# button
URL = 'https://www.listennotes.com/podcasts/the-what-bitcoin-did-podcast-peter-mccormack-4n2D3d67Yxk/'
session.head(URL)

# TODO beautiful soup the first page for first 10 episodes.
# soup = session.get(URL).content
# episodes = []
# for header in soup.find_all('h3', {'class': 'ln-channel-episode-card-info-title'}):
    # episode_urls.append(header.find('a').get('href'))

# episodes = scrape(session=session, url=XHR, episodes=episodes)

# TODO new plan: try to force XHR request that loads initial episodes onto the
# page


episodes = scrape(session=session, url=XHR)
print(f'{len(episodes)} EPISODES SCRAPED')
