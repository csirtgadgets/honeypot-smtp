#!/bin/bash

set -e

docker build --rm=true --force-rm=true -t csirtgadgets/honeypot-smtp -f docker/Dockerfile .
