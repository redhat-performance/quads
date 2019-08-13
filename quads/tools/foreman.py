#!/usr/bin/env python3
import aiohttp
import asyncio
import logging
import urllib3
from aiohttp import BasicAuth

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Foreman(object):
    def __init__(self, url, username, password, loop=None):
        logger.debug(":Initializing Foreman object:")
        self.url = url
        self.username = username
        self.password = password
        if not loop:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        connector = aiohttp.TCPConnector(loop=self.loop)
        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop)

    async def get(self, endpoint):
        logger.debug("GET: %s" % endpoint)
        try:
            async with self.session.get(
                    self.url + endpoint,
                    auth=BasicAuth(self.username, self.password),
            ) as response:
                result = await response.json()
        except Exception:
            logger.exception("There was something wrong with your request.")
            return {}
        return result

    async def get_obj_dict(self, endpoint, identifier="name"):
        response_json = await self.get(endpoint)
        objects = {}
        if "results" in response_json:
            objects = {
                _object[identifier]: _object
                for _object in response_json["results"]
            }
        return objects

    async def set_host_parameter(self, host_name, name, value):
        host_parameter = self.get_host_parameter_id(host_name, name)
        _host_id = self.get_host_id(host_name)
        if host_parameter:
            return await self.put_host_parameter(_host_id, host_parameter, value)
        else:
            return await self.post_host_parameter(_host_id, name, value)

    async def put_host_parameter(self, host_id, parameter_id, value):
        logger.debug("PUT param: {%s:%s}" % (parameter_id, value))
        endpoint = "/hosts/%s/parameters/%s" % (host_id, parameter_id)
        data = {'parameter': {"value": value}}
        try:
            async with self.session.put(
                    self.url + endpoint,
                    json=data,
                    auth=BasicAuth(self.username, self.password),
                    ) as response:
                await response.json()
        except Exception:
            logger.exception("There was something wrong with your request.")
            return False
        if response.status in [200, 204]:
            return True
        return False

    async def post_host_parameter(self, host_id, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        endpoint = "/hosts/%s/parameters" % host_id
        data = {"parameter": {"name": name, "value": value}}
        try:
            async with self.session.post(
                    self.url + endpoint,
                    json=data,
                    auth=BasicAuth(self.username, self.password),
                    ) as response:
                await response.json()
        except Exception:
            logger.exception("There was something wrong with your request.")
            return False
        if response.status in [200, 201, 204]:
            return True
        return False

    async def update_user_password(self, login, password):
        logger.debug("PUT login pass: {%s}" % login)
        _host_id = self.get_user_id(login)
        endpoint = "/users/%s" % _host_id
        data = {"user": {"login": login, "password": password}}
        try:
            async with self.session.put(
                    self.url + endpoint,
                    json=data,
                    auth=BasicAuth(self.username, self.password),
                    ) as response:
                await response.json()
        except Exception:
            logger.exception("There was something wrong with your request.")
            return False
        if response.status in [200, 204]:
            return True
        return False

    async def put_element(self, element_name, element_id, param_name, param_value):
        params = {
            param_name: param_value
        }
        results = await self.put_elements(element_name, element_id, params)
        return results

    async def put_elements(self, element_name, element_id, params):
        logger.debug("PUT param: %s" % params)
        endpoint = "/%s/%s" % (element_name, element_id)
        data = {
            element_name[:-1]: params
        }
        try:
            async with self.session.put(
                    self.url + endpoint,
                    json=data,
                    auth=BasicAuth(self.username, self.password),
                    ) as response:
                await response.json()
        except Exception:
            logger.exception("There was something wrong with your request.")
            return False
        if response.status in [200, 204]:
            return True
        return False

    async def put_parameter(self, host_name, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        _host_id = await self.get_host_id(host_name)
        return await self.put_element("hosts", _host_id, name, value)

    def put_parameters(self, host_name, params):
        logger.debug("PUT param: %s" % params)
        _host_id = self.get_host_id(host_name)
        return self.put_elements("hosts", _host_id, params)

    def put_parameters_by_name(self, host, params):
        logger.debug("PUT param: %s" % params)
        data = {}
        for param in params:
            param_name = param.get("name")
            param_value = param.get("value")
            param_identifier = param.get("identifier", "name")

            param_id = None
            if param_name == "media":
                put_name = "medium"
            else:
                put_name = param_name[:-1]
            endpoint = "/%s" % param_name
            result = self.get(endpoint)
            for item in result["results"]:
                if item.get(param_identifier, None) == param_value:
                    param_id = item["id"]
                    break
            if param_id:
                data["%s_id" % put_name] = param_id
                data["%s_name" % put_name] = param_value
        success = self.put_parameters(host, data)
        return success

    async def put_parameter_by_name(self, host, name, value, identifier="name"):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        param_id = None
        if name == "media":
            put_name = "medium"
        else:
            put_name = name[:-1]
        endpoint = "/%s" % name
        result = await self.get(endpoint)
        for item in result["results"]:
            if identifier in item and item[identifier] == value:
                param_id = item["id"]
                break
        if param_id:
            success = await self.put_parameter(host, "%s_id" % put_name, param_id)
            success = await self.put_parameter(host, "%s_name" % put_name, value) and success
            return success
        return False

    async def verify_credentials(self):
        endpoint = "/status"
        logger.debug("GET: %s" % endpoint)
        try:
            async with self.session.get(
                self.url + endpoint,
                auth=BasicAuth(self.username, self.password),
            ) as response:
                await response.json()
        except Exception:
            logger.exception("There was something wrong with your request.")
            return False
        if response.status == 200:
            return True
        return False

    async def get_idrac_host(self, host_name):
        logger.debug("GET idrac: %s" % host_name)
        _host_id = await self.get_host_id(host_name)
        endpoint = "/hosts/%s/interfaces/" % _host_id
        result = await self.get_obj_dict(endpoint)
        for interface, details in result.items():
            if "mgmt" in interface:
                return interface
        return None

    async def get_idrac_host_with_details(self, host_name):
        logger.debug("GET idrac: %s" % host_name)
        _host_id = await self.get_host_id(host_name)
        endpoint = "/hosts/%s/interfaces/" % _host_id
        result = await self.get_obj_dict(endpoint)
        for interface, details in result.items():
            if "mgmt" in interface:
                return details
        return None

    async def get_all_hosts(self):
        endpoint = "/hosts"
        return await self.get_obj_dict(endpoint)

    async def get_broken_hosts(self):
        endpoint = "/hosts?search=params.broken_state=true"
        return await self.get_obj_dict(endpoint)

    async def get_build_hosts(self, build=True):
        endpoint = "/hosts?search=build=%s" % str(build).lower()
        return await self.get_obj_dict(endpoint)

    async def get_parametrized(self, param, value):
        endpoint = "/hosts?search=%s=%s" % (param, value)
        return await self.get_obj_dict(endpoint)

    async def get_host_id(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = await self.get_obj_dict(endpoint)
        _id = None
        if host_name in result:
            _id = result[host_name]["id"]
        return _id

    async def get_host_parameter_id(self, host_name, parameter_name):
        host_id = await self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters?search=name=%s" % (host_id, parameter_name)
        result = await self.get_obj_dict(endpoint)
        _id = None
        if parameter_name in result:
            _id = result[parameter_name]["id"]
        return _id

    async def get_user_id(self, user_name):
        endpoint = "/users?search=login=%s" % user_name
        result = await self.get_obj_dict(endpoint, "login")
        _id = None
        if user_name in result:
            _id = result[user_name]["id"]
        return _id

    async def get_role_id(self, role):
        endpoint = "/roles?search=name=%s" % role
        result = await self.get_obj_dict(endpoint)
        _id = None
        if role in result:
            _id = result[role]["id"]
        return _id

    async def get_host_param(self, host_name, param):
        _id = await self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters?search=name=%s" % (_id, param)
        result = await self.get_obj_dict(endpoint)
        if result:
            return {"result": result[param]["value"]}
        return

    async def get_host_build_status(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = await self.get_obj_dict(endpoint)
        build_status = result[host_name]["build_status"]
        return bool(build_status)

    async def get_host_extraneous_interfaces(self, host_id):
        endpoint = "/hosts/%s/interfaces" % host_id
        response_json = await self.get(endpoint)
        extraneous_interfaces = [i for i in response_json["results"] if i["identifier"] != "mgmt" and not i["primary"]]
        return extraneous_interfaces

    async def remove_extraneous_interfaces(self, host):
        _host_id = await self.get_host_id(host)
        success = True
        extraneous_interfaces = await self.get_host_extraneous_interfaces(_host_id)
        for interface in extraneous_interfaces:
            endpoint = self.url + "/hosts/%s/interfaces/%s" % (_host_id, interface["id"])
            try:
                async with self.session.delete(
                    endpoint,
                    auth=BasicAuth(self.username, self.password),
                ) as response:
                    await response.json()
            except Exception:
                logger.exception("There was something wrong with your request.")
                success = False
                continue
            if response.status != 200:
                success = False
        return success

    async def add_role(self, user_name, role):
        user_id = await self.get_user_id(user_name)
        role_id = await self.get_role_id(role)
        user_roles = await self.get_user_roles(user_id)
        user_roles.append(role_id)
        return await self.put_element("users", user_id, "role_ids", user_roles)

    async def remove_role(self, user_name, role):
        user_id = await self.get_user_id(user_name)
        role_id = await self.get_role_id(role)
        user_roles = await self.get_user_roles(user_id)
        if role_id in user_roles:
            user_roles.pop(user_roles.index(role_id))
        else:
            logger.warning("Nothing done. User does not have this role assigned.")
            return True
        return await self.put_element("users", user_id, "role_ids", user_roles)

    async def get_user_roles(self, user_id):
        endpoint = "/users/%s/roles" % user_id
        result = await self.get_obj_dict(endpoint)
        result.pop("Default role")
        return [role["id"] for _, role in result.items()]
