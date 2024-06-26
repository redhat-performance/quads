#!/usr/bin/env python3
import asyncio

import aiohttp
from aiohttp import BasicAuth

import json
import logging
import os
import re
import sys
import warnings
import yaml

warnings.filterwarnings("ignore")

RETRIES = 15

logger = logging.getLogger(__name__)


async def badfish_factory(_host, _username, _password, loop=None, _retries=RETRIES, propagate=False):
    logger.propagate = propagate
    badfish = Badfish(_host, _username, _password, loop, _retries=RETRIES)
    await badfish.init()
    return badfish


class BadfishException(Exception):
    pass


class Badfish:
    def __init__(self, _host, _username, _password, loop=None, _retries=RETRIES):
        self.host = _host
        self.username = _username
        self.password = _password
        self.retries = _retries
        self.host_uri = "https://%s" % _host
        self.redfish_uri = "/redfish/v1"
        self.root_uri = "%s%s" % (self.host_uri, self.redfish_uri)
        self.semaphore = asyncio.Semaphore(50)
        if not loop:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.system_resource = None
        self.manager_resource = None
        self.bios_uri = None
        self.boot_devices = None

    async def init(self):
        await self.validate_credentials()
        self.system_resource = await self.find_systems_resource()
        self.manager_resource = await self.find_managers_resource()
        self.bios_uri = "%s/Bios/Settings" % self.system_resource[len(self.redfish_uri) :]

    @staticmethod
    def progress_bar(value, end_value, state, bar_length=20):
        ratio = float(value) / end_value
        arrow = "-" * int(round(ratio * bar_length) - 1) + ">"
        spaces = " " * (bar_length - len(arrow))
        percent = int(round(ratio * 100))

        if state.lower() == "on":
            state = "On  "
        ret = "\r" if percent != 100 else "\n"
        sys.stdout.write("\r- POLLING: [{0}] {1}% - Host state: {2}{3}".format(arrow + spaces, percent, state, ret))
        sys.stdout.flush()

    @staticmethod
    async def error_handler(_response):
        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        except Exception:
            logger.error("Error reading response from host.")
            raise BadfishException

        if "error" in data:
            message = data["error"]["@Message.ExtendedInfo"][0].get("Message")
            if not message:
                message = data["error"]["@Message.ExtendedInfo"][0].get("MessageArgs")
            detail_message = str(message)
            logger.warning(detail_message)

        raise BadfishException

    async def get_request(self, uri, _continue=False):
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(loop=self.loop) as session:
                    async with session.get(
                        uri,
                        auth=BasicAuth(self.username, self.password),
                        verify_ssl=False,
                        timeout=120,
                    ) as _response:
                        await _response.text("utf-8", "ignore")
        except Exception as ex:
            if _continue:
                return
            else:
                logger.debug(str(ex))
                raise BadfishException("Failed to communicate with server.")
        return _response

    async def post_request(self, uri, payload, headers):
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(loop=self.loop) as session:
                    async with session.post(
                        uri,
                        data=json.dumps(payload),
                        headers=headers,
                        auth=BasicAuth(self.username, self.password),
                        verify_ssl=False,
                        timeout=120,
                    ) as _response:
                        if _response.status != 204:
                            await _response.text("utf-8", "ignore")
                        else:
                            return _response
        except (Exception, TimeoutError):
            logger.exception("Failed to communicate with server.")
            raise BadfishException
        return _response

    async def patch_request(self, uri, payload, headers, _continue=False):
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(loop=self.loop) as session:
                    async with session.patch(
                        uri,
                        data=json.dumps(payload),
                        headers=headers,
                        auth=BasicAuth(self.username, self.password),
                        verify_ssl=False,
                        timeout=120,
                    ) as _response:
                        await _response.text("utf-8", "ignore")
        except Exception as ex:
            if _continue:
                return
            else:
                logger.debug(ex)
                logger.error("Failed to communicate with server.")
                raise BadfishException
        return _response

    async def delete_request(self, uri, headers):
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(loop=self.loop) as session:
                    async with session.delete(
                        uri,
                        headers=headers,
                        auth=BasicAuth(self.username, self.password),
                        ssl=False,
                    ) as _response:
                        await _response.read()
        except (Exception, TimeoutError):
            logger.exception("Failed to communicate with server.")
            raise BadfishException
        return _response

    async def get_interfaces_by_type(self, host_type, _interfaces_path):
        definitions = await self.read_yaml(_interfaces_path)

        host_name_split = self.host.split(".")[0].split("-")
        host_model = host_name_split[-1]
        host_blade = host_name_split[-2]
        uloc = host_name_split[-3]
        rack = host_name_split[-4]

        prefix = [host_type, rack, uloc]

        b_pattern = re.compile("b0[0-9]")
        if b_pattern.match(host_blade):
            host_model = "%s_%s" % (host_model, host_blade)

        len_prefix = len(prefix)
        for _ in range(len_prefix):
            prefix_string = "_".join(prefix)
            key = "%s_%s_interfaces" % (prefix_string, host_model)
            interfaces_string = definitions.get(key)
            if interfaces_string:
                return interfaces_string.split(",")
            else:
                prefix.pop()

        logger.error(f"Couldn't find a valid key defined on the interfaces yaml: {key}")
        raise BadfishException

    async def get_boot_seq(self):
        bios_boot_mode = await self.get_bios_boot_mode()
        if bios_boot_mode == "Uefi":
            return "UefiBootSeq"
        else:
            return "BootSeq"

    async def get_bios_boot_mode(self):
        logger.debug("Getting bios boot mode.")
        _uri = "%s%s/Bios" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_uri)

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        except ValueError:
            logger.error("Could not retrieve Bios Boot mode.")
            raise BadfishException

        try:
            bios_boot_mode = data["Attributes"]["BootMode"]
            return bios_boot_mode
        except KeyError:
            logger.warning("Could not retrieve Bios Attributes. Assuming Bios.")
            return "Bios"

    async def get_boot_devices(self):
        if not self.boot_devices:
            _boot_seq = await self.get_boot_seq()
            _uri = "%s%s/BootSources" % (self.host_uri, self.system_resource)
            _response = await self.get_request(_uri)

            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            if "Attributes" in data:
                try:
                    self.boot_devices = data["Attributes"][_boot_seq]
                except KeyError:
                    logger.error("No boot devices found")
                    raise BadfishException
            else:
                logger.debug(data)
                logger.error("Boot order modification is not supported by this host.")
                raise BadfishException

    async def get_job_queue(self):
        logger.debug("Getting job queue.")
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _response = await self.get_request(_url)

        data = await _response.text("utf-8", "ignore")
        job_queue = re.findall(r"[JR]ID_.+?\d+", data)
        jobs = [job.strip("}").strip('"').strip("'") for job in job_queue]
        return jobs

    async def get_job_status(self, _job_id):
        logger.debug("Getting job status.")
        _uri = "%s%s/Jobs/%s" % (self.host_uri, self.manager_resource, _job_id)

        for _ in range(self.retries):
            _response = await self.get_request(_uri, _continue=True)
            if not _response:
                continue

            status_code = _response.status
            if status_code == 200:
                logger.info(f"Command passed to check job status {_job_id}")
                await asyncio.sleep(10)
            else:
                logger.error(f"Command failed to check job status {_job_id}, return code is %s." % status_code)

                await self.error_handler(_response)

            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            if data["Message"] == "Task successfully scheduled.":
                logger.info("Job id %s successfully scheduled." % _job_id)
                return
            else:
                logger.warning("JobStatus not scheduled, current status is: %s." % data["Message"])

        logger.error("Not able to successfully schedule the job.")
        raise BadfishException

    async def get_reset_types(self):
        logger.debug("Getting allowable reset types.")
        _url = "%s%s" % (self.host_uri, self.manager_resource)
        _response = await self.get_request(_url)
        reset_types = []
        if _response:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            if "Actions" not in data:
                logger.warning("Actions resource not found")
            else:
                manager_reset = data["Actions"].get("#Manager.Reset")
                if manager_reset:
                    reset_types = manager_reset.get("ResetType@Redfish.AllowableValues", [])
                    if not reset_types:
                        logger.warning("Could not get allowable reset types")
        return reset_types

    @staticmethod
    async def read_yaml(_yaml_file):
        with open(_yaml_file, "r") as f:
            try:
                definitions = yaml.safe_load(f)
            except yaml.YAMLError as ex:
                logger.error("Couldn't read file: %s" % _yaml_file)
                logger.debug(ex)
                raise BadfishException
        return definitions

    async def get_host_types_from_yaml(self, _interfaces_path):
        definitions = await self.read_yaml(_interfaces_path)
        host_types = set()
        for line in definitions:
            _split = line.split("_")
            host_types.add(_split[0])

        ordered_types = sorted(list(host_types))
        return ordered_types

    async def get_host_type(self, _interfaces_path):
        await self.get_boot_devices()

        if _interfaces_path and self.boot_devices:
            host_types = await self.get_host_types_from_yaml(_interfaces_path)
            for host_type in host_types:
                match = True
                interfaces = await self.get_interfaces_by_type(host_type, _interfaces_path)
                for device in sorted(self.boot_devices[: len(interfaces)], key=lambda x: x["Index"]):
                    if device["Name"] == interfaces[device["Index"]]:
                        continue
                    else:
                        match = False
                        break
                if match:
                    return host_type

        return None

    async def validate_credentials(self):
        response = await self.get_request(self.root_uri + "/Systems")

        if response.status == 401:
            logger.error(f"Failed to authenticate. Verify your credentials for {self.host}")
            raise BadfishException

        if response.status not in [200, 201]:
            logger.error(f"Failed to communicate with {self.host}")
            raise BadfishException

    async def get_interfaces_endpoints(self):
        _uri = "%s%s/EthernetInterfaces" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_uri)

        raw = await _response.text("utf-8", "ignore")
        data = json.loads(raw.strip())

        if _response.status == 404:
            logger.debug(raw)
            logger.error("EthernetInterfaces entry point not supported by this host.")
            raise BadfishException

        endpoints = []
        if data.get("Members"):
            for member in data["Members"]:
                endpoints.append(member["@odata.id"])
        else:
            logger.error("EthernetInterfaces's Members array is either empty or missing")
            raise BadfishException

        return endpoints

    async def get_interface(self, endpoint):
        _uri = "%s%s" % (self.host_uri, endpoint)
        _response = await self.get_request(_uri)

        raw = await _response.text("utf-8", "ignore")

        if _response.status == 404:
            logger.debug(raw)
            logger.error("EthernetInterface entry point not supported by this host.")
            raise BadfishException

        data = json.loads(raw.strip())

        return data

    async def find_systems_resource(self):
        response = await self.get_request(self.root_uri)

        if response:
            raw = await response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            if "Systems" not in data:
                logger.error("Systems resource not found")
                raise BadfishException
            else:
                systems = data["Systems"]["@odata.id"]
                _response = await self.get_request(self.host_uri + systems)
                if _response:
                    raw = await _response.text("utf-8", "ignore")
                    data = json.loads(raw.strip())
                    if data.get("Members"):
                        for member in data["Members"]:
                            systems_service = member["@odata.id"]
                            logger.info("Systems service: %s." % systems_service)
                            return systems_service
                    else:
                        try:
                            msg = data.get("error").get("@Message.ExtendedInfo")[0].get("Message")
                            resolution = data.get("error").get("@Message.ExtendedInfo")[0].get("Resolution")
                            logger.error(msg)
                            logger.info(resolution)
                        except (IndexError, TypeError, AttributeError):
                            pass
                        else:
                            logger.error("ComputerSystem's Members array is either empty or missing")
                        raise BadfishException

    async def find_managers_resource(self):
        response = await self.get_request(self.root_uri)
        if response:
            raw = await response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            if "Managers" not in data:
                logger.error("Managers resource not found")
                raise BadfishException
            else:
                managers = data["Managers"]["@odata.id"]
                response = await self.get_request(self.host_uri + managers)
                if response:
                    raw = await response.text("utf-8", "ignore")
                    data = json.loads(raw.strip())
                    if data.get("Members"):
                        for member in data["Members"]:
                            managers_service = member["@odata.id"]
                            logger.info("Managers service: %s." % managers_service)
                            return managers_service
                    else:
                        logger.error("Manager's Members array is either empty or missing")
                        raise BadfishException

    async def get_power_state(self):
        _uri = "%s%s" % (self.host_uri, self.system_resource)
        logger.debug("url: %s" % _uri)

        _response = await self.get_request(_uri, _continue=True)
        if not _response:
            return "Down"

        if _response.status == 200:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        else:
            logger.debug("Couldn't get power state. Retrying.")
            return "Down"

        if not data.get("PowerState"):
            raise BadfishException("Power state not found. Try to racreset.")
        else:
            logger.debug("Current server power state is: %s." % data["PowerState"])

        return data["PowerState"]

    async def set_power_state(self, state):
        if state.lower() not in ["on", "off"]:
            raise BadfishException("Power state not valid. 'on' or 'off' only accepted.")

        _uri = "%s%s" % (self.host_uri, self.system_resource)
        logger.debug("url: %s" % _uri)

        _response = await self.get_request(_uri, _continue=True)
        if not _response and state.lower() == "off":
            logger.warning("Power state appears to be already set to 'off'.")
            return

        if _response.status == 200:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        else:
            raise BadfishException("Couldn't get power state.")

        if not data.get("PowerState"):
            raise BadfishException("Couldn't get power state.")
        else:
            logger.debug("Current server power state is: %s." % data["PowerState"])

        if state.lower() == "off":
            await self.send_reset("ForceOff")
        elif state.lower() == "on":
            await self.send_reset("On")

        return data["PowerState"]

    async def change_boot(self, host_type, interfaces_path, pxe=False):
        if interfaces_path:
            host_types = await self.get_host_types_from_yaml(interfaces_path)
            if host_type.lower() not in host_types:
                logger.error(f"Expected values for -t argument are: {host_types}")
                raise BadfishException
            if not os.path.exists(interfaces_path):
                logger.error("No such file or directory: %s." % interfaces_path)
                raise BadfishException
        else:
            logger.error("You must provide a path to the interfaces yaml via `-i` optional argument.")
            raise BadfishException

        _type = await self.get_host_type(interfaces_path)
        if (_type and _type.lower() != host_type.lower()) or not _type:
            await self.clear_job_queue()
            await self.change_boot_order(host_type, interfaces_path)

            if pxe:
                await self.set_next_boot_pxe()

            job_id = await self.create_bios_config_job(self.bios_uri)
            if job_id:
                await self.get_job_status(job_id)

            await self.reboot_server()

        else:
            logger.warning("No changes were made since the boot order already matches the requested.")
        return True

    async def change_boot_order(self, _host_type, _interfaces_path):
        interfaces = await self.get_interfaces_by_type(_host_type, _interfaces_path)

        await self.get_boot_devices()
        devices = [device["Name"] for device in self.boot_devices]
        valid_devices = [device for device in interfaces if device in devices]
        if len(valid_devices) < len(interfaces):
            diff = [device for device in interfaces if device not in valid_devices]
            logger.warning("Some interfaces are not valid boot devices. Ignoring: %s" % ", ".join(diff))
        change = False
        for i, interface in enumerate(valid_devices):
            for device in self.boot_devices:
                if interface == device["Name"]:
                    if device["Index"] != i:
                        device["Index"] = i
                        change = True
                    break

        if change:
            await self.patch_boot_seq()

        else:
            logger.warning("No changes were made since the boot order already matches the requested.")

    async def patch_boot_seq(self):
        _boot_seq = await self.get_boot_seq()
        boot_sources_uri = "%s/BootSources/Settings" % self.system_resource
        url = "%s%s" % (self.host_uri, boot_sources_uri)
        payload = {"Attributes": {_boot_seq: self.boot_devices}}
        headers = {"content-type": "application/json"}
        response = None
        _status_code = 400

        for _ in range(self.retries):
            if _status_code != 200:
                response = await self.patch_request(url, payload, headers, True)
                if response:
                    raw = await response.text("utf-8", "ignore")
                    logger.debug(raw)
                    _status_code = response.status
            else:
                break

        if _status_code == 200:
            logger.info("PATCH command passed to update boot order.")
        else:
            logger.error("There was something wrong with your request.")

            if response:
                await self.error_handler(response)

    async def set_next_boot_pxe(self):
        _url = "%s%s" % (self.host_uri, self.system_resource)
        _payload = {
            "Boot": {
                "BootSourceOverrideTarget": "Pxe",
                "BootSourceOverrideEnabled": "Once",
            }
        }
        _headers = {"content-type": "application/json"}
        _response = await self.patch_request(_url, _payload, _headers)

        await asyncio.sleep(5)

        if _response.status == 200:
            logger.info('PATCH command passed to set next boot onetime boot device to: "%s".' % "Pxe")
        else:
            logger.error("Command failed, error code is %s." % _response.status)

            await self.error_handler(_response)

    async def check_supported_idrac_version(self):
        _url = "%s/Dell/Managers/iDRAC.Embedded.1/DellJobService/" % self.root_uri
        _response = await self.get_request(_url)
        if _response.status != 200:
            logger.warning("iDRAC version installed does not support DellJobService")
            return False

        return True

    async def check_supported_network_interfaces(self, endpoint):
        _url = "%s%s/%s" % (self.host_uri, self.system_resource, endpoint)
        _response = await self.get_request(_url)
        if _response.status != 200:
            return False

        return True

    async def delete_job_queue_dell(self):
        _url = "%s/Dell/Managers/iDRAC.Embedded.1/DellJobService/Actions/DellJobService.DeleteJobQueue" % self.root_uri
        _payload = {"JobID": "JID_CLEARALL"}
        _headers = {"content-type": "application/json"}
        response = await self.post_request(_url, _payload, _headers)
        if response.status == 200:
            logger.info("Job queue for iDRAC %s successfully cleared." % self.host)
        else:
            raw = await response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            if data.get("error"):
                if data["error"].get("@Message.ExtendedInfo"):
                    logger.debug(data["error"].get("@Message.ExtendedInfo"))
            logger.error("Job queue not cleared, there was something wrong with your request.")
            raise BadfishException

    async def delete_job_queue_force(self):
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _headers = {"content-type": "application/json"}
        url = "%s/JID_CLEARALL_FORCE" % _url
        try:
            _response = await self.delete_request(url, _headers)
        except BadfishException:
            logger.warning("There was something wrong clearing the job queue.")
            raise
        return _response

    async def clear_job_list(self, _job_queue):
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _headers = {"content-type": "application/json"}
        logger.warning("Clearing job queue for job IDs: %s." % _job_queue)
        failed = False
        for _job in _job_queue:
            job = _job.strip("'")
            url = "%s/%s" % (_url, job)
            response = await self.delete_request(url, _headers)
            if response.status != 200:
                failed = True

        if not failed:
            logger.info("Job queue for iDRAC %s successfully cleared." % self.host)
        else:
            logger.error("Job queue not cleared, there was something wrong with your request.")
            raise BadfishException

    async def clear_job_queue(self):
        _job_queue = await self.get_job_queue()
        if _job_queue:
            supported = await self.check_supported_idrac_version()
            if supported:
                await self.delete_job_queue_dell()
            else:
                try:
                    _response = await self.delete_job_queue_force()
                    if _response.status == 400:
                        await self.clear_job_list(_job_queue)
                except BadfishException:
                    logger.info("Attempting to clear job list instead.")
                    await self.clear_job_list(_job_queue)
        else:
            logger.warning("Job queue already cleared for iDRAC %s, DELETE command will not execute." % self.host)

    async def list_job_queue(self):
        _job_queue = await self.get_job_queue()
        if _job_queue:
            logger.info("Found active jobs:")
            for job in _job_queue:
                logger.info(job)
        else:
            logger.info("No active jobs found.")

    async def create_job(self, _url, _payload, _headers, expected=None):
        if not expected:
            expected = [200, 204]
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status

        if status_code in expected:
            logger.info("POST command passed to create target config job.")
        else:
            logger.error("POST command failed to create BIOS config job, status code is %s." % status_code)

            await self.error_handler(_response)

    async def create_bios_config_job(self, uri):
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _payload = {"TargetSettingsURI": "%s%s" % (self.redfish_uri, uri)}
        _headers = {"content-type": "application/json"}
        await self.create_job(_url, _payload, _headers)

    async def send_reset(self, reset_type):
        _url = "%s%s/Actions/ComputerSystem.Reset" % (
            self.host_uri,
            self.system_resource,
        )
        _payload = {"ResetType": reset_type}
        _headers = {"content-type": "application/json"}
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status
        if status_code in [200, 204]:
            logger.info("Command passed to %s server, code return is %s." % (reset_type, status_code))
            await asyncio.sleep(10)
        elif status_code in [409, 400]:
            logger.warning("Command failed to %s server, host appears to be already in that state." % reset_type)
        else:
            logger.error("Command failed to %s server, status code is: %s." % (reset_type, status_code))

            await self.error_handler(_response)

    async def reboot_server(self, graceful=False):
        logger.debug("Rebooting server: %s." % self.host)
        power_state = await self.get_power_state()
        if power_state.lower() == "on":
            if graceful:
                await self.send_reset("GracefulRestart")

                host_down = await self.polling_host_state("Off")

                if not host_down:
                    logger.warning("Unable to graceful shutdown the server, will perform forced shutdown now.")
                    await self.send_reset("ForceOff")
            else:
                await self.send_reset("ForceOff")

            host_not_down = await self.polling_host_state("Down", False)

            if host_not_down:
                await self.send_reset("On")

        elif power_state.lower() == "off":
            await self.send_reset("On")
        return True

    async def reset_idrac(self):
        logger.debug("Running reset iDRAC.")
        _reset_types = await self.get_reset_types()
        reset_type = "ForceRestart"
        if reset_type not in _reset_types:
            for rt in _reset_types:
                if "restart" in rt.lower():
                    reset_type = rt
        _url = "%s%s/Actions/Manager.Reset/" % (self.host_uri, self.manager_resource)
        _payload = {"ResetType": reset_type}
        _headers = {"content-type": "application/json"}
        logger.debug("url: %s" % _url)
        logger.debug("payload: %s" % _payload)
        logger.debug("headers: %s" % _headers)
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status
        if status_code == 204:
            logger.info("Status code %s returned for POST command to reset iDRAC." % status_code)
        else:
            data = await _response.text("utf-8", "ignore")
            logger.error("Status code %s returned, error is: \n%s." % (status_code, data))
            raise BadfishException
        await asyncio.sleep(15)

        logger.info("iDRAC will now reset and be back online within a few minutes.")
        return True

    async def reset_bios(self):
        logger.debug("Running BIOS reset.")
        _url = "%s%s/Bios/Actions/Bios.ResetBios/" % (
            self.host_uri,
            self.system_resource,
        )
        _payload = {}
        _headers = {"content-type": "application/json"}
        logger.debug("url: %s" % _url)
        logger.debug("payload: %s" % _payload)
        logger.debug("headers: %s" % _headers)
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status
        if status_code in [200, 204]:
            logger.info("Status code %s returned for POST command to reset BIOS." % status_code)
        else:
            data = await _response.text("utf-8", "ignore")
            logger.error("Status code %s returned, error is: \n%s." % (status_code, data))
            raise BadfishException

        logger.info("BIOS will now reset and be back online within a few minutes.")
        return True

    async def boot_to(self, device, skip_job=False):
        device_check = await self.check_device(device)
        if device_check:
            await self.clear_job_queue()
            await self.send_one_time_boot(device)
            if not skip_job:
                await self.create_bios_config_job(self.bios_uri)
        else:
            raise BadfishException
        return True

    async def boot_to_type(self, host_type, _interfaces_path):
        if _interfaces_path:
            if not os.path.exists(_interfaces_path):
                logger.error("No such file or directory: %s." % _interfaces_path)
                raise BadfishException
        else:
            logger.error("You must provide a path to the interfaces yaml via `-i` optional argument.")
            raise BadfishException
        host_types = await self.get_host_types_from_yaml(_interfaces_path)
        if host_type.lower() not in host_types:
            logger.error(f"Expected values for -t argument are: {host_types}")
            raise BadfishException

        device = await self.get_host_type_boot_device(host_type, _interfaces_path)

        await self.boot_to(device)

    async def boot_to_mac(self, mac_address):
        interfaces_endpoints = await self.get_interfaces_endpoints()

        device = None
        for endpoint in interfaces_endpoints:
            interface = await self.get_interface(endpoint)
            if interface.get("MACAddress", "").upper() == mac_address.upper():
                device = interface.get("Id")
                break

        if device:
            await self.boot_to(device)
        else:
            logger.error("MAC Address does not match any of the existing")
            raise BadfishException

    async def send_one_time_boot(self, device):
        boot_seq = await self.get_boot_seq()
        _url = "%s%s" % (self.root_uri, self.bios_uri)
        _payload = {
            "Attributes": {
                "OneTimeBootMode": f"OneTime{boot_seq}",
                f"OneTime{boot_seq}Dev": device,
            }
        }
        _headers = {"content-type": "application/json"}
        _first_reset = False
        for i in range(self.retries):
            _response = await self.patch_request(_url, _payload, _headers)
            status_code = _response.status
            if status_code == 200:
                logger.info("Command passed to set BIOS attribute pending values.")
                break
            else:
                logger.error("Command failed, error code is: %s." % status_code)
                if status_code == 503 and i - 1 != self.retries:
                    logger.info("Retrying to send one time boot.")
                    continue
                elif status_code == 400:
                    await self.clear_job_queue()
                    if not _first_reset:
                        await self.reset_idrac()
                        _first_reset = True
                        await self.polling_host_state("On")
                    continue
                await self.error_handler(_response)

    async def check_boot(self, _interfaces_path):
        if _interfaces_path:

            _host_type = await self.get_host_type(_interfaces_path)

            if _host_type:
                logger.warning("Current boot order is set to: %s." % _host_type)
            else:
                await self.get_boot_devices()

                logger.warning("Current boot order does not match any of the given.")
                logger.info("Current boot order:")
                for device in sorted(self.boot_devices, key=lambda x: x["Index"]):
                    logger.info("%s: %s" % (int(device["Index"]) + 1, device["Name"]))

        else:

            await self.get_boot_devices()
            logger.info("Current boot order:")
            for device in sorted(self.boot_devices, key=lambda x: x["Index"]):
                logger.info("%s: %s" % (int(device["Index"]) + 1, device["Name"]))
        return True

    async def check_device(self, device):
        logger.debug("Checking device %s." % device)
        await self.get_boot_devices()
        logger.debug(self.boot_devices)
        if self.boot_devices:
            boot_devices = [_device["Name"].lower() for _device in self.boot_devices]
            if device.lower() in boot_devices:
                return True
            else:
                logger.error("Device %s does not match any of the existing for host %s" % (device, self.host))
                return False
        else:
            logger.error(f"No boot devices found for {self.host}")
            return False

    async def polling_host_state(self, state, equals=True):
        state_str = "Not %s" % state if not equals else state
        logger.info("Polling for host state: %s" % state_str)
        desired_state = False
        for count in range(self.retries):
            current_state = await self.get_power_state()
            if equals:
                desired_state = current_state.lower() == state.lower()
            else:
                desired_state = current_state.lower() != state.lower()
            await asyncio.sleep(5)
            if desired_state:
                self.progress_bar(self.retries, self.retries, current_state)
                break
            self.progress_bar(count, self.retries, current_state)

        return desired_state

    async def get_firmware_inventory(self):
        logger.debug("Getting firmware inventory for all devices supported by iDRAC.")

        _url = "%s/UpdateService/FirmwareInventory/" % self.root_uri
        _response = await self.get_request(_url)

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        except ValueError:
            logger.error("Not able to access Firmware inventory.")
            raise BadfishException
        installed_devices = []
        if "error" in data:
            logger.debug(data["error"])
            logger.error("Not able to access Firmware inventory.")
            raise BadfishException
        for device in data["Members"]:
            a = device["@odata.id"]
            a = a.replace("/redfish/v1/UpdateService/FirmwareInventory/", "")
            if "Installed" in a:
                installed_devices.append(a)

        for device in installed_devices:
            logger.debug("Getting device info for %s" % device)
            _uri = "%s/UpdateService/FirmwareInventory/%s" % (self.root_uri, device)

            _response = await self.get_request(_uri, _continue=True)
            if not _response:
                continue

            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
            for info in data.items():
                if "odata" not in info[0] and "Description" not in info[0]:
                    logger.info("%s: %s" % (info[0], info[1]))

            logger.info("*" * 48)

    async def get_host_type_boot_device(self, host_type, _interfaces_path):
        if _interfaces_path:
            interfaces = await self.get_interfaces_by_type(host_type, _interfaces_path)
        else:
            logger.error("You must provide a path to the interfaces yaml via `-i` optional argument.")
            raise BadfishException

        return interfaces[0]

    async def get_virtual_media_config_uri(self):
        _url = "%s%s" % (self.host_uri, self.manager_resource)
        _response = await self.get_request(_url)

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        except ValueError:
            logger.error("Not able to access Firmware inventory.")
            raise BadfishException

        vm_endpoint = data.get("VirtualMedia")
        if vm_endpoint:
            virtual_media = vm_endpoint.get("@odata.id")
            if virtual_media:
                vm_url = "%s%s" % (self.host_uri, virtual_media)
                vm_response = await self.get_request(vm_url)
                try:
                    raw = await vm_response.text("utf-8", "ignore")
                    vm_data = json.loads(raw.strip())

                    oem = vm_data.get("Oem")
                    if oem:
                        sm = oem.get("Supermicro")
                        if sm:
                            vmc = sm.get("VirtualMediaConfig")
                            if vmc:
                                return vmc.get("@odata.id")

                except ValueError:
                    logger.error("Not able to check for supported virtual media unmount")
                    raise BadfishException

        return None

    async def get_virtual_media(self):
        _url = "%s%s" % (self.host_uri, self.manager_resource)
        _response = await self.get_request(_url)

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())
        except ValueError:
            logger.error("Not able to access Firmware inventory.")
            raise BadfishException

        vm_endpoint = data.get("VirtualMedia")
        vms = []
        if vm_endpoint:
            virtual_media = vm_endpoint.get("@odata.id")
            if virtual_media:
                vm_url = "%s%s" % (self.host_uri, virtual_media)
                vm_response = await self.get_request(vm_url)
                try:
                    raw = await vm_response.text("utf-8", "ignore")
                    vm_data = json.loads(raw.strip())

                    if vm_data.get("Members"):
                        for member in vm_data["Members"]:
                            vms.append(member["@odata.id"])
                    else:
                        logger.warning("No active VirtualMedia found")
                        return vms

                except ValueError:
                    logger.error("Not able to access Firmware inventory.")
                    raise BadfishException
            else:
                logger.error("No VirtualMedia endpoint found")
                raise BadfishException
        else:
            logger.error("No VirtualMedia endpoint found")
            raise BadfishException

        return vms

    async def check_virtual_media(self):
        vms = await self.get_virtual_media()
        for vm in vms:
            disc_url = "%s%s" % (self.host_uri, vm)
            disc_response = await self.get_request(disc_url)
            try:
                raw = await disc_response.text("utf-8", "ignore")
                disc_data = json.loads(raw.strip())
                _id = disc_data.get("Id")
                name = disc_data.get("Name")
                image_name = disc_data.get("ImageName")
                inserted = disc_data.get("Inserted")
                logger.info(f"ID: {_id} - Name: {name} - ImageName: {image_name} - Inserted: {inserted}")
            except ValueError:
                logger.error("There was something wrong getting values for VirtualMedia")
                raise BadfishException

        return True

    async def unmount_virtual_media(self):

        vmc = await self.get_virtual_media_config_uri()
        if not vmc:
            logger.warning("OOB management does not support Virtual Media unmount")
            return False

        _vmc_url = "%s%s/Actions/IsoConfig.UnMount" % (self.host_uri, vmc)
        _headers = {"content-type": "application/json"}
        _payload = {}
        try:
            disc_response = await self.post_request(_vmc_url, _payload, _headers)
            if disc_response.status == 200:
                logger.info("Successfully unmounted all VirtualMedia")
            else:
                logger.error("There was something wrong unmounting the VirtualMedia")
                raise BadfishException
        except ValueError:
            logger.error("There was something wrong getting values for VirtualMedia")
            raise BadfishException

        return True

    async def get_network_adapters(self):
        _url = "%s%s/NetworkAdapters" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_url)
        try:
            raw = await _response.text("utf-8", "ignore")
            na_data = json.loads(raw.strip())

            root_nics = []
            if na_data.get("Members"):
                for member in na_data["Members"]:
                    root_nics.append(member["@odata.id"])

            data = {}
            for nic in root_nics:
                net_ports_url = "%s%s/NetworkPorts" % (self.host_uri, nic)
                rn_response = await self.get_request(net_ports_url)
                rn_raw = await rn_response.text("utf-8", "ignore")
                rn_data = json.loads(rn_raw.strip())

                nic_ports = []
                if rn_data.get("Members"):
                    for member in rn_data["Members"]:
                        nic_ports.append(member["@odata.id"])

                net_df_url = "%s%s/NetworkDeviceFunctions" % (self.host_uri, nic)
                ndf_response = await self.get_request(net_df_url)
                ndf_raw = await ndf_response.text("utf-8", "ignore")
                ndf_data = json.loads(ndf_raw.strip())

                ndf_members = []
                if ndf_data.get("Members"):
                    for member in ndf_data["Members"]:
                        ndf_members.append(member["@odata.id"])

                for i, nic_port in enumerate(nic_ports):
                    np_url = "%s%s" % (self.host_uri, nic_port)
                    np_response = await self.get_request(np_url)
                    np_raw = await np_response.text("utf-8", "ignore")
                    np_data = json.loads(np_raw.strip())

                    interface = nic_port.split("/")[-1]

                    fields = [
                        "Id",
                        "LinkStatus",
                        "SupportedLinkCapabilities",
                    ]
                    values = {}
                    for field in fields:
                        value = np_data.get(field)
                        if value:
                            values[field] = value

                    ndf_url = "%s%s" % (self.host_uri, ndf_members[i])
                    ndf_response = await self.get_request(ndf_url)
                    ndf_raw = await ndf_response.text("utf-8", "ignore")
                    ndf_data = json.loads(ndf_raw.strip())
                    oem = ndf_data.get("Oem")
                    ethernet = ndf_data.get("Ethernet")
                    if ethernet:
                        mac_address = ethernet.get("MACAddress")
                        if mac_address:
                            values["MACAddress"] = mac_address
                    if oem:
                        dell = oem.get("Dell")
                        if dell:
                            dell_nic = dell.get("DellNIC")
                            vendor = dell_nic.get("VendorName")
                            if dell_nic.get("VendorName"):
                                values["Vendor"] = vendor

                    data.update({interface: values})

        except (ValueError, AttributeError):
            logger.error("There was something wrong getting network interfaces")
            raise BadfishException

        return data

    async def get_ethernet_interfaces(self):
        _url = "%s%s/EthernetInterfaces" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_url)

        if _response.status == 404:
            logger.error("Server does not support this functionality")
            raise BadfishException

        try:
            raw = await _response.text("utf-8", "ignore")
            ei_data = json.loads(raw.strip())

            interfaces = []
            if ei_data.get("Members"):
                for member in ei_data["Members"]:
                    interfaces.append(member["@odata.id"])

            data = {}
            for interface in interfaces:
                interface_url = "%s%s" % (self.host_uri, interface)
                int_response = await self.get_request(interface_url)
                int_raw = await int_response.text("utf-8", "ignore")
                int_data = json.loads(int_raw.strip())

                int_name = int_data.get("Id")
                fields = [
                    "Name",
                    "MACAddress",
                    "Status",
                    "LinkStatus",
                    "SpeedMbps",
                ]

                values = {}
                for field in fields:
                    value = int_data.get(field)
                    if value:
                        values[field] = value

                data.update({int_name: values})

        except (ValueError, AttributeError):
            logger.error("There was something wrong getting network interfaces")
            raise BadfishException

        return data

    async def list_interfaces(self):
        na_supported = await self.check_supported_network_interfaces("NetworkAdapters")
        ei_supported = await self.check_supported_network_interfaces("EthernetInterfaces")
        if na_supported:
            logger.debug("Getting Network Adapters")
            data = await self.get_network_adapters()
        elif ei_supported:
            logger.debug("Getting Ethernet interfaces")
            data = await self.get_ethernet_interfaces()
        else:
            logger.error("Server does not support this functionality")
            return False

        for interface, properties in data.items():
            logger.info(f"{interface}:")
            for key, value in properties.items():
                if key == "SupportedLinkCapabilities":
                    speed_key = "LinkSpeedMbps"
                    speed = value[0].get(speed_key)
                    if speed:
                        logger.info(f"    {speed_key}: {speed}")
                elif key == "Status":
                    health_key = "Health"
                    health = value.get(health_key)
                    if health:
                        logger.info(f"    {health_key}: {health}")
                else:
                    logger.info(f"    {key}: {value}")

        return True

    async def get_processor_summary(self):
        _url = "%s%s" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_url)

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())

            proc_data = data.get("ProcessorSummary")

            if not proc_data:
                logger.error("Server does not support this functionality")
                raise BadfishException

            fields = [
                "Count",
                "LogicalProcessorCount",
                "Model",
            ]

            values = {}
            for field in fields:
                value = proc_data.get(field)
                if value:
                    values[field] = value

        except (ValueError, AttributeError):
            logger.error("There was something wrong getting network interfaces")
            raise BadfishException

        return values

    async def get_processor_details(self):

        _url = "%s%s/Processors" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_url)

        if _response.status == 404:
            logger.error("Server does not support this functionality")
            raise BadfishException

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())

            processors = []
            if data.get("Members"):
                for member in data["Members"]:
                    processors.append(member["@odata.id"])

            proc_details = {}
            for processor in processors:
                processor_url = "%s%s" % (self.host_uri, processor)
                proc_response = await self.get_request(processor_url)
                proc_raw = await proc_response.text("utf-8", "ignore")
                proc_data = json.loads(proc_raw.strip())

                proc_name = proc_data.get("Id")
                fields = [
                    "Name",
                    "InstructionSet",
                    "Manufacturer",
                    "MemoryDeviceType",
                    "MaxSpeedMHz",
                    "Model",
                    "TotalCores",
                    "TotalThreads",
                ]

                values = {}
                for field in fields:
                    value = proc_data.get(field)
                    if value:
                        values[field] = value

                proc_details.update({proc_name: values})

        except (ValueError, AttributeError):
            logger.error("There was something wrong getting network interfaces")
            raise BadfishException

        return proc_details

    async def get_memory_summary(self):
        _url = "%s%s" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_url)

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())

            proc_data = data.get("MemorySummary")

            if not proc_data:
                logger.error("Server does not support this functionality")
                raise BadfishException

            fields = [
                "MemoryMirroring",
                "TotalSystemMemoryGiB",
            ]

            values = {}
            for field in fields:
                value = proc_data.get(field)
                if value:
                    values[field] = value

        except (ValueError, AttributeError):
            logger.error("There was something wrong getting network interfaces")
            raise BadfishException

        return values

    async def get_memory_details(self):

        _url = "%s%s/Memory" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_url)

        if _response.status == 404:
            logger.error("Server does not support this functionality")
            raise BadfishException

        try:
            raw = await _response.text("utf-8", "ignore")
            data = json.loads(raw.strip())

            memories = []
            if data.get("Members"):
                for member in data["Members"]:
                    memories.append(member["@odata.id"])

            mem_details = {}
            for memory in memories:
                memory_url = "%s%s" % (self.host_uri, memory)
                mem_response = await self.get_request(memory_url)
                mem_raw = await mem_response.text("utf-8", "ignore")
                mem_data = json.loads(mem_raw.strip())

                mem_name = mem_data.get("Name")
                fields = [
                    "CapacityMiB",
                    "Description",
                    "Manufacturer",
                    "MemoryDeviceType",
                    "OperatingSpeedMhz",
                ]

                values = {}
                for field in fields:
                    value = mem_data.get(field)
                    if value:
                        values[field] = value

                mem_details.update({mem_name: values})

        except (ValueError, AttributeError):
            logger.error("There was something wrong getting network interfaces")
            raise BadfishException

        return mem_details

    async def list_processors(self):
        data = await self.get_processor_summary()

        logger.info("Processor Summary:")
        for _key, _value in data.items():
            logger.info(f"    {_key}: {_value}")

        processor_data = await self.get_processor_details()

        for _processor, _properties in processor_data.items():
            logger.info(f"{_processor}:")
            for _key, _value in _properties.items():
                logger.info(f"    {_key}: {_value}")

        return True

    async def list_memory(self):
        data = await self.get_memory_summary()

        logger.info("Memory Summary:")
        for _key, _value in data.items():
            logger.info(f"    {_key}: {_value}")

        memory_data = await self.get_memory_details()

        for _memory, _properties in memory_data.items():
            logger.info(f"{_memory}:")
            for _key, _value in _properties.items():
                logger.info(f"    {_key}: {_value}")

        return True
