#!/usr/bin/env python3
import asyncio
import aiohttp
import logging
import urllib3
from aiohttp import BasicAuth

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, url, username, password, semaphore=None, loop=None):
        logger.debug(":Initializing Manager object:")
        self.url = url
        self.username = username
        self.password = password
        if not loop:
            self.loop = asyncio.new_event_loop()
            self.new_loop = True
        else:
            self.loop = loop
            self.new_loop = False
        if not semaphore:
            self.semaphore = asyncio.Semaphore(20)
        else:
            self.semaphore = semaphore

    def __exit__(self):
        if self.new_loop:
            self.loop.close()

    async def get(self, endpoint):
        logger.debug("GET: %s" % endpoint)
        try:
            async with aiohttp.ClientSession(
                loop=self.loop
            ) as session:
                async with session.get(
                    self.url + endpoint,
                    auth=BasicAuth(self.username, self.password),
                    verify_ssl=False,
                ) as response:
                    result = await response.json(content_type="application/json")
        except Exception as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return {}
        return result

    async def update_user_password(self, login, password):
        pass

    async def verify_credentials(self):
        pass

    async def get_all_hosts(self):
        pass

    async def get_build_hosts(self, build=True):
        pass

    async def get_host_id(self, host_name):
        pass

    async def get_user_id(self, user_name):
        pass

    async def get_host_build_status(self, host_name):
        pass

    async def add_role(self, user_name, role):
        pass

    async def remove_role(self, user_name, role):
        pass

    async def get_user_roles(self, user_id):
        pass
