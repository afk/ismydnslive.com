from flask import Flask, request
app = Flask(__name__)

import dns.resolver
import requests

ATLAS_API_KEY = ''

@app.route('/step1')
def step1():
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [request.args.get('ns')]
    return str(resolver.query(request.args.get('domain'), 'soa')[0].serial)

@app.route('/step2')
def step2():
    url = 'https://atlas.ripe.net/api/v2/measurements/?key=%s' % ATLAS_API_KEY
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {
        "definitions": [
            {
                "af": 4,
                "query_class": "IN",
                "query_type": "SOA",
                "query_argument": request.args.get('domain'),
                "use_macros": False,
                "description": "ismydnslive.com",
                "use_probe_resolver": True,
                "resolve_on_probe": False,
                "set_nsid_bit": False,
                "protocol": "UDP",
                "udp_payload_size": 512,
                "retry": 0,
                "skip_dns_check": False,
                "include_qbuf": False,
                "include_abuf": True,
                "prepend_probe_id": False,
                "set_rd_bit": False,
                "set_do_bit": False,
                "set_cd_bit": False,
                "timeout": 5000,
                "type": "dns"
            }
        ],
        "probes": [
            {
                "type": "area",
                "value": "WW",
                "requested": 10
            }
        ],
        "is_oneoff": True,
        "bill_to": "mail@timwattenberg.de"
    }
    r = requests.post(url, headers=headers, json=data)
    #return r.json()
    return r.text

@app.route('/step3/probe/<prb_id>')
def step3_probe(prb_id):
    url = 'https://atlas.ripe.net:443/api/v2/probes/%s/' % prb_id
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    return r.text
