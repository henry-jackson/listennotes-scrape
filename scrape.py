from furl import furl

def update_url(previous_url, new_next_pub_date):
    """
    Updates the url's next_pub_date query parameters the data provided by the last
    query that was executed.
    """
    u = furl(previous_url)
    u.args['next_pub_date'] = new_next_pub_date
    return u.url

def scrape(session, url, last_json=None, episodes=None):
    """
    Recursively scrape until the XHR response states that there is no more
    data that follows, then return the list of all episode json
    """
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
            print(episode['title'])
            episodes.append(episode)

    if j['bundle']['has_next']:
        return scrape(session, url, j, episodes)

    return episodes
