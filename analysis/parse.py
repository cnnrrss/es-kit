import json
import glob

totals = []

loc = ''
searches = []

state = 0

for f in glob.glob('sample/*.log'):
	loc = ''
	state = 0
	for line in open(f):
		if line.startswith('1 '):
			state = 1
			loc = loc.strip('GET ').replace(''' HTTP/1.1\n''', '')
			loc = loc.strip('GET ').replace(''' HTTP/1.1\r\n''', '')
			loc = loc.replace('k3', 'k3_20191118144323')

			# if you want a sample...
			# if '_msearch' in loc:
			# 	print loc
			# 	print ''.join(searches).strip()
			# 	break

			if loc != '':
				totals.append({
					'endpoint': loc,
					'search': '@@@@'.join([x.strip() for x in searches]).strip()
				})

				loc = ''
				searches = []


		if state == 1:
			if '_search' in line:
				loc = line
				state = 2
			if '_msearch' in line:
				loc = line
				state = 3

		if state == 2:
			if line.startswith('{'):
				searches.append(line)
		if state == 3:
			if line.startswith('{'):
				searches.append(line)


# print json.dumps(totals)

for r in totals:
	print r['endpoint'] + "||" + r['search']
