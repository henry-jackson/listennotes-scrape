import json
from requests import Session
from furl import furl

from scrape import scrape, current_milli_time

if __name__ == '__main__':
    session = Session()

    # head requests ask for *just* the headers, which is all you need to grab the
    # session cookie to make ajax requests as if you are clicking the 'load more'
    # button
    URL = 'https://www.listennotes.com/podcasts/the-what-bitcoin-did-podcast-peter-mccormack-4n2D3d67Yxk/'
    session.head(URL)

    # take an XHR endpoint that is used by the "Load more" button on the page
    sample_xhr = 'https://www.listennotes.com/endpoints/v1/channels/4104fab13a6f4cb39b90a09a8c25d8d8/episodes?next_pub_date=1573825131000'

    # update the next_pub_date query to be the current time in milliseconds
    u = furl(sample_xhr)
    u.args['next_pub_date'] = current_milli_time()

    # scrape until all episodes are loaded, starting with the 10 most recent
    # episodes from the current time
    episodes = scrape(session=session, url=u.url)
    print(f'{len(episodes)} EPISODES SCRAPED')

    # save all episode metadata to a file, overwrite if necessary in order to
    # update
    filename = 'what-bitcoin-did.json'
    with open(filename, 'w') as f:
        json.dump(episodes , f)

    print(f'Output saved to current directory as {filename}')
