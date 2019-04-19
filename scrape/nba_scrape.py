import requests
import json
import time
from fake_useragent import UserAgent

''' This module is for scraping data from stats.nba.com and
    saving it to a local .json file.

    functions:
        init_ua - starts UserAgent
        url_to_json - requests from a url

'''
ua = None


def url_to_json(segments, queries, mode='w'):
    '''Given a URL, send a request and download the info
        into a json file
        arguments:
            segments, queries - url string pieces
            mode - 'w' or 'a'
    '''
    global ua
    if ua is None:
        ua = UserAgent(verify_ssl=False, use_cache_server=False)
        # ua.update()
        print('Initialized UserAgent')

    url = ''
    for i in range(len(segments)):
        url += segments[i] + queries[i]

    head = {'user-agent': ua.safari}
    response = requests.get(url, headers=head)
    response.raise_for_status()
    data = response.json()

    dump_filename = ''
    if mode == 'a':
        dump_filename += 'Games' + queries[2]
    elif mode == 'w':
        for item in queries:
            dump_filename += item

    with open('data/'+dump_filename+'.json', mode) as outfile:
        if mode == 'a':
            outfile.write('\n')

        json.dump(data, outfile)

    print("Written to: " + dump_filename)
    time.sleep(5)
    return dump_filename
