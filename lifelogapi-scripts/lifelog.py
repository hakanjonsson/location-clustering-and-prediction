import sys, logging

import json
import urllib2

import config

def do_request(access_token, url):
    headers = {'Authorization': 'Bearer %s' % (access_token)}
    req = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(req).read()

def get_user(access_token):
    try:
        contents = do_request(access_token, config.LL_API_BASE + '/users/me')
    except urllib2.HTTPError, e:
        logging.warn("lifelog.get_user(): Caught HTTPError, status code: %d, reason: %s" % (e.code, e.reason))
        return None
    return json.loads(contents)['result'][0]

def get_all_from_endpoint(access_token, endpoint, file, content = "json", indent = None):
    '''Get all pages from a specific endpoint and save to file.
    'content' is json as default and the only format supported right now, with optional indentation
    set through 'indent'.'''
    file.write('[\n')
    next_url = config.LL_API_BASE + '/users/me/' + endpoint
    while next_url is not None:
        logging.debug("lifelog.get_all_from_endpoint(): next url: %s" % (next_url))
        contents = do_request(access_token, next_url)
        reply = json.loads(contents)
        if 'links' in reply:
            next_url = reply['links'][0]['href']
        else:
            next_url = None
        file.write(",".join([json.dumps(item, indent=indent) for item in reply['result']]))
        if next_url is not None:
           file.write(",")
    file.write(']\n')

