# honeypot-smtp
a simple SMTP honeypot for logging odd SMTP connections to CSIRTG.

```bash
# from docker/run.sh
$ export CSIRTG_USER=wes
$ export CSIRTG_FEED=smtp
$ export CSIRTG_TOKEN=1234..

$ docker pull csirtgadgets/honeypot-smtp

$ docker run -d --name honeypot-smtp \
  -p 25:2525 \
  -e CSIRTG_USER=${CSIRTG_USER} \
  -e CSIRTG_FEED=${CSIRTG_FEED} \
  -e CSIRTG_TOKEN=${CSIRTG_TOKEN} \
  -e TRACE=1 \
  csirtgadgets/honeypot-smtp
```

```bash
$ docker log honeypot-smtp -f
2019-02-09 15:52:47,180 - INFO - __main__[129] - listening on localhost:2525
2019-02-09 15:52:47,180 - INFO - __main__[137] - Logging indicators to wes/smtp
2019-02-09 15:52:49,707 - DEBUG - __main__[58] - {
    "user": "wes",
    "feed": "smtp",
    "indicator": "172.17.0.1",
    "tags": [
        "smtp",
        "spam",
        "relay"
    ],
    "description": "peer using open smtp relay",
    "portlist": "25",
    "lasttime": "2019-02-09T15:52:49.1549727569Z",
    "content": null
}
2019-02-09 15:52:49,928 - DEBUG - __main__[63] - {'id': 13375931, 'indicator': '172.17.0.1', 'itype': 'ipv4', 'portlist': '25', 'count': 21, 'protocol': None, 'firsttime': '2019-02-09 14:50:40 UTC', 'lasttime': '2019-02-09 15:52:49 UTC', 'created_at': '2019-02-09 14:50:40 UTC', 'updated_at': '2019-02-09 15:52:49 UTC', 'description': 'peer using open smtp relay', 'portlist_src': None, 'asn': None, 'asn_desc': None, 'cc': None, 'provider': None, 'license': {'name': 'CC BY-SA 4.0', 'url': 'http://creativecommons.org/licenses/by-sa/4.0/'}, 'content': None, 'feed': 'smtp', 'user': 'wes', 'location': 'https://csirtg.io/users/wes/feeds/smtp/indicators/13375931'}
```