#!/usr/bin/env python3
import asyncio

import aiohttp
from requests.exceptions import RequestException

import json
import logging
import os
import re
import requests
import sys
import time
import warnings
import yaml

warnings.filterwarnings("ignore")

RETRIES = 15

logger = logging.getLogger(__name__)


class Badfish:
    def __init__(self, _host, _username, _password, _retries=RETRIES, loop=None):
        self.host = _host
        self.username = _username
        self.password = _password
        self.retries = _retries
        self.host_uri = "https://%s" % _host
        self.redfish_uri = "/redfish/v1"
        self.root_uri = "%s%s" % (self.host_uri, self.redfish_uri)
        if not loop:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        connector = aiohttp.TCPConnector(loop=self.loop)
        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop)

        self.system_resource = await self.find_systems_resource()
        self.manager_resource = await self.find_managers_resource()
        self.bios_uri = "%s/Bios/Settings" % self.system_resource[len(self.redfish_uri):]

    @staticmethod
    def progress_bar(value, end_value, state, bar_length=20):
        percent = float(value) / end_value
        arrow = '-' * int(round(percent * bar_length) - 1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        if state.lower() == "on":
            state = "On  "
        sys.stdout.write(
            "\r  Polling: [{0}] {1}% - Host state: {2}\n".format(arrow + spaces, int(round(percent * 100)), state)
        )
        sys.stdout.flush()

    def error_handler(self, _response):
        try:
            data = _response.json()
        except ValueError:
            logger.error("Error reading response from host.")
            sys.exit(1)

        if "error" in data:
            detail_message = str(data["error"]["@Message.ExtendedInfo"][0]["Message"])
            logger.warning(detail_message)

        sys.exit(1)

    async def get_request(self, uri, _continue=False):
        try:
            async with self.session.get(uri, auth=(self.username, self.password), verify=False, timeout=60) as _response:
                await _response.json()
        except Exception:
            logger.exception("Failed to communicate with server.")
            if _continue:
                return
            else:
                sys.exit(1)
        return _response

    async def post_request(self, uri, payload, headers):
        try:
            async with self.session.post(
                uri,
                data=json.dumps(payload),
                headers=headers,
                verify=False,
                auth=(self.username, self.password)
            ) as _response:
                await _response.json()
        except Exception:
            logger.exception("Failed to communicate with server.")
            sys.exit(1)
        return _response

    async def patch_request(self, uri, payload, headers, _continue=False):
        try:
            async with self.session.patch(
                uri,
                data=json.dumps(payload),
                headers=headers,
                verify=False,
                auth=(self.username, self.password)
            ) as _response:
                await _response.json()
        except Exception:
            logger.exception("Failed to communicate with server.")
            if _continue:
                return
            else:
                sys.exit(1)
        return _response

    async def delete_request(self, uri, headers):
        try:
            async with self.session.delete(
                uri,
                headers=headers,
                verify=False,
                auth=(self.username, self.password)
            ) as _response:
                await _response.json()
        except Exception:
            logger.exception("Failed to communicate with server.")
            sys.exit(1)
        return

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
            data = _response.json()
        except ValueError:
            logger.error("Could not retrieve Bios Boot mode.")
            sys.exit(1)

        try:
            bios_boot_mode = data[u"Attributes"]["BootMode"]
            return bios_boot_mode
        except KeyError:
            logger.warning("Could not retrieve Bios Attributes. Assuming Bios.")
            return "Bios"

    async def get_boot_devices(self):
        _boot_seq = await self.get_boot_seq()
        _uri = "%s%s/BootSources" % (self.host_uri, self.system_resource)
        _response = await self.get_request(_uri)

        data = _response.json()
        if "Attributes" in data:
            return data[u"Attributes"][_boot_seq]
        else:
            logger.debug(data)
            logger.error("Boot order modification is not supported by this host.")
            sys.exit(1)

    async def get_job_queue(self):
        logger.debug("Getting job queue.")
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _response = await self.get_request(_url)

        data = _response.json()
        data = str(data)
        job_queue = re.findall("[JR]ID_.+?'", data)
        jobs = [job.strip("}").strip("\"").strip("'") for job in job_queue]
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
                logger.info("Command passed to check job status, code 200 returned.")
                time.sleep(10)
            else:
                logger.error("Command failed to check job status, return code is %s." % status_code)

                self.error_handler(_response)

            data = _response.json()
            if data[u"Message"] == "Task successfully scheduled.":
                logger.info("Job id %s successfully scheduled." % _job_id)
                return
            else:
                logger.warning("JobStatus not scheduled, current status is: %s." % data[u"Message"])

        logger.error("Not able to successfully schedule the job.")
        sys.exit(1)

    async def get_host_type(self, _interfaces_path):
        boot_devices = await self.get_boot_devices()

        if _interfaces_path:
            with open(_interfaces_path, "r") as f:
                try:
                    definitions = yaml.safe_load(f)
                except yaml.YAMLError as ex:
                    logger.error("Couldn't read file: %s" % _interfaces_path)
                    logger.debug(ex)
                    sys.exit(1)

            host_model = self.host.split(".")[0].split("-")[-1]
            interfaces = {}
            for _host in ["foreman", "director"]:
                match = True
                interfaces[_host] = definitions["%s_%s_interfaces" % (_host, host_model)].split(",")
                for device in sorted(boot_devices[: len(interfaces)], key=lambda x: x[u"Index"]):
                    if device[u"Name"] == interfaces[_host][device[u"Index"]]:
                        continue
                    else:
                        match = False
                        break
                if match:
                    return _host

        return None

    async def find_systems_resource(self):
        response = self.get_request(self.root_uri)

        if response.status == 401:
            logger.error("Failed to authenticate. Verify your credentials.")
            sys.exit(1)

        if response:
            data = response.json()
            if 'Systems' not in data:
                logger.error("Systems resource not found")
                sys.exit(1)
            else:
                systems = data["Systems"]["@odata.id"]
                _response = self.get_request(self.host_uri + systems)
                if _response:
                    data = _response.json()
                    if data.get(u'Members'):
                        for member in data[u'Members']:
                            systems_service = member[u'@odata.id']
                            logger.info("Systems service: %s." % systems_service)
                            return systems_service
                    else:
                        logger.error("ComputerSystem's Members array is either empty or missing")
                        sys.exit(1)

    async def find_managers_resource(self):
        response = await self.get_request(self.root_uri)
        if response:
            data = response.json()
            if 'Managers' not in data:
                logger.error("Managers resource not found")
                sys.exit(1)
            else:
                managers = data["Managers"]["@odata.id"]
                response = await self.get_request(self.host_uri + managers)
                if response:
                    data = response.json()
                    if data.get(u'Members'):
                        for member in data[u'Members']:
                            managers_service = member[u'@odata.id']
                            logger.info("Managers service: %s." % managers_service)
                            return managers_service
                    else:
                        logger.error("Manager's Members array is either empty or missing")
                        sys.exit(1)

    async def get_power_state(self):
        _uri = '%s%s' % (self.host_uri, self.system_resource)
        logger.debug("url: %s" % _uri)

        _response = await self.get_request(_uri, _continue=True)
        if not _response:
            return "Down"

        if _response.ok:
            data = _response.json()
        else:
            logger.debug("Couldn't get power state. Retrying.")
            return "Down"
        logger.debug("Current server power state is: %s." % data[u'PowerState'])

        return data[u'PowerState']

    async def change_boot(self, host_type, interfaces_path, pxe=False):
        if host_type.lower() not in ("foreman", "director"):
            logger.error('Expected values for -t argument are "foreman" or "director"')
            sys.exit(1)

        if interfaces_path:
            if not os.path.exists(interfaces_path):
                logger.error("No such file or directory: %s." % interfaces_path)
                sys.exit(1)
        else:
            logger.error(
                "You must provide a path to the interfaces yaml via `-i` optional argument."
            )
            sys.exit(1)

        _type = await self.get_host_type(interfaces_path)
        if _type and _type.lower() != host_type.lower():
            await self.clear_job_queue()
            logger.warning("Waiting for host to be up.")
            host_up = self.polling_host_state("On")
            if host_up:
                await self.change_boot_order(interfaces_path, host_type)

                if pxe:
                    await self.set_next_boot_pxe()

                job_id = await self.create_bios_config_job(self.bios_uri)
                if job_id:
                    await self.get_job_status(job_id)

                await self.reboot_server()

            else:
                logger.error("Couldn't communicate with host after %s attempts." % self.retries)
                sys.exit(1)
        else:
            logger.warning(
                "No changes were made since the boot order already matches the requested."
            )
        return True

    async def change_boot_order(self, _interfaces_path, _host_type):
        with open(_interfaces_path, "r") as f:
            try:
                definitions = yaml.safe_load(f)
            except yaml.YAMLError as ex:
                logger.error(ex)
                sys.exit(1)

        host_model = self.host.split(".")[0].split("-")[-1]
        interfaces = definitions["%s_%s_interfaces" % (_host_type, host_model)].split(",")

        boot_devices = await self.get_boot_devices()
        change = False
        for i in range(len(interfaces)):
            for device in boot_devices:
                if interfaces[i] == device[u"Name"]:
                    if device[u"Index"] != i:
                        device[u"Index"] = i
                        change = True
                    break

        if change:
            await self.patch_boot_seq(boot_devices)

        else:
            logger.warning("No changes were made since the boot order already matches the requested.")
            sys.exit()

    async def patch_boot_seq(self, boot_devices):
        _boot_seq = await self.get_boot_seq()
        boot_sources_uri = "%s/BootSources/Settings" % self.system_resource
        url = "%s%s" % (self.host_uri, boot_sources_uri)
        payload = {"Attributes": {_boot_seq: boot_devices}}
        headers = {"content-type": "application/json"}
        response = None
        _status_code = 400

        for _ in range(self.retries):
            if _status_code != 200:
                response = self.patch_request(url, payload, headers, True)
                if response:
                    _status_code = response.status
            else:
                break

        if _status_code == 200:
            logger.info("PATCH command passed to update boot order.")
        else:
            logger.error("There was something wrong with your request.")

            if response:
                self.error_handler(response)

    async def set_next_boot_pxe(self):
        _url = "%s%s" % (self.host_uri, self.system_resource)
        _payload = {"Boot": {"BootSourceOverrideTarget": "Pxe"}}
        _headers = {"content-type": "application/json"}
        _response = await self.patch_request(_url, _payload, _headers)

        time.sleep(5)

        if _response.status_code == 200:
            logger.info('PATCH command passed to set next boot onetime boot device to: "%s".' % "Pxe")
        else:
            logger.error("Command failed, error code is %s." % _response.status_code)

            self.error_handler(_response)

    async def check_supported_idrac_version(self):
        _url = "%s/Dell/Managers/iDRAC.Embedded.1/DellJobService/" % self.root_uri
        _response = await self.get_request(_url)
        if _response.status_code != 200:
            logger.warning("iDRAC version installed does not support DellJobService")
            return False

        return True

    async def delete_job_queue(self):
        _url = "%s/Dell/Managers/iDRAC.Embedded.1/DellJobService/Actions/DellJobService.DeleteJobQueue" % self.root_uri
        _payload = {"JobID": "JID_CLEARALL"}
        _headers = {'content-type': 'application/json'}
        response = await self.post_request(_url, _payload, _headers)
        if response.status == 200:
            logger.info("Job queue for iDRAC %s successfully cleared." % self.host)
        else:
            logger.error("Job queue not cleared, there was something wrong with your request.")
            sys.exit(1)

    async def clear_job_list(self, _job_queue):
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _headers = {"content-type": "application/json"}
        logger.warning("Clearing job queue for job IDs: %s." % _job_queue)
        for _job in _job_queue:
            job = _job.strip("'")
            url = "%s/%s" % (_url, job)
            await self.delete_request(url, _headers)

        job_queue = await self.get_job_queue()
        if not job_queue:
            logger.info("Job queue for iDRAC %s successfully cleared." % self.host)
        else:
            logger.error("Job queue not cleared, current job queue contains jobs: %s." % job_queue)
            sys.exit(1)

    async def clear_job_queue(self):
        _job_queue = await self.get_job_queue()
        if _job_queue:
            supported = await self.check_supported_idrac_version()
            if supported:
                await self.delete_job_queue()
            else:
                await self.clear_job_list(_job_queue)
        else:
            logger.warning(
                "Job queue already cleared for iDRAC %s, DELETE command will not execute." % self.host
            )

    async def create_job(self, _url, _payload, _headers, expected=200):
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status

        if status_code == expected:
            logger.info("POST command passed to create target config job.")
        else:
            logger.error("POST command failed to create BIOS config job, status code is %s." % status_code)

            self.error_handler(_response)

        convert_to_string = str(_response.__dict__)
        job_id_search = re.search("[RJ]ID_.+?,", convert_to_string).group()
        _job_id = re.sub("[,']", "", job_id_search).strip("}").strip("\"").strip("'")
        logger.info("%s job ID successfully created." % _job_id)
        return _job_id

    async def create_bios_config_job(self, uri):
        _url = "%s%s/Jobs" % (self.host_uri, self.manager_resource)
        _payload = {"TargetSettingsURI": "%s%s" % (self.redfish_uri, uri)}
        _headers = {"content-type": "application/json"}
        _job = await self.create_job(_url, _payload, _headers)
        return _job

    async def send_reset(self, reset_type):
        _url = "%s%s/Actions/ComputerSystem.Reset" % (self.host_uri, self.system_resource)
        _payload = {"ResetType": reset_type}
        _headers = {"content-type": "application/json"}
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status
        if status_code in [200, 204]:
            logger.info(
                "Command passed to %s server, code return is %s." % (reset_type, status_code)
            )
            time.sleep(10)
        elif status_code == 409:
            logger.warning(
                "Command failed to %s server, host appears to be already in that state." % reset_type
            )
        else:
            logger.error(
                "Command failed to %s server, status code is: %s." % (reset_type, status_code)
            )

            self.error_handler(_response)

    async def reboot_server(self, graceful=True):
        logger.debug("Rebooting server: %s." % self.host)
        power_state = await self.get_power_state()
        if power_state.lower() == "on":
            if graceful:
                await self.send_reset("GracefulRestart")

                host_down = self.polling_host_state("Off")

                if not host_down:
                    logger.warning(
                        "Unable to graceful shutdown the server, will perform forced shutdown now."
                    )
                    await self.send_reset("ForceOff")
            else:
                await self.send_reset("ForceOff")

            host_not_down = self.polling_host_state("Down", False)

            if host_not_down:
                await self.send_reset("On")

        elif power_state.lower() == "off":
            await self.send_reset("On")
        return True

    async def reset_idrac(self):
        logger.debug("Running reset iDRAC.")
        _url = "%s%s/Actions/Manager.Reset/" % (self.host_uri, self.manager_resource)
        _payload = {"ResetType": "GracefulRestart"}
        _headers = {'content-type': 'application/json'}
        logger.debug("url: %s" % _url)
        logger.debug("payload: %s" % _payload)
        logger.debug("headers: %s" % _headers)
        _response = await self.post_request(_url, _payload, _headers)

        status_code = _response.status
        if status_code == 204:
            logger.info("Status code %s returned for POST command to reset iDRAC." % status_code)
        else:
            data = _response.json()
            logger.error("Status code %s returned, error is: \n%s." % (status_code, data))
            sys.exit(1)
        time.sleep(15)

        logger.info("iDRAC will now reset and be back online within a few minutes.")
        return True

    async def boot_to(self, device):
        device_check = await self.check_device(device)
        if device_check:
            await self.clear_job_queue()
            await self.send_one_time_boot(device)
            job_id = await self.create_bios_config_job(self.bios_uri)
            if job_id:
                await self.get_job_status(job_id)
        else:
            sys.exit(1)
        return True

    async def boot_to_type(self, host_type, _interfaces_path):
        if host_type.lower() not in ("foreman", "director"):
            logger.error('Expected values for -t argument are "foreman" or "director"')
            sys.exit(1)

        if _interfaces_path:
            if not os.path.exists(_interfaces_path):
                logger.error("No such file or directory: %s." % _interfaces_path)
                sys.exit(1)

        device = self.get_host_type_boot_device(host_type, _interfaces_path)

        await self.boot_to(device)

    async def send_one_time_boot(self, device):
        _url = "%s%s" % (self.root_uri, self.bios_uri)
        _payload = {"Attributes": {"OneTimeBootMode": "OneTimeBootSeq", "OneTimeBootSeqDev": device}}
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
                        self.polling_host_state("On")
                    continue
                self.error_handler(_response)

    async def check_boot(self, _interfaces_path):
        if _interfaces_path:

            _host_type = await self.get_host_type(_interfaces_path)

            if _host_type:
                logger.warning("Current boot order is set to: %s." % _host_type)
            else:
                boot_devices = await self.get_boot_devices()

                logger.warning("Current boot order does not match any of the given.")
                logger.info("Current boot order:")
                for device in sorted(boot_devices, key=lambda x: x[u"Index"]):
                    logger.info("%s: %s" % (int(device[u"Index"]) + 1, device[u"Name"]))

        else:
            boot_devices = await self.get_boot_devices()
            logger.info("Current boot order:")
            for device in sorted(boot_devices, key=lambda x: x[u"Index"]):
                logger.info("%s: %s" % (int(device[u"Index"]) + 1, device[u"Name"]))
        return True

    async def check_device(self, device):
        logger.debug("Checking device %s." % device)
        devices = await self.get_boot_devices()
        logger.debug(devices)
        boot_devices = [_device["Name"].lower() for _device in devices]
        if device.lower() in boot_devices:
            return True
        else:
            logger.error("Device %s does not match any of the existing for host %s" % (device, self.host))
            return False

    def polling_host_state(self, state, equals=True):
        state_str = "Not %s" % state if not equals else state
        logger.info("Polling for host state: %s" % state_str)
        desired_state = False
        for count in range(self.retries):
            current_state = self.get_power_state()
            if equals:
                desired_state = current_state.lower() == state.lower()
            else:
                desired_state = current_state.lower() != state.lower()
            time.sleep(5)
            if desired_state:
                self.progress_bar(self.retries, self.retries, current_state)
                break
            self.progress_bar(count, self.retries, current_state)

        return desired_state

    async def get_firmware_inventory(self):
        logger.debug("Getting firmware inventory for all devices supported by iDRAC.")

        _url = '%s/UpdateService/FirmwareInventory/' % self.root_uri
        _response = await self.get_request(_url)

        try:
            data = _response.json()
        except ValueError:
            logger.error("Not able to access Firmware inventory.")
            sys.exit(1)
        installed_devices = []
        if "error" in data:
            logger.debug(data["error"])
            logger.error("Not able to access Firmware inventory.")
            sys.exit(1)
        for device in data[u'Members']:
            a = device[u'@odata.id']
            a = a.replace("/redfish/v1/UpdateService/FirmwareInventory/", "")
            if "Installed" in a:
                installed_devices.append(a)

        for device in installed_devices:
            logger.debug("Getting device info for %s" % device)
            _uri = '%s/UpdateService/FirmwareInventory/%s' % (self.root_uri, device)

            _response = await self.get_request(_uri, _continue=True)
            if not _response:
                continue

            data = _response.json()
            for info in data.items():
                if "odata" not in info[0] and "Description" not in info[0]:
                    logger.info("%s: %s" % (info[0], info[1]))

            logger.info("*" * 48)

    async def export_configuration(self):
        _url = '%s%s/Actions/' \
               'Oem/EID_674_Manager.ExportSystemConfiguration' % (self.host_uri, self.manager_resource)
        _payload = {"ExportFormat": "XML", "ShareParameters": {"Target": "ALL"},
                    "IncludeInExport": "IncludeReadOnly,IncludePasswordHashValues"}
        _headers = {'content-type': 'application/json'}
        job_id = await self.create_job(_url, _payload, _headers, 202)

        _uri = '%s/TaskService/Tasks/%s' % (self.root_uri, job_id)

        for _ in range(self.retries):

            _response = await self.get_request(_uri, _continue=True)
            if not _response:
                continue

            data = _response.__dict__
            if "<SystemConfiguration Model" in str(data):
                logger.info("Export job ID %s successfully completed." % job_id)

                filename = "%s_export.xml" % self.host

                with open(filename, "w") as _file:
                    _content = data["_content"]
                    _file.writelines(["%s\n" % line.decode("utf-8") for line in _content.split(b"\n")])

                logger.info("Exported attributes saved in file: %s" % filename)

                return
            else:
                pass

            status_code = _response.status
            data = _response.json()

            if status_code == 202 or status_code == 200:
                logger.info("JobStatus not completed, current status: \"%s\", percent complete: \"%s\"" % (
                    data[u'Oem'][u'Dell'][u'Message'], data[u'Oem'][u'Dell'][u'PercentComplete']))
                time.sleep(1)
            else:
                logger.error("Execute job ID command failed, error code is: %s" % status_code)
                sys.exit(1)

        logger.error("Could not export settings after %s attempts." % self.retries)

    def get_host_type_boot_device(self, host_type, _interfaces_path):
        if _interfaces_path:
            with open(_interfaces_path, "r") as f:
                try:
                    definitions = yaml.safe_load(f)
                except yaml.YAMLError as ex:
                    logger.error("Couldn't read file: %s" % _interfaces_path)
                    logger.debug(ex)
                    sys.exit(1)

            host_model = self.host.split(".")[0].split("-")[-1]
            return definitions["%s_%s_interfaces" % (host_type, host_model)].split(",")[0]
        return None
