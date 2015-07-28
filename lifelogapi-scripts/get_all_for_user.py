#!/usr/bin/env python

import sys, logging, argparse
import json, urllib2,cStringIO
from datetime import datetime
from gzip import GzipFile

import config
import lifelog

logging.getLogger().setLevel(logging.DEBUG)
parser = argparse.ArgumentParser(description="Get all data for a user through the Lifelog public API")
parser.add_argument('--access_token', '-a', required=True,
   help='Access token to use, required')
parser.add_argument('--indent', '-i', default=None, type=int, 
   help='Indentation of JSON output, default is None')
parser.add_argument('--gzip', '-z', action="store_true",
   help='Gzip compress output')
args = parser.parse_args()

user_access_token = args.access_token
headers = {'Authorization': 'Bearer %s' % (user_access_token)}

user = lifelog.get_user(user_access_token)
file_prefix = "%s-%s" % (user['username'], datetime.now().strftime('%FT%T.000%z'))
file_suffix = 'json'
if args.gzip:
    file_suffix += '.gz'

for endpoint in ('locations', 'activities'):
    output_filename = "%s-%s.%s" % (file_prefix, endpoint, file_suffix)
    output = cStringIO.StringIO()
    if args.gzip:
        with GzipFile(fileobj=output, mode="wb") as gz:
            lifelog.get_all_from_endpoint(user_access_token, endpoint, gz)
    else:
        lifelog.get_all_from_endpoint(user_access_token, endpoint, output)
    with open(output_filename, "w") as out:
        out.write(output.getvalue())
        output.close()
