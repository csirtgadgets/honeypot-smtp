#!/bin/bash

set -e

VERSION="$1"

docker tag csirtgadgets/honeypot-smtp:latest csirtgadgets/honeypot-smtp:${VERSION}
docker push csirtgadgets/honeypot-smtp:latest
docker push csirtgadgets/honeypot-smtp:${VERSION}
