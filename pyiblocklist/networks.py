# -*- coding: utf-8 -*-


from __future__ import absolute_import

import itertools

import netaddr
import requests

from .settings import ATTEMPT_COUNT
from .utils import try_if_empty


@try_if_empty(ATTEMPT_COUNT)
def extract_networks(urls):
    networks = itertools.chain.from_iterable(
        fetch_networks(url) for url in urls
    )
    return frozenset(networks)


def fetch_networks(url):
    http_response = requests.get(url, stream=True)
    for item in http_response.iter_lines(decode_unicode=False):
        for network in convert_to_ipnetwork(item):
            yield str(network)


def convert_to_ipnetwork(blocklist_line):
    chunks = blocklist_line.split(":")
    if len(chunks) != 2:
        return []

    ip_start, ip_finish = tuple(rng.strip() for rng in chunks[1].split("-"))
    return netaddr.IPRange(ip_start, ip_finish).cidrs()
