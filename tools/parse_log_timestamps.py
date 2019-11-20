import re
import sys
from datetime import datetime


timestamps = []

file_name = './put2_requests_0.log'
if len(sys.argv) > 1:
	file_name = sys.argv[1]

with open() as f:
    for line in f:
        m = re.match(r'^[0-9]{1}\s[a-zA-Z0-9]{40,}\s(?P<nanos>.*)$', line)
        if m:
        	timestamps.append(m.group('nanos'))

for ts in timestamps:
    dt = datetime.utcfromtimestamp(int(ts) // 1000000000)
    print(dt)
    dt.strftime('%Y-%m-%d %H:%M:%S')