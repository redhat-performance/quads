#!/usr/bin/env python3
import aiohttp
import asyncio
import logging
import urllib3
from aiohttp import BasicAuth

from quads.config import conf

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Jira(object):
    def __init__(self, url, username, password, semaphore=None, loop=None):
        logger.debug(":Initializing Jira object:")
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

    async def post_comment(self, ticket, comment):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/comment" % issue_id
        logger.debug("POST comment: {%s:%s}" % (issue_id, comment))
        data = {"body": comment}
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(
                    loop=self.loop
                ) as session:
                    async with session.post(
                        self.url + endpoint,
                        json=data,
                        auth=BasicAuth(self.username, self.password),
                        verify_ssl=False,
                    ) as response:
                        await response.json(content_type="application/json")
        except Exception as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status in [200, 201, 204]:
            logger.info("Jira comment posted successfully.")
            return True
        if response.status == 404:
            logger.error("Resource not found: %s" % self.url + endpoint)
        return False

    async def post_transition(self, ticket, transition):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/transitions" % issue_id
        logger.debug("POST transition: {%s:%s}" % (issue_id, transition))
        data = {"transition": {"id": transition}}
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(
                    loop=self.loop
                ) as session:
                    async with session.post(
                        self.url + endpoint,
                        json=data,
                        auth=BasicAuth(self.username, self.password),
                        verify_ssl=False,
                    ) as response:
                        await response.json(content_type="application/json")
        except Exception as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status in [200, 201, 204]:
            logger.info("Transition updated correctly.")
            return True
        if response.status == 404:
            logger.error("Resource not found: %s" % self.url + endpoint)
        return False

    async def get_transitions(self, ticket):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/transitions" % issue_id
        logger.debug("GET transitions: %s" % endpoint)
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
            return []
        if response.status == 404:
            logger.error("Resource not found: %s" % self.url + endpoint)
            return []

        transitions = result.get("transitions")
        if transitions:
            return transitions
        else:
            logger.error("No transitions found under %s" % issue_id)
            return []
