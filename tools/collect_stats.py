import time
import requests
from time import gmtime, strftime


dev_host = 'http://localhost:9200/'
i = 0

def nodes_request(host, with_headers):
    if with_headers:
        return requests.get(f"{host}_cat/nodes?v&h=n,hp,rp,rm,du,cpu,gc,qcm,rcm,fm")
    return requests.get(f"{host}_cat/nodes?h=n,hp,rp,rm,du,cpu,gc,qcm,rcm,fm")


while True:
    current_time = str(strftime("%Y-%m-%d_%H.%M.%S", gmtime()))

    if i == 0:
        resp = nodes_request(host=dev_host, with_headers=True)
        lines = resp.text.split('\n')
        print('\t'.join(lines[0].split()) + '\t' + 'time')
        for l in lines[1:len(lines)-1]:
            cells = l.split()
            if len(cells) > 0:
                print('\t'.join(cells) + '\t' + current_time)
    else:
        resp = nodes_request(host=dev_host, with_headers=False)
        lines = resp.text.split("\n")
        for l in lines:
            cells = l.split()
            if len(cells) > 0:
                print('\t'.join(cells) + '\t' + current_time)

    i += 1
    time.sleep(15)