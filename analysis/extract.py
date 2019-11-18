import glob
import json
import os

searches = []
autocompletes = []
msearches = []
loc = ''
endpoint = ''

query_types=('"query"', '"index"', '"sort"')

for f in glob.glob('data/sample/*.log'):
    for line in open(f):
        if '_msearch' in line:
            loc = line.replace('k3', 'k3_20191118144323')
            queries = []
        if line.startswith('{'):
            queries.append(line)
            continue
        else:
            if loc != "" and len(queries) > 0:
                searches.append({
                    'target': loc,
                    'endpoint': loc.strip('GET ').replace(' HTTP/1.1\n', ''),
                    'search': '\n'.join(queries)
                })
                queries = []


f2 = open("msearches.json", "w+")
f2.write(json.dumps(searches))
