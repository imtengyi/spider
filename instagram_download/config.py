#!/usr/bin/env python
import logging

# PROXIES = {
#     'http': 'http://192.168.3.231:8118',
#     'https': 'http://192.168.3.231:8118',
# }

PROXIES = "http://0.0.0.0:8118"

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('instagram-download')
