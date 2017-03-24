#!/usr/bin/env python
import logging

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

PROXIES = {
    'http': '0.0.0.0:8118',
    'https': '0.0.0.0:8118'
}

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('root')
