#!/usr/bin/env python3
import logging
import requests
import urllib3
from requests import RequestException

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Foreman(object):
    def __init__(self, url, username, password):
        logger.debug(":Initializing Foreman object:")
        self.url = url
        self.username = username
        self.password = password

    def get(self, endpoint):
        logger.debug("GET: %s" % endpoint)
        try:
            response = requests.get(
                self.url + endpoint,
                auth=(self.username, self.password),
                verify=False

            )
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return {}
        return response.json()

    def get_obj_dict(self, endpoint, identifier="name"):
        response_json = self.get(endpoint)
        if "results" in response_json:
            objects = {
                _object[identifier]: _object
                for _object in response_json["results"]
            }
        else:
            objects = {}
        return objects

    def set_host_parameter(self, host_name, name, value):
        host_parameter = self.get_host_parameter_id(host_name, name)
        if host_parameter:
            return self.put_host_parameter(host_name, host_parameter, value)
        else:
            return self.post_host_parameter(host_name, name, value)

    def put_host_parameter(self, host_name, parameter_id, value):
        logger.debug("PUT param: {%s:%s}" % (parameter_id, value))
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters/%s" % (_host_id, parameter_id)
        data = {'parameter': {"value": value}}
        try:
            response = requests.put(
                self.url + endpoint,
                json=data,
                auth=(self.username, self.password),
                verify=False)
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status_code in [200, 204]:
            return True
        return False

    def post_host_parameter(self, host_name, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters" % _host_id
        data = {"parameter": {"name": name, "value": value}}
        try:
            response = requests.post(
                self.url + endpoint,
                json=data,
                auth=(self.username, self.password),
                verify=False)
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status_code in [200, 201, 204]:
            return True
        return False

    def update_user_password(self, login, password):
        logger.debug("PUT login pass: {%s}" % login)
        _host_id = self.get_user_id(login)
        endpoint = "/users/%s" % _host_id
        data = {"user": {"login": login, "password": password}}
        try:
            response = requests.put(
                self.url + endpoint,
                json=data,
                auth=(self.username, self.password),
                verify=False)
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status_code in [200, 204]:
            return True
        return False

    def put_element(self, element_name, element_id, param_name, param_value):
        logger.debug("PUT param: {%s:%s}" % (param_name, param_value))
        endpoint = "/%s/%s" % (element_name, element_id)
        data = {
            element_name[:-1]: {param_name: param_value}
        }
        try:
            response = requests.put(
                self.url + endpoint,
                json=data,
                auth=(self.username, self.password),
                verify=False)
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status_code in [200, 204]:
            return True
        return False

    def put_parameter(self, host_name, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        _host_id = self.get_host_id(host_name)
        return self.put_element("hosts", _host_id, name, value)

    def put_parameter_by_name(self, host, name, value, identifier="name"):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        param_id = None
        if name == "media":
            put_name = "medium"
        else:
            put_name = name[:-1]
        endpoint = "/%s" % name
        result = self.get(endpoint)
        for item in result["results"]:
            if identifier in item and item[identifier] == value:
                param_id = item["id"]
                break
        if param_id:
            self.put_parameter(host, "%s_id" % put_name, param_id)
            self.put_parameter(host, "%s_name" % put_name, value)
            return True
        return False

    def get_idrac_host(self, host_name):
        logger.debug("GET idrac: %s" % host_name)
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/interfaces/" % _host_id
        result = self.get_obj_dict(endpoint)
        for interface, details in result.items():
            if "mgmt" in interface:
                return interface
        return None

    def get_idrac_host_with_details(self, host_name):
        logger.debug("GET idrac: %s" % host_name)
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/interfaces/" % _host_id
        result = self.get_obj_dict(endpoint)
        for interface, details in result.items():
            if "mgmt" in interface:
                return details
        return None

    def get_all_hosts(self):
        endpoint = "/hosts"
        return self.get_obj_dict(endpoint)

    def get_broken_hosts(self):
        endpoint = "/hosts?search=params.broken_state=true"
        return self.get_obj_dict(endpoint)

    def get_build_hosts(self, build=True):
        endpoint = "/hosts?search=build=%s" % str(build).lower()
        return self.get_obj_dict(endpoint)

    def get_parametrized(self, param, value):
        endpoint = "/hosts?search=%s=%s" % (param, value)
        return self.get_obj_dict(endpoint)

    def get_host_id(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = self.get_obj_dict(endpoint)
        _id = None
        if host_name in result:
            _id = result[host_name]["id"]
        return _id

    def get_host_parameter_id(self, host_name, parameter_name):
        host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters?search=name=%s" % (host_id, parameter_name)
        result = self.get_obj_dict(endpoint)
        _id = None
        if parameter_name in result:
            _id = result[parameter_name]["id"]
        return _id

    def get_user_id(self, user_name):
        endpoint = "/users?search=login=%s" % user_name
        result = self.get_obj_dict(endpoint, "login")
        _id = None
        if user_name in result:
            _id = result[user_name]["id"]
        return _id

    def get_role_id(self, role):
        endpoint = "/roles?search=name=%s" % role
        result = self.get_obj_dict(endpoint)
        _id = None
        if role in result:
            _id = result[role]["id"]
        return _id

    def get_host_param(self, host_name, param):
        _id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters?search=name=%s" % (_id, param)
        result = self.get_obj_dict(endpoint)
        if result:
            return {"result": result[param]["value"]}
        return

    def get_host_build_status(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = self.get_obj_dict(endpoint)
        build_status = result[host_name]["build_status"]
        return bool(build_status)

    def get_host_extraneous_interfaces(self, host_id):
        endpoint = "/hosts/%s/interfaces" % host_id
        response_json = self.get(endpoint)
        extraneous_interfaces = [i for i in response_json["results"] if i["identifier"] != "mgmt" and not i["primary"]]
        return extraneous_interfaces

    def remove_extraneous_interfaces(self, host):
        _host_id = self.get_host_id(host)
        success = True
        extraneous_interfaces = self.get_host_extraneous_interfaces(_host_id)
        for interface in extraneous_interfaces:
            endpoint = "/hosts/%s/interfaces/%s" % (_host_id, interface["id"])
            try:
                response = requests.delete(endpoint)
            except RequestException as ex:
                logger.debug(ex)
                logger.error("There was something wrong with your request.")
                success = False
                continue
            if response.status_code != 200:
                success = False
        return success

    def add_role(self, user_name, role):
        user_id = self.get_user_id(user_name)
        role_id = self.get_role_id(role)
        user_roles = self.get_user_roles(user_id)
        user_roles.append(role_id)
        return self.put_element("users", user_id, "role_ids", user_roles)

    def remove_role(self, user_name, role):
        user_id = self.get_user_id(user_name)
        role_id = self.get_role_id(role)
        user_roles = self.get_user_roles(user_id)
        if role_id in user_roles:
            user_roles.pop(user_roles.index(role_id))
        else:
            logger.warning("Nothing done. User does not have this role assigned.")
            return True
        return self.put_element("users", user_id, "role_ids", user_roles)

    def get_user_roles(self, user_id):
        endpoint = "/users/%s/roles" % user_id
        result = self.get_obj_dict(endpoint)
        result.pop("Default role")
        return [role["id"] for _, role in result.items()]
