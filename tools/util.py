import json

import requests
from urllib import parse


def load_file(filename):
    data = {}
    if filename:
        with open(filename, 'r') as f:
            data = json.load(f)
    return data


res = load_file('./msearches.json')
requests = {}
i = -1
x = 0
for line in res:
    i += 1
    srch = line['search']
    k = parse.quote_plus(line['endpoint'])
    if '_msearch' in line['endpoint']:
        x = i
        print(line['endpoint'], len(srch.split('\n')))
    try:
        requests[k] += 1
    except KeyError:
        requests[k] = 1

# Print one out for fun
print(res[x]['endpoint'], res[x]['search'])

# Print count, by endpoint
for k in requests:
    print(parse.unquote_plus(k), requests[k])
