#!/usr/bin/env python
import os
import re
import aiohttp
import async_timeout
import asyncio
import uvloop
import random

from pprint import pprint
from config import USER_AGENT, PROXIES, LOGGER


class InsDownload():
    """
    This async script can help you to download Instagram photos.
    """

    def __init__(self, single_url):
        self.single_url = single_url
        self._dir = 'data/'
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)

    async def fetch(self, client, url) -> bytes:
        """
        fetch url
        :param client: aiohttp client
        :param url: request url
        :return: response.read()
        """
        with async_timeout.timeout(10):
            try:
                headers = {'user-agent': self.get_random_user_agent()}
                proxy = PROXIES if PROXIES else None
                async with client.get(url, headers=headers, proxy=proxy) as response:
                    assert response.status == 200
                    LOGGER.info('Task url: {}'.format(response.url))
                    text = await response.read()
                    return text
            except Exception as e:
                LOGGER.exception(e)
                return None

    async def get_photo_url(self, loop) -> bool:
        """
        Get user photo's url
        :return: True or False
        """
        async with aiohttp.ClientSession(loop=None) as client:
            asyncio.sleep(1)
            html = await self.fetch(client=client, url=self.single_url)
            if html:
                preg_type = r"<meta\s*property=\"og:type\"\s*content=\"(.*?)\"\s*/>"
                type = re.findall(preg_type, str(html))
                if type:
                    if type[0] == "video":
                        preg_url = r"<meta\s*property=\"og:video\"\s*content=\"(.*?)\"\s*/>"
                    else:
                        preg_url = r"<meta\s*property=\"og:image\"\s*content=\"(.*?)\"\s*/>"
                    target_url_res = re.findall(preg_url, str(html))
                    if target_url_res:
                        target_url = target_url_res[0]
                        target_name = target_url[-25:].replace('/', '-')
                        if not os.path.exists(self._dir + target_name):
                            asyncio.sleep(random.randint(1, 2))
                            target_result = await self.fetch(client=client, url=target_url)
                            if target_result:
                                LOGGER.info("Downloading {target_url}".format(target_url=target_url))
                                try:
                                    with open(self._dir + target_name, 'wb') as file:
                                        file.write(target_result)
                                        LOGGER.info(
                                            'File downloaded successfully at {dir}'.format(dir=self._dir + target_name))
                                    return True
                                except Exception as e:
                                    LOGGER.exception(e)
                                    return False
                        else:
                            return True
                    return False
                else:
                    return False

    def get_random_user_agent(self) -> str:
        """
        Get a random user agent string.
        :return: Random user agent string.
        """
        try:
            with open('./user_agents.txt') as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [USER_AGENT]
        return random.choice(data)

    def start(self):
        """
        start crawling ins url
        :return:
        """
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.get_photo_url(loop=loop))
        loop.run_until_complete(task)
        return task.result()
