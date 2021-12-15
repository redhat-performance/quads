#!/usr/bin/env python3
import aiohttp
import asyncio
import logging
import urllib3
from aiohttp import BasicAuth

from quads.config import conf

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class JiraException(Exception):
    pass


class Jira(object):
    def __init__(self, url, username=None, password=None, semaphore=None, loop=None):
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

        jira_auth = conf.get("jira_auth")
        if jira_auth and jira_auth == "token":
            token = conf.get("jira_token")
            if not token:
                raise JiraException(
                    "Jira authentication is set to BearerAuth but no "
                    "token has been defined on the configuration file"
                )
            payload = "Bearer: %s" % token
        else:
            if self.username and self.password:
                payload = BasicAuth(self.username, self.password)
            else:
                raise JiraException(
                    "Jira authentication is set to BasicAuth but no "
                    "username or password have been defined"
                )
        self.headers = {"Authorization": payload}

    def __exit__(self):
        if self.new_loop:
            self.loop.close()

    async def get_request(self, endpoint):
        logger.debug("GET: %s" % endpoint)
        try:
            async with aiohttp.ClientSession(
                headers=self.headers,
                loop=self.loop,
            ) as session:
                async with session.get(
                    self.url + endpoint,
                    verify_ssl=False,
                ) as response:
                    result = await response.json(content_type="application/json")
        except Exception as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return None
        if response.status == 404:
            logger.error("Resource not found: %s" % self.url + endpoint)
            return None
        return result

    async def post_request(self, endpoint, payload):
        logger.debug("POST: {%s:%s}" % (endpoint, payload))
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(
<<<<<<< HEAD
                    headers=self.headers,
                    loop=self.loop
=======
                    headers=self.headers, loop=self.loop
>>>>>>> 5f83082 (feat: Added token auth to jira library)
                ) as session:
                    async with session.post(
                        self.url + endpoint,
                        json=payload,
                        verify_ssl=False,
                    ) as response:
                        await response.json(content_type="application/json")
        except Exception as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status in [200, 201, 204]:
            logger.info("Post successful.")
            return True
        if response.status == 404:
            logger.error("Resource not found: %s" % self.url + endpoint)
        return False

    async def put_request(self, endpoint, payload):
        logger.debug("POST: {%s:%s}" % (endpoint, payload))
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(
<<<<<<< HEAD
                    headers=self.headers,
                    loop=self.loop
=======
                    headers=self.headers, loop=self.loop
>>>>>>> 5f83082 (feat: Added token auth to jira library)
                ) as session:
                    async with session.put(
                        self.url + endpoint,
                        json=payload,
                        verify_ssl=False,
                    ) as response:
                        await response.json(content_type="application/json")
        except Exception as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status in [200, 201, 204]:
            logger.info("Post successful.")
            return True
        if response.status == 404:
            logger.error("Resource not found: %s" % self.url + endpoint)
        return False

    async def add_watcher(self, ticket, watcher):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/watchers" % issue_id
        logger.debug("POST transition: {%s:%s}" % (issue_id, watcher))
        data = watcher
        response = await self.post_request(endpoint, data)
        return response

    async def add_label(self, ticket, label):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s" % issue_id
        data = {"update": {"labels": [{"add": label}]}}
        response = await self.put_request(endpoint, data)
        return response

    async def post_comment(self, ticket, comment):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/comment" % issue_id
        payload = {"body": comment}
        response = await self.post_request(endpoint, payload)
        return response

    async def post_transition(self, ticket, transition):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/transitions" % issue_id
        payload = {"transition": {"id": transition}}
        response = await self.post_request(endpoint, payload)
        return response

    async def get_transitions(self, ticket):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/transitions" % issue_id
        result = await self.get_request(endpoint)
        if not result:
            logger.error("Failed to get transitions")
            return []

        transitions = result.get("transitions")
        if transitions:
            return transitions
        else:
            logger.error("No transitions found under %s" % issue_id)
            return []

    async def get_ticket(self, ticket):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s" % issue_id
        result = await self.get_request(endpoint)
        if not result:
            logger.error("Failed to get ticket")
            return None
        return result

    async def get_watchers(self, ticket):
        issue_id = "%s-%s" % (conf["ticket_queue"], ticket)
        endpoint = "/issue/%s/watchers" % issue_id
        logger.debug("GET watchers: %s" % endpoint)
        result = await self.get_request(endpoint)
        if not result:
            logger.error("Failed to get watchers")
            return None
        return result

    async def get_pending_tickets(self):
        query = {"statusCategory": 4, "labels": "EXTENSION"}
        logger.debug("GET pending tickets")
        result = await self.search_tickets(query)
        if not result:
            logger.error("Failed to get pending tickets")
            return None
        return result

    async def search_tickets(self, query=None):
        project = {"project": conf["ticket_queue"]}
        prefix = "/search?jql="
        query_items = []

        if not query:
            query = project
        else:
            query.update(project)

        for k, v in query.items():
            query_items.append(f"{k}={v}")

        jql = " AND ".join(query_items)
        endpoint = f"{prefix}{jql}"
        logger.debug("GET pending tickets: %s" % endpoint)
        result = await self.get_request(endpoint)
        if not result:
            logger.error("Failed to get pending tickets")
            return None
        return result
