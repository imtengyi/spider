#!/usr/bin/env python

import requests
import re
import random

from urllib.parse import urlparse

from config import USER_AGENT, PROXIES, LOGGER

url = "http://findmyfbid.in/"


def get_headers() -> dict:
    def get_random_user_agent() -> str:
        """
        Get a random user agent string.
        :return: Random user agent string.
        """
        try:
            with open('user_agents.txt') as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [USER_AGENT]
        return random.choice(data)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        'user-agent': get_random_user_agent()
    }

    return headers


def get_csrfmiddlewaretoken(headers) -> str:
    csrfmiddlewaretoken = ''
    try:
        result = requests.get(url="http://findmyfbid.in/", headers=headers, proxies=PROXIES, timeout=10).text
        preg = r"name='csrfmiddlewaretoken' value='(.*?)'"
        preg_token = re.findall(preg, result)
        if preg_token:
            csrfmiddlewaretoken = preg_token[0]
            LOGGER.info('successfully get  csrfmiddlewaretoken: [%s]' %
                        (csrfmiddlewaretoken))
    except Exception as e:
        LOGGER.exception(e)
    return csrfmiddlewaretoken


def facebook_convert_to_id(fb_url):
    # https://www.facebook.com/profile.php?id=1000
    url_parse = urlparse(fb_url)
    if "facebook.com" in url_parse.netloc:
        if "/profile.php" in url_parse.path:
            preg = "id=(\d{1,})"
            m = re.findall(preg, url_parse.query)
            if len(m):
                LOGGER.info('successfully converted facebook id for url : [%s to %s]' %
                            (fb_url, m[0]))
                return m[0]
        # https://facebook.com/zuck
        headers = get_headers()
        csrfmiddlewaretoken = get_csrfmiddlewaretoken(headers)
        if csrfmiddlewaretoken:
            data = {
                "csrfmiddlewaretoken": csrfmiddlewaretoken,
                "fburl": fb_url
            }
            headers.update(
                {"Cookie": "csrftoken={csrfmiddlewaretoken}".format(csrfmiddlewaretoken=csrfmiddlewaretoken)}
            )
            try:
                r = requests.post(
                    'http://findmyfbid.in/',
                    data=data,
                    timeout=10,
                    allow_redirects=False,
                    proxies=PROXIES,
                    headers=headers
                )
                location = r.headers['Location']
                preg = r'\d{1,}'
                m = re.findall(preg, location)
                if len(m):
                    LOGGER.info('successfully converted facebook id for url : [%s to %s]' %
                                (fb_url, m[0]))
                    return m[0]
                else:
                    return None
            except Exception as e:
                LOGGER.exception(e)
                return None
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    print(facebook_convert_to_id('https://facebook.com/zuck'))
