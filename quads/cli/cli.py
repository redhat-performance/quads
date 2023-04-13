import asyncio
import functools
import json
import logging
import os
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Tuple, Optional
from urllib.parse import urlencode

import requests
import yaml
from jinja2 import Template
from requests import ConnectionError
from quads.config import Config as conf
from quads.exceptions import CliException, BaseQuadsException
from quads.helpers import first_day_month, last_day_month
from quads.quads_api import QuadsApi as Quads
from quads.server.models import Assignment
from quads.tools import reports
from quads.tools.external.jira import Jira, JiraException
from quads.tools.move_and_rebuild import move_and_rebuild, switch_config

default_move_command = "/opt/quads/quads/tools/move_and_rebuild_hosts.py"


class QuadsCli:
    ACTION_PREFIX = "action_"

    quads: Quads
    logger: logging.Logger
    cli_args: dict

    def __init__(self, quads: Quads, logger: logging.Logger):
        self.quads = quads
        self.logger = logger

    @staticmethod
    def _confirmation_dialog(msg, default_choice="n"):
        return (input(msg) or default_choice).lower() in ("y", "yes")

    def run(self, action: str, cli_args: dict) -> Optional[int]:
        self.cli_args = cli_args
        self.logger.debug(self.cli_args)

        if self.cli_args["datearg"]:
            assert "date" not in self.cli_args, "cli arg date already exists?"

            self.cli_args["date"] = datetime.strptime(
                self.cli_args["datearg"], "%Y-%m-%d %H:%M"
            ).isoformat()

        if action:
            # action method should always be available
            # unless not implemented on this class yet
            action_meth_name = self.ACTION_PREFIX + action
            action_meth = getattr(self, action_meth_name, None)
            self.logger.debug(f"Action: {action}; {action_meth}")

            assert action_meth is not None and callable(
                action_meth
            ), f"Missing callable action method '{action_meth_name}', not implemented yet?"

            return action_meth()

        # default action
        clouds = self.quads.get_clouds()
        hosts = self.quads.get_hosts()
        _date = datetime.now()
        if self.cli_args.get("datearg"):
            _date = datetime.strptime(self.cli_args["datearg"], "%Y-%m-%d %H:%M")
        for cloud in clouds:
            if cloud.name == "cloud01":
                available = []
                for host in hosts:
                    payload = {"start": _date, "end": _date}
                    if self.quads.is_available(host.name, payload):
                        available.append(host)
                if available:
                    self.logger.info(f"{cloud.name}:")
                    for host in available:
                        self.logger.info(f"  - {host.name}")
            else:
                payload = {"cloud": cloud, "date": _date}
                schedules = self.quads.get_current_schedules(payload)
                if schedules:
                    self.logger.info(f"{cloud.name}:")
                    for schedule in schedules:
                        self.logger.info(f"  - {schedule.host.name}")

        return 0

    def clear_field(self, host, key):
        dispatch_remove = {
            "disks": self.quads.remove_disk,
            "interfaces": self.quads.remove_interface,
            "memory": self.quads.remove_memory,
            "processors": self.quads.remove_processor,
        }
        field = host.get(key)
        if not field:
            raise CliException("{key} is not a Host property")

        for obj in field:
            remove_func = dispatch_remove.get(key)
            remove_func(obj.get("id"))

    def _filter_kwargs(self, filter_args):
        kwargs = {}
        ops = {
            "==": "",
            "!=": "__ne",
            "<": "__lt",
            "<=": "__lte",
            ">": "__gt",
            ">=": "__gte",
        }
        conditions = filter_args.split(",")
        for condition in conditions:
            op_found = False
            for op, op_suffix in ops.items():
                if op in condition:
                    op_found = True
                    k, v = condition.split(op)
                    keys = k.split(".")

                    try:
                        value = int(v)
                    except ValueError:
                        value = v

                    if type(value) == str:
                        if value.lower() == "false":
                            value = False
                        elif value.lower() == "true":
                            value = True

                    if keys[0].strip().lower() in [
                        "disks",
                        "interfaces",
                        "processors",
                        "memory",
                    ]:

                        key = f"{keys[0].strip()}__match"
                        condition_dict = {
                            f"{'__'.join(keys[1:])}{op_suffix}".strip(): value
                        }
                        if kwargs.get(key, False):
                            kwargs[key].update(condition_dict)
                        else:
                            kwargs[key] = condition_dict
                    else:
                        if keys[0].strip().lower() == "model":
                            if str(value).upper() not in conf["models"].split(","):
                                self.logger.warning(
                                    f"Accepted model names are: {conf['models']}"
                                )
                                raise CliException("Model type not recognized.")

                        if type(value) == str:
                            value = value.upper()
                        query = {f"{'__'.join(keys)}{op_suffix}": value}
                        kwargs.update(query)
                    break
            if not op_found:
                self.logger.warning(f"Condition: {condition}")
                self.logger.warning(f"Accepted operators: {', '.join(ops.keys())}")
                raise CliException(
                    "A filter was defined but not parsed correctly. Check filter operator."
                )
        if not kwargs:
            raise CliException(
                "A filter was defined but not parsed correctly. Check filter syntax."
            )
        return kwargs

    def _output_json_result(self, request, data):
        try:
            if request.status_code == 204:
                self.logger.info("Successfully removed")
            else:
                js = request.json()
                self.logger.debug(
                    "%s %s: %s" % (request.status_code, request.reason, data)
                )
                if request.request.method == 'POST' and request.status_code == 200:
                    self.logger.info('Successful request')
                if js.get("result"):
                    for result in js["result"]:
                        if type(result) == list:
                            for line in result:
                                self.logger.info(line)
                        else:
                            self.logger.info(result)
        except JSONDecodeError:
            self.logger.debug(request.text)
            raise CliException("Could not parse json reply")

    def action_version(self):
        response = self.quads.get_version()
        if response.status_code == 200:
            data = response.json()
        else:
            raise CliException("There was something wrong communicating with the quads server")
        self.logger.info(data.get("result"))

    def action_ls_broken(self):
        payload = {"broken": True}
        _hosts = self.quads.filter_hosts(payload)
        for host in _hosts:
            self.logger.info(host.name)

    def action_ls_retired(self):
        payload = {"retired": True}
        _hosts = self.quads.filter_hosts(payload)
        for host in _hosts:
            self.logger.info(host.name)

    def _call_api_action(self, action: str):
        assignments = self.quads.get_active_assignments()
        for ass in assignments:
            self.logger.info(f"{ass.cloud.name}: {getattr(ass, action)}")

    def action_owner(self):
        self._call_api_action("owner")

    def action_ticket(self):
        self._call_api_action("ticket")

    def action_qinq(self):
        self._call_api_action("qinq")

    def action_wipe(self):
        self._call_api_action("wipe")

    def action_ccuser(self):
        self._call_api_action("ccuser")

    def action_interface(self):
        hostname = self.cli_args["host"]
        if hostname is None:
            raise CliException(
                "Missing option. --host option is required for --ls-interface:"
            )

        host = self.quads.get_host(hostname)
        if not host:
            raise CliException(f"Host {hostname} does not exist")

        data = self.quads.get_host_interface(hostname)

        if data:
            for interface in sorted(data, key=lambda k: k.name):
                self.logger.info(f"interface: {interface.name}")
                self.logger.info(f"  bios id: {interface.bios_id}")
                self.logger.info(f"  mac address: {interface.mac_address}")
                self.logger.info(f"  switch ip: {interface.switch_ip}")
                self.logger.info(f"  port: {interface.switch_port}")
                self.logger.info(f"  speed: {interface.speed}")
                self.logger.info(f"  vendor: {interface.vendor}")
                self.logger.info(f"  pxe_boot: {interface.pxe_boot}")
                self.logger.info(f"  maintenance: {interface.maintenance}")
        else:
            self.logger.error(f"No interfaces defined for {hostname}")

    def action_memory(self):
        hostname = self.cli_args["host"]
        if hostname is None:
            raise CliException(
                "Missing option. --host option is required for --ls-memory:"
            )

        host = self.quads.get_host(hostname)
        if not host:
            raise CliException(f"Host {hostname} does not exist")

        for i, memory in enumerate(host.memory):
            self.logger.info(f"memory: {memory.handle}")
            self.logger.info(f"  size: {memory.size_gb}")

    def action_disks(self):
        hostname = self.cli_args["host"]
        if hostname is None:
            raise CliException(
                "Missing option. --host option is required for --ls-disks:"
            )

        host = self.quads.get_host(hostname)
        if not host:
            raise CliException(f"Host {hostname} does not exist")

        for i, disk in enumerate(host.disks):
            self.logger.info(f"disk{i}:")
            self.logger.info(f"  type: {disk.disk_type}")
            self.logger.info(f"  size: {disk.size_gb}")
            self.logger.info(f"  count: {disk.count}")

    def action_processors(self):
        hostname = self.cli_args["host"]
        if hostname is None:
            raise CliException(
                "Missing option. --host option is required for --ls-processors:"
            )

        host = self.quads.get_host(hostname)

        if not host:
            raise CliException(f"Host {hostname} does not exist")

        for i, processor in enumerate(host.processors):
            self.logger.info(f"processor: {processor.handle}")
            self.logger.info(f"  vendor: {processor.vendor}")
            self.logger.info(f"  product: {processor.product}")
            self.logger.info(f"  cores: {processor.cores}")
            self.logger.info(f"  threads: {processor.threads}")

    def action_ls_vlan(self):
        _vlans = self.quads.get_vlans()
        if not _vlans:
            raise CliException("No VLANs defined")
        for vlan in _vlans:
            payload = {"vlan_id": vlan.vlan_id, "active": True}
            assignment = self.quads.get_assignment(**payload)
            data = assignment.json()
            ass_obj = Assignment().from_dict(data[0])
            cloud_assigned = "Free"
            if assignment:
                cloud_assigned = ass_obj.cloud.name
            self.logger.info(f"{vlan.vlan_id}: {cloud_assigned}")

    def action_schedule(self):
        _kwargs = {}
        if self.cli_args["host"]:
            _host = self.quads.get_host(self.cli_args["host"])
            if not _host:
                raise CliException("Host %s does not exist" % self.cli_args["host"])

            _kwargs["host"] = _host.name
            self.logger.info("Default cloud: %s" % _host.default_cloud.name)
            _current_schedule = self.quads.get_current_schedules(**_kwargs)
            if _current_schedule:
                _current_cloud = _current_schedule[0].cloud.name
                if _current_cloud != _host.default_cloud.name:
                    self.logger.info("Current cloud: %s" % _current_cloud)
                    self.logger.info(
                        "Current schedule: %s" % _current_schedule[0].index
                    )
                else:
                    self.logger.info("Current cloud: %s" % _host.default_cloud.name)
            else:
                self.logger.info("Current cloud: %s" % _host.default_cloud.name)
            if "date" in _kwargs:
                _kwargs.pop("date")
            _host_schedules = self.quads.get_schedules(**_kwargs)
            if _host_schedules:
                for schedule in _host_schedules:
                    _cloud_name = schedule.assignment.cloud.name
                    start = str(schedule.start)[:-3]
                    end = str(schedule.end)[:-3]
                    self.logger.info(
                        f"{schedule.id}| start={start}, end={end}, cloud={_cloud_name}"
                    )
        else:
            _clouds = self.quads.get_clouds()
            for cloud in _clouds:
                self.logger.info("%s:" % cloud.name)
                _kwargs["cloud"] = cloud.name
                if cloud.name == "cloud01":
                    if _kwargs.get("date"):
                        data = {
                            "start": _kwargs["date"],
                            "end": _kwargs["date"],
                        }
                        try:
                            available_hosts = self.quads.filter_available(**data)
                        except ConnectionError:
                            raise CliException(
                                "Could not connect to the quads-server, verify service is up and running."
                            )

                        for host in available_hosts:
                            self.logger.info(host)
                else:
                    # TODO: check this one
                    payload = {"cloud": cloud}
                    _hosts = self.quads.filter_hosts(payload)
                    for host in _hosts:
                        self.logger.info(host.name)

    # TODO: Remove this if not used
    def action_cloud(self):
        try:
            entries = self.quads.get_clouds()
        except ConnectionError:
            raise CliException(
                "Could not connect to the quads-server, verify service is up and running."
            )

        if entries and "result" not in entries:
            for entry in sorted(entries, key=lambda k: k.name):
                self.logger.info(entry.name)
        elif "result" in entries:
            self.logger.info(entries["result"])

    def action_ls_hosts(self):
        kwargs = {"retired": False}
        if self.cli_args["filter"]:
            filter_args = self._filter_kwargs(self.cli_args["filter"])
            kwargs.update(filter_args)
            hosts = self.quads.filter_hosts(kwargs)
        else:
            hosts = self.quads.get_hosts()
        if hosts:
            for host in sorted(hosts, key=lambda k: k.name):
                self.logger.info(host.name)
        else:
            self.logger.warning("No hosts found.")

        return 0

    def action_ls_clouds(self):
        clouds = self.quads.get_clouds()
        if clouds:
            for cloud in sorted(clouds, key=lambda k: k.name):
                self.logger.info(cloud.name)
        else:
            self.logger.warning("No clouds found.")

        return 0

    def action_free_cloud(self):
        _clouds = self.quads.get_clouds()
        _clouds = [_c for _c in _clouds if _c.name != "cloud01"]
        for cloud in _clouds:
            _future_sched = self.quads.get_future_schedules({"cloud": cloud.name})
            if len(_future_sched):
                continue
            else:
                cloud_reservation_lock = int(conf["cloud_reservation_lock"])
                last_redefined = datetime.strptime(cloud.last_redefined, "%a, %d %b %Y %H:%M:%S GMT")
                lock_release = last_redefined + timedelta(
                    hours=cloud_reservation_lock
                )
                cloud_string = f"{cloud.name}"
                if lock_release > datetime.now():
                    time_left = lock_release - datetime.now()
                    hours = time_left.total_seconds() // 3600
                    minutes = (time_left.total_seconds() % 3600) // 60
                    cloud_string += " (reserved: %dhr %dmin remaining)" % (
                        hours,
                        minutes,
                    )
                self.logger.info(cloud_string)

    def action_available(self):

        kwargs = {}
        if self.cli_args["filter"]:
            filter_args = self._filter_kwargs(self.cli_args["filter"])
            kwargs.update(filter_args)

        if self.cli_args["schedstart"]:
            kwargs["start"] = datetime.strptime(
                self.cli_args["schedstart"], "%Y-%m-%d %H:%M"
            )

        if self.cli_args["schedend"]:
            kwargs["end"] = datetime.strptime(
                self.cli_args["schedend"], "%Y-%m-%d %H:%M"
            )

        available = []
        current = []
        all_hosts = self.quads.filter_hosts(kwargs)

        omit_cloud = ""
        if self.cli_args["omitcloud"]:
            omit_cloud = self.quads.get_cloud(self.cli_args["omitcloud"])
            if not omit_cloud:
                raise CliException("Omit cloud not found")

        for host in all_hosts:
            data = {"start": _start, "end": _end}
            # TODO: check return on this below
            if self.quads.is_available(host["name"], data):
                current_schedule = self.quads.get_current_schedules({"host": host})
                if current_schedule:
                    if (
                            host.default_cloud.name == conf["spare_pool_name"]
                            and current_schedule[0].cloud != omit_cloud
                    ):
                        current.append(host["name"])
                else:
                    if host.default_cloud.name == conf["spare_pool_name"]:
                        available.append(host["name"])

        for host in available:
            self.logger.info(host)
        for host in current:
            self.logger.warning(host)

    def action_report_scheduled(self):
        if self.cli_args["months"] is None and self.cli_args["year"] is None:
            raise CliException("Missing argument. --months or --year must be provided.")

        now = datetime.now()
        if self.cli_args["year"]:
            months = 12
            year = self.cli_args["year"]
        else:
            months = self.cli_args["months"]
            year = now.year

        reports.report_scheduled(self.logger, int(months), int(year))

    def _helper_report_start_end(self) -> Tuple[datetime, datetime]:
        now = datetime.now()
        if self.cli_args["schedstart"] and self.cli_args["schedend"] is None:
            self.cli_args["schedend"] = self.cli_args["schedstart"]

        if self.cli_args["schedstart"] is None and self.cli_args["schedend"]:
            self.cli_args["schedstart"] = str(now)[:-10]

        if self.cli_args["schedstart"] is None and self.cli_args["schedend"] is None:
            start = first_day_month(now)
            self.cli_args["schedstart"] = str(start)[:-10]
            end = last_day_month(now)
            self.cli_args["schedend"] = str(end)[:-10]

        _start = datetime.strptime(self.cli_args["schedstart"], "%Y-%m-%d %H:%M")
        _end = datetime.strptime(self.cli_args["schedend"], "%Y-%m-%d %H:%M")

        return _start, _end

    def action_report_available(self):
        start, end = self._helper_report_start_end()
        reports.report_available(self.logger, start, end)

    def action_report_detailed(self):
        start, end = self._helper_report_start_end()
        reports.report_detailed(self.logger, start, end)

    def action_extend(self):
        if not self.cli_args["weeks"] and not self.cli_args["datearg"]:
            raise CliException(
                "Missing option. Need --weeks or --date when using --extend"
            )

        if self.cli_args["cloud"] is None and self.cli_args["host"] is None:
            raise CliException(
                "Missing option. At least one of either --host or --cloud is required."
            )

        weeks = 0
        _date = None
        end_date = None

        if self.cli_args["weeks"]:
            try:
                weeks = int(self.cli_args["weeks"])
            except ValueError:
                raise CliException("The value of --weeks must be an integer")

        else:
            _date = datetime.strptime(self.cli_args["datearg"], "%Y-%m-%d %H:%M")

        if self.cli_args["cloud"]:
            cloud = self.quads.get_cloud(self.cli_args["cloud"])
            assignment = self.quads.get_active_cloud_assignment(cloud.name)
            if not cloud:
                raise CliException("Cloud not found")

            schedules = self.quads.get_current_schedules({"cloud": cloud.name})
            if not schedules:
                self.logger.warning(
                    "The selected cloud does not have any active schedules"
                )
                future_schedules = self.quads.get_future_schedules(
                    {"cloud": cloud.name}
                )
                if not future_schedules:
                    return

                if not self._confirmation_dialog(
                        f"Would you like to extend a future allocation of {cloud.name}? (y/N): "
                ):
                    return
                schedules = future_schedules

            non_extendable = []
            for schedule in schedules:
                if weeks:
                    end_date = schedule.end + timedelta(weeks=weeks)
                else:
                    end_date = _date
                is_host_available = self.quads.is_available(
                    schedule.host.name, {"start": schedule.end, "end": end_date}
                )
                if not is_host_available or end_date < schedule.end:
                    non_extendable.append(schedule.host)

            if non_extendable:
                self.logger.warning(
                    "The following hosts cannot be extended for the "
                    "allocation or target date is sooner than current end date:"
                )
                for host in non_extendable:
                    self.logger.info(host.name)
                return

            if not self.cli_args["check"]:
                # TODO: get notification obj
                data = {
                    "one_day": False,
                    "three_days": False,
                    "five_days": False,
                    "seven_days": False,
                }
                self.quads.update_assignment(assignment.id, data)

                for schedule in schedules:
                    if weeks:
                        end_date = schedule.end + timedelta(weeks=weeks)
                    else:
                        end_date = _date
                    self.quads.update_schedule(schedule.id, {"end": end_date})

                if weeks:
                    self.logger.info(
                        "Cloud %s has now been extended for %s week[s] until %s"
                        % (cloud.name, str(weeks), str(end_date)[:16])
                    )
                else:
                    self.logger.info(
                        "Cloud %s has now been extended until %s"
                        % (cloud.name, str(_date)[:16])
                    )
            else:
                self.logger.info(
                    "Cloud %s can be extended until %s"
                    % (cloud.name, str(end_date)[:16])
                )

        elif self.cli_args["host"]:
            host = self.quads.get_host(self.cli_args["host"])
            if not host:
                raise CliException("Host not found")

            schedule = self.quads.get_current_schedules({"host": host})
            if not schedule:
                self.logger.error(
                    "The selected host does not have any active schedules"
                )
                future_schedule = self.quads.get_future_schedules({"host": host})
                if not future_schedule:
                    return 1

                if not self._confirmation_dialog(
                        "Would you like to extend a future allocation of"
                        f" {host.name}? (y/N): "
                ):
                    return
                schedule = future_schedule

            if self.cli_args["weeks"]:
                end_date = schedule.end + timedelta(weeks=weeks)
            else:
                end_date = _date
            data = {"start": schedule.end, "end": end_date}
            is_host_available = self.quads.is_available(host.name, data)
            if not is_host_available or end_date < schedule.end:
                # TODO: Should this be warning/error?
                self.logger.info(
                    "The host cannot be extended for the current allocation as "
                    "it is not available during that time frame or end date would "
                    "result in a shrink action."
                )
                return 1

            if not self.cli_args["check"]:
                assignment = self.quads.get_active_cloud_assignment(schedule.cloud.name)
                data = {
                    "one_day": False,
                    "three_days": False,
                    "five_days": False,
                    "seven_days": False,
                }
                self.quads.update_assignment(assignment.id, data)

                self.quads.update_schedule(schedule.id, {"end": end_date})

                if self.cli_args["weeks"]:
                    self.logger.info(
                        "Host %s has now been extended for %s week[s] until %s"
                        % (host.name, str(weeks), str(end_date)[:16])
                    )
                else:
                    self.logger.info(
                        "Host %s has now been extended until %s"
                        % (host.name, str(end_date)[:16])
                    )

            else:
                self.logger.info(
                    "Host %s can be extended until %s" % (host.name, str(end_date)[:16])
                )

    def action_shrink(self):
        if (
                not self.cli_args["weeks"]
                and not self.cli_args["now"]
                and not self.cli_args["datearg"]
        ):
            raise CliException(
                "Missing option. Need --weeks, --date or --now when using --shrink"
            )

        if self.cli_args["cloud"] is None and self.cli_args["host"] is None:
            raise CliException(
                "Missing option. At least one of either --host or --cloud is required"
            )

        time_delta = timedelta()
        weeks = 0
        _date = None
        end_date = None

        if self.cli_args["weeks"]:
            try:
                weeks = int(self.cli_args["weeks"])
            except ValueError:
                raise CliException("The value of --weeks must be an integer")

            time_delta = timedelta(weeks=weeks)
        elif self.cli_args["datearg"]:
            _date = datetime.strptime(self.cli_args["datearg"], "%Y-%m-%d %H:%M")
        elif self.cli_args["now"]:
            _date = datetime.now()

        threshold = datetime.now() + timedelta(hours=1)

        if self.cli_args["cloud"]:
            cloud = self.quads.get_cloud(self.cli_args["cloud"])
            assignment = self.quads.get_active_cloud_assignment(cloud.name)
            if not cloud:
                raise CliException("Cloud not found")

            schedules = self.quads.get_current_schedules({"cloud": cloud.name})
            if not schedules:
                self.logger.error(
                    "The selected cloud does not have any active schedules"
                )
                future_schedules = self.quads.get_future_schedules(
                    {"cloud": cloud.name}
                )
                if not future_schedules:
                    return 1

                if not self._confirmation_dialog(
                        "Would you like to shrink a future allocation of"
                        f" {cloud.name}? (y/N): "
                ):
                    return
                schedules = future_schedules

            non_shrinkable = []

            for schedule in schedules:
                if self.cli_args["weeks"]:
                    end_date = schedule.end - time_delta
                else:
                    end_date = _date
                if (
                        end_date < schedule.start
                        or end_date > schedule.end
                        or (not self.cli_args["now"] and end_date < threshold)
                ):
                    non_shrinkable.append(schedule.host)

            if non_shrinkable:
                self.logger.info(
                    "The following hosts cannot be shrunk past it's start date, target date means an extension"
                    " or target date is earlier than 1 hour from now:"
                )
                for host in non_shrinkable:
                    self.logger.info(host.name)
                return 1

            if not self.cli_args["check"]:
                confirm_msg = (
                    f"for {self.cli_args['weeks']} week[s]? (y/N): "
                    if weeks
                    else f"to {str(_date)[:16]}? (y/N): "
                )
                if not self._confirmation_dialog(
                        f"Are you sure you want to shrink {cloud.name} " + confirm_msg
                ):
                    return

                for schedule in schedules.all():
                    if self.cli_args["weeks"]:
                        end_date = schedule.end - time_delta
                    else:
                        end_date = _date
                    schedule.update(end=end_date)
                if weeks:
                    self.logger.info(
                        "Cloud %s has now been shrunk for %s week[s] until %s"
                        % (cloud.name, str(weeks), str(end_date)[:16])
                    )
                elif self.cli_args["datearg"]:
                    self.logger.info(
                        "Cloud %s has now been shrunk to %s"
                        % (cloud.name, str(end_date)[:16])
                    )
                else:
                    self.logger.info("Cloud %s has now been terminated" % cloud.name)

            else:
                if weeks:
                    self.logger.info(
                        "Cloud %s can be shrunk for %s week[s] to %s"
                        % (cloud.name, str(weeks), str(end_date)[:16])
                    )
                elif self.cli_args["datearg"]:
                    self.logger.info(
                        "Cloud %s can be shrunk to %s"
                        % (cloud.name, str(end_date)[:16])
                    )
                else:
                    self.logger.info("Cloud %s can be terminated now" % cloud.name)

        elif self.cli_args["host"]:
            host = self.quads.get_host(self.cli_args["host"])
            if not host:
                raise CliException("Host not found")

            schedule = self.quads.get_current_schedules({"host": host})
            if not schedule:
                self.logger.warning(
                    "The selected host does not have any active schedules"
                )
                future_schedule = self.quads.get_future_schedules({"host": host})
                if not future_schedule:
                    return 1

                if self._confirmation_dialog(
                        f"Would you like to shrink a future allocation of {host.name}? (y/N): "
                ):
                    return

                schedule = future_schedule

            if weeks:
                end_date = schedule.end - time_delta
            else:
                end_date = _date
            if (
                    end_date < schedule.start
                    or end_date > schedule.end
                    or (not self.cli_args["now"] and end_date < threshold)
            ):
                raise CliException(
                    "The host cannot be shrunk past it's start date, target date means an extension"
                    " or target date is earlier than 1 hour from now:"
                )

            if not self.cli_args["check"]:
                if self._confirmation_dialog(
                        "Are you sure you want to shrink"
                        f"{host.name} to {str(end_date)[:16]}? (y/N): "
                ):
                    return

                self.quads.update_schedule(schedule.id, {"end": end_date})

                if weeks:
                    self.logger.info(
                        "Host %s has now been shrunk for %s week[s] to %s"
                        % (host.name, str(weeks), str(end_date)[:16])
                    )
                elif self.cli_args["datearg"]:
                    self.logger.info(
                        "Host %s has now been shrunk to %s"
                        % (host.name, str(end_date)[:16])
                    )
                else:
                    self.logger.info(
                        "Host %s schedule has now been terminated" % host.name
                    )
            else:
                if weeks:
                    self.logger.info(
                        "Host %s can be shrunk for %s weeks until %s"
                        % (host.name, str(weeks), str(end_date)[:16])
                    )
                elif self.cli_args["datearg"]:
                    self.logger.info(
                        "Host %s can been shrunk to %s"
                        % (host.name, str(end_date)[:16])
                    )
                else:
                    self.logger.info(
                        "Host %s schedule can be terminated now" % host.name
                    )

    def action_cloudresource(self):
        data = {
            "cloud": self.cli_args["cloud"],
            "description": self.cli_args["description"],
            "owner": self.cli_args["cloudowner"],
            "ccuser": self.cli_args["ccusers"],
            "qinq": self.cli_args["qinq"],
            "ticket": self.cli_args["cloudticket"],
            "force": self.cli_args["force"],
            "wipe": self.cli_args.get("wipe", True),
        }
        if self.cli_args.get("vlan"):
            try:
                data["vlan"] = int(self.cli_args["vlan"])
            except (TypeError, ValueError) as ཀʖ̯ཀ:
                self.logger.debug(ཀʖ̯ཀ, exc_info=ཀʖ̯ཀ)
                self.logger.error("Could not parse vlan id. Only integers accepted.")
                return 1

        cloud_reservation_lock = int(conf["cloud_reservation_lock"])
        assignment = self.quads.get_active_cloud_assignment(data["cloud"])
        if assignment:
            lock_release = assignment.last_redefined + timedelta(
                hours=cloud_reservation_lock
            )
            cloud_string = f"{assignment.cloud.name}"
            if lock_release > datetime.now():
                time_left = lock_release - datetime.now()
                hours = time_left.total_seconds() // 3600
                minutes = (time_left.total_seconds() % 3600) // 60
                cloud_string += " (reserved: %dhr %dmin remaining)" % (hours, minutes)
                self.logger.warning("Can't redefine cloud:")
                self.logger.warning(cloud_string)
                return 1

        try:
            cloud = self.quads.get_cloud(data["cloud"])
            if not cloud:
                cloud_response = self.quads.insert_cloud(data)
                if cloud_response.status_code == 200:
                    self.logger.info(f"Cloud {data['cloud']} created.")

            response = self.quads.insert_assignment(data)
            if response.status_code == 200:
                self.logger.info("Assignment created.")

        except ConnectionError:
            raise CliException(
                "Could not connect to the quads-server, verify service is up and running."
            )

    def action_modcloud(self):
        data = {
            "name": self.cli_args["cloud"],
            "description": self.cli_args["description"],
            "owner": self.cli_args["cloudowner"],
            "ccuser": self.cli_args["ccusers"],
            "ticket": self.cli_args["cloudticket"],
        }

        clean_data = {k: v for k, v in data.items() if v and k != "name"}
        if self.cli_args.get("vlan"):
            try:
                clean_data["vlan"] = int(self.cli_args["vlan"])
            except (TypeError, ValueError):
                clean_data["vlan"] = None

        if "wipe" in self.cli_args:
            clean_data["wipe"] = self.cli_args["wipe"]
        if "qinq" in self.cli_args:
            clean_data["qinq"] = self.cli_args["qinq"]

        response = self.quads.get_active_cloud_assignment(data["name"])
        assignment = response.json()

        if self.cli_args.get("cloudticket"):
            payload = {"ticket": self.cli_args.get("cloudticket")}
            self.quads.update_assignment(assignment.get("id"), payload)

        self.quads.update_assignment(assignment.get("id"), clean_data)

        self.logger.info("Cloud modified successfully")

    def action_rmcloud(self):
        cloud = self.cli_args.get("cloud")
        if not cloud:
            raise CliException("Missing parameter --cloud")

        response = self.quads.get_active_cloud_assignment(cloud)
        assignment = response.json()
        if assignment:
            raise CliException(f"There is an active cloud assignment for {cloud}")

        _response = self.quads.remove_cloud(self.cli_args["cloud"])
        self._output_json_result(_response, {"cloud": self.cli_args.get("cloud")})

    def action_rmhost(self):
        if not self.cli_args.get("host"):
            raise CliException("Missing parameter --host")
        _response = self.quads.remove_host(self.cli_args["host"])
        self._output_json_result(_response, {"host": self.cli_args.get("host")})

    def action_hostresource(self):
        if not self.cli_args["hostcloud"]:
            raise CliException("Missing option --default-cloud")

        data = {
            "name": self.cli_args["hostresource"],
            "default_cloud": self.cli_args["hostcloud"],
            "host_type": self.cli_args["hosttype"],
            "model": self.cli_args["model"],
            "force": self.cli_args["force"],
        }
        _response = self.quads.create_host(data)
        self._output_json_result(_response, data)

    def action_define_host_metadata(self):
        if not self.cli_args["metadata"]:
            raise CliException("Missing option --metadata")

        if not os.path.exists(self.cli_args["metadata"]):
            raise CliException("The path for the --metadata yaml is not valid")

        try:
            with open(self.cli_args["metadata"]) as md:
                hosts_metadata = yaml.safe_load(md)
        except IOError as ಠ_ಠ:
            self.logger.debug(ಠ_ಠ, exc_info=ಠ_ಠ)
            raise CliException(
                f"There was something wrong reading from {self.cli_args['metadata']}"
            )

        for host_md in hosts_metadata:
            ready_defined = []
            host = self.quads.get_host(host_md.get("name"))
            if not host:
                self.logger.warning(
                    f"Host {host_md.get('name')} not found. Check hostname or if name is defined on the yaml. IGNORING."
                )
                continue

            data = {}
            dispatch_create = {
                "disks": self.quads.create_disk,
                "interfaces": self.quads.create_interface,
                "memory": self.quads.create_memory,
                "processors": self.quads.create_processor,
            }
            for key, value in host_md.items():
                if key != "name" and host[key]:
                    ready_defined.append(key)
                    if not self.cli_args["force"]:
                        continue
                    if type(value) == list:
                        self.clear_field(host, key)
                        dispatch_func = dispatch_create.get(key)
                        for obj in value:

                            if dispatch_func:
                                dispatch_func(obj)
                            else:
                                raise CliException(
                                    f"Invalid key '{key}' on metadata for {host.name}"
                                )

                elif key == "default_cloud":
                    cloud = self.quads.get_cloud(value)
                    data[key] = cloud
                else:
                    data = {"name": host.name, key: value}

            if ready_defined:
                action = "SKIPPING" if not self.cli_args["force"] else "RECREATING"
                self.logger.warning(f"{host.name} [{action}]: {ready_defined}")
            if data and len(data.keys()) > 1:
                host.update(**data)

        if not self.cli_args["force"]:
            self.logger.warning("For overwriting existing values use the --force.")

    def action_host_metadata_export(self):
        all_hosts = self.quads.get_hosts()
        content = []
        for host in all_hosts:
            host_meta = {
                "name": host.name,
                "model": host.model,
                "host_type": host.host_type,
                "default_cloud": host.default_cloud.name,
            }

            interfaces = []
            for interface in host.interfaces:
                interface_dict = {
                    "name": interface.name,
                    "mac_address": interface.mac_address,
                    "switch_ip": interface.switch_ip,
                    "switch_port": interface.switch_port,
                    "speed": interface.speed,
                    "vendor": interface.vendor,
                    "pxe_boot": interface.pxe_boot,
                    "maintenance": interface.maintenance,
                }
                interfaces.append(interface_dict)
            if interfaces:
                host_meta["interfaces"] = interfaces

            disks = []
            for disk in host.disks:
                disk_dict = {
                    "disk_type": disk.disk_type,
                    "size_gb": disk.size_gb,
                    "count": disk.count,
                }
                disks.append(disk_dict)
            if disks:
                host_meta["disks"] = disks

            content.append(host_meta)

        try:
            with open(self.cli_args["host_metadata_export"], "w") as _file:
                yaml.dump(content, _file)
        except Exception as ಠ益ಠ:
            self.logger.debug(ಠ益ಠ, exc_info=ಠ益ಠ)
            raise BaseQuadsException(
                "There was something wrong writing to file."
            ) from ಠ益ಠ

        self.logger.info("Metadata successfully exported.")
        return 0

    def action_add_schedule(self):
        if (
                self.cli_args["schedstart"] is None
                or self.cli_args["schedend"] is None
                or self.cli_args["schedcloud"] is None
        ):
            raise CliException(
                "\n".join(
                    (
                        "Missing option. All of these options are required for --add-schedule:",
                        "\t--schedule-start",
                        "\t--schedule-end",
                        "\t--schedule-cloud",
                    )
                )
            )

        if self.cli_args["host"] is None and self.cli_args["host_list"] is None:
            raise CliException("Missing option. --host or --host-list required.")

        omitted_cloud_id = None
        if self.cli_args["omitcloud"]:
            _clouds = self.quads.get_clouds()
            clouds = json.loads(_clouds)
            omitted_cloud = [
                c for c in clouds if c.get("name") == self.cli_args["omitcloud"]
            ]
            if len(omitted_cloud) == 0:
                self.logger.warning(
                    f"No cloud named {self.cli_args['omitcloud']} found."
                )
            omitted_cloud_id = omitted_cloud[0].get("_id").get("$oid")

        if self.cli_args["host"]:
            if self.cli_args["omitcloud"] and omitted_cloud_id:
                host_obj = self.quads.get_host(self.cli_args["host"])
                host_json = json.loads(host_obj)
                if host_json.get("cloud").get("$oid") == omitted_cloud_id:
                    self.logger.info(
                        "Host is in part of the cloud specified with --omit-cloud. Nothing has been done."
                    )
            else:
                data = {
                    "cloud": self.cli_args["schedcloud"],
                    "host": self.cli_args["host"],
                    "start": self.cli_args["schedstart"],
                    "end": self.cli_args["schedend"],
                }
                try:
                    response = self.quads.insert_schedule(data)
                    if response.status_code == 200:
                        self.logger.info("Schedule created")
                    else:
                        data = response.json()
                        self.logger.error(f"Status code:{data.get('status_code')}, Error: {data.get('message')}")
                except ConnectionError:
                    raise CliException(
                        "Could not connect to the quads-server, verify service is up and running."
                    )

        elif self.cli_args["host_list"]:
            try:
                with open(self.cli_args["host_list"]) as _file:
                    host_list_stream = _file.read()
            except IOError:
                raise CliException(f"{self.cli_args['host_list']} File Error.")

            host_list = host_list_stream.split()
            non_available = []
            _sched_start = datetime.strptime(
                self.cli_args["schedstart"], "%Y-%m-%d %H:%M"
            )
            _sched_end = datetime.strptime(self.cli_args["schedend"], "%Y-%m-%d %H:%M")

            if self.cli_args["omitcloud"] and omitted_cloud_id:
                self.logger.info(
                    f"INFO - All hosts from {self.cli_args['omitcloud']} will be omitted."
                )
                omitted = []

                for host in host_list:
                    host_obj = self.quads.get_host(host)
                    host_json = json.loads(host_obj)
                    if host_json.get("cloud").get("$oid") == omitted_cloud_id:
                        omitted.append(host)
                for host in omitted:
                    host_list.remove(host)
                    self.logger.info(f"{host} will be omitted.")

            for host in host_list:
                is_available = self.quads.is_available(
                    hostname=host,
                    data={
                        "start": _sched_start,
                        "end": _sched_end,
                    },
                )
                host_obj = self.quads.get_host(host)
                if not is_available or host_obj.broken:
                    non_available.append(host)

            if non_available:
                self.logger.error(
                    "The following hosts are either broken or unavailable:"
                )

                for host in non_available:
                    self.logger.error(host)
                raise CliException("Remove these from your host list and try again.")

            for host in host_list:
                data = {
                    "cloud": self.cli_args["schedcloud"],
                    "host": host,
                    "start": self.cli_args["schedstart"],
                    "end": self.cli_args["schedend"],
                }
                try:
                    response = self.quads.insert_schedule(data)
                    if response.status_code == 200:
                        self.logger.info("Schedule created")
                    else:
                        self.logger.error("There was something wrong creating the schedule entry")
                except ConnectionError:
                    raise CliException(
                        "Could not connect to the quads-server, verify service is up and running."
                    )

            template_file = "jira_ticket_assignment"
            with open(os.path.join(conf.TEMPLATES_PATH, template_file)) as _file:
                template = Template(_file.read())

            _cloud = self.quads.get_cloud(self.cli_args["schedcloud"])
            jira_docs_links = conf["jira_docs_links"].split(",")
            jira_vlans_docs_links = conf["jira_vlans_docs_links"].split(",")
            comment = template.render(
                schedule_start=self.cli_args["schedstart"],
                schedule_end=self.cli_args["schedend"],
                cloud=self.cli_args["schedcloud"],
                jira_docs_links=jira_docs_links,
                jira_vlans_docs_links=jira_vlans_docs_links,
                host_list=host_list_stream,
                vlan=_cloud.vlan,
            )

            loop = asyncio.get_event_loop()
            try:
                jira = Jira(
                    conf["jira_url"],
                    loop=loop,
                )
            except JiraException as ex:
                self.logger.error(ex)
                exit(1)
            result = loop.run_until_complete(jira.post_comment(_cloud.ticket, comment))
            if not result:
                self.logger.warning("Failed to update Jira ticket")

            transitions = loop.run_until_complete(jira.get_transitions(_cloud.ticket))
            transition_result = False
            for transition in transitions:
                t_name = transition.get("name")
                if t_name and t_name.lower() == "scheduled":
                    transition_id = transition.get("id")
                    transition_result = loop.run_until_complete(
                        jira.post_transition(_cloud.ticket, transition_id)
                    )
                    break

            if not transition_result:
                self.logger.warning("Failed to update ticket status")

        return 0

    def action_rmschedule(self):
        if self.cli_args["schedid"] is None:
            raise CliException("Missing option --schedule-id.")

        try:
            self.logger.info(self.quads.remove_schedule(self.cli_args["schedid"]))
        except (ConnectionError, Exception) as ex:
            raise CliException(
                "Could not connect to the quads-server, verify service is up and running."
            )
        return 0

    def action_modschedule(self):
        if self.cli_args["host"] is None:
            raise CliException("Missing option. Need --host when using --mod-schedule")

        if (
                self.cli_args["schedstart"] is None
                and self.cli_args["schedend"] is None
                and self.cli_args["schedcloud"] is None
        ):
            raise CliException(
                "\n".join(
                    (
                        "Missing option. At least one these options are required for --mod-schedule:",
                        "\t--schedule-start",
                        "\t--schedule-end",
                        "\t--schedule-cloud",
                    )
                )
            )

        data = {
            "index": self.cli_args["modschedule"],
            "start": self.cli_args["schedstart"],
            "end": self.cli_args["schedend"],
            "cloud": self.cli_args["schedcloud"],
            "host": self.cli_args["host"],
        }
        try:
            self.logger.info(self.quads.insert_schedule(data)["result"])
        except ConnectionError:
            raise CliException(
                "Could not connect to the quads-server, verify service is up and running."
            )

        return 0

    def action_movehosts(self):
        if self.cli_args["datearg"] is not None and not self.cli_args["dryrun"]:
            raise CliException(
                "--move-hosts and --date are mutually exclusive unless using --dry-run."
            )

        url = os.path.join(conf.API_URL, "moves")
        date = ''
        if self.cli_args["datearg"] is not None:
            date = datetime.strptime(
                self.cli_args["datearg"], "%Y-%m-%d %H:%M"
            ).isoformat()
        _response = requests.get(os.path.join(url, date))
        if _response.status_code == 200:
            data = _response.json()
            if not data:
                self.logger.info("Nothing to do.")
                return 0

            _clouds = defaultdict(list)
            for result in data:
                _clouds[result["new"]].append(result)

            # TODO:
            #  raise the number of semaphores after this is resolved
            #  https://projects.theforeman.org/issues/27953#change-127120
            semaphore = asyncio.Semaphore(1)
            for _cloud, results in _clouds.items():
                provisioned = True
                tasks = []
                switch_tasks = []
                for result in results:
                    host = result["host"]
                    current = result["current"]
                    new = result["new"]
                    cloud = self.quads.get_cloud(new)
                    response = self.quads.get_active_cloud_assignment(cloud.name)
                    data = response.json()
                    target_assignment = None
                    if data:
                        target_assignment = Assignment().from_dict(data=data)
                    wipe = target_assignment.wipe if target_assignment else False

                    self.logger.info(
                        "Moving %s from %s to %s, wipe = %s"
                        % (host, current, new, wipe)
                    )
                    if not self.cli_args["dryrun"]:
                        self.quads.update_host(host, {"switch_config_applied": False})
                        if new != "cloud01":
                            has_active_schedule = self.quads.get_current_schedules(
                                {"cloud": f"{cloud.name}"}
                            )
                            if has_active_schedule and wipe:
                                assignment = self.quads.get_active_cloud_assignment(
                                    cloud.name
                                )
                                self.quads.update_assignment(
                                    assignment.id, {"validated": False}
                                )
                        try:
                            if self.cli_args["movecommand"] == default_move_command:
                                fn = functools.partial(
                                    move_and_rebuild, host, new, semaphore, cloud.wipe
                                )
                                tasks.append(fn)
                                omits = conf.get("omit_network_move")
                                omit = False
                                if omits:
                                    omits = omits.split(",")
                                    omit = [
                                        omit
                                        for omit in omits
                                        if omit in host or omit == new
                                    ]
                                if not omit:
                                    switch_tasks.append(
                                        functools.partial(
                                            switch_config, host, current, new
                                        )
                                    )
                            else:
                                if cloud.wipe:
                                    subprocess.check_call(
                                        [
                                            self.cli_args["movecommand"],
                                            host,
                                            current,
                                            new,
                                        ]
                                    )
                                else:
                                    subprocess.check_call(
                                        [
                                            self.cli_args["movecommand"],
                                            host,
                                            current,
                                            new,
                                            "nowipe",
                                        ]
                                    )
                        except Exception as ex:
                            self.logger.debug(ex)
                            self.logger.exception(
                                "Move command failed for host: %s" % host
                            )
                            provisioned = False

                if not self.cli_args["dryrun"]:

                    _old_cloud_obj = self.quads.get_cloud(results[0]["current"])
                    old_cloud_schedule = self.quads.get_current_schedules(
                        {"cloud": _old_cloud_obj}
                    )

                    if not old_cloud_schedule and _old_cloud_obj.name != "cloud01":
                        assignment = self.quads.get_active_cloud_assignment(
                            _old_cloud_obj
                        )
                        payload = {"active": False}
                        self.quads.update_assignment(assignment.id, payload)

                    done = None
                    loop = asyncio.get_event_loop()
                    loop.set_exception_handler(
                        lambda _loop, ctx: self.logger.error(
                            f"Caught exception: {ctx['message']}"
                        )
                    )

                    try:
                        done = loop.run_until_complete(
                            asyncio.gather(*[task(loop) for task in tasks])
                        )
                    except (
                            asyncio.CancelledError,
                            SystemExit,
                            Exception,
                            TimeoutError,
                    ):
                        self.logger.exception("Move command failed")
                        provisioned = False
                    for task in switch_tasks:
                        try:
                            host_obj = self.quads.get_host(task.args[0])

                            if not host_obj.switch_config_applied:
                                self.logger.info(
                                    f"Running switch config for {task.args[0]}"
                                )
                                result = task()
                                if result:
                                    host_obj.update(switch_config_applied=True)
                                else:
                                    self.logger.exception(
                                        "There was something wrong configuring the switch."
                                    )

                        except Exception as exc:
                            self.logger.exception(
                                "There was something wrong configuring the switch.",
                                exc_info=exc,
                            )

                    if done:
                        for future in done:
                            if isinstance(future, Exception):
                                provisioned = False
                            else:
                                provisioned = provisioned and future

                    if provisioned:
                        _new_cloud_obj = self.quads.get_cloud(_cloud)
                        validate = not _new_cloud_obj.wipe
                        assignment = self.quads.get_active_cloud_assignment(
                            _new_cloud_obj
                        )
                        self.quads.update_assignment(
                            assignment.id, {"provisioned": True, "validated": validate}
                        )

            return 0

    def action_mark_broken(self):
        if not self.cli_args["host"]:
            raise CliException("Missing option. Need --host when using --mark-broken")

        host = self.quads.get_host(self.cli_args["host"])
        if host:
            if host.broken:
                self.logger.warning(
                    f"Host {self.cli_args['host']} has already been marked broken"
                )
            else:
                self.quads.update_host(self.cli_args["host"], {"broken": True})
                self.logger.info(
                    f"Host {self.cli_args['host']} is now marked as broken"
                )
        else:
            raise CliException(f"Host {self.cli_args['host']} not found")

    def action_mark_repaired(self):
        if not self.cli_args["host"]:
            raise CliException("Missing option. Need --host when using --mark-repaired")

        host = self.quads.get_host(self.cli_args["host"])
        if not host:
            raise CliException("Host not found")

        if not host.broken:
            self.logger.warning(
                f"Host {self.cli_args['host']} has already been marked repaired"
            )
        else:
            self.quads.update_host(self.cli_args["host"], {"broken": False})
            self.logger.info(f"Host {self.cli_args['host']} is now marked as repaired")

    def action_retire(self):
        if not self.cli_args["host"]:
            raise CliException("Missing option. Need --host when using --retire")

        host = self.quads.get_host(self.cli_args["host"])
        if not host:
            raise CliException(f"Host {self.cli_args['host']} not found")

        if host.retired:
            self.logger.warning(
                f"Host {self.cli_args['host']} has already been marked as retired"
            )
        else:
            self.quads.update_host(self.cli_args["host"], {"retired": True})
            self.logger.info(f"Host {self.cli_args['host']} is now marked as retired")

    def action_unretire(self):
        if not self.cli_args["host"]:
            raise CliException("Missing option. Need --host when using --unretire")

        host = self.quads.get_host(self.cli_args["host"])

        if not host.retired:
            self.logger.warning(
                f"Host {self.cli_args['host']} has already been marked unretired"
            )
        else:
            self.quads.update_host(self.cli_args["host"], {"retired": False})
            self.logger.info(f"Host {self.cli_args['host']} is now marked as unretired")

    def action_host(self):
        host = self.quads.get_host(self.cli_args["host"])
        if not host:
            raise CliException(f"Unknown host: {self.cli_args['host']}")

        _kwargs = {"host": host}
        if self.cli_args["datearg"]:
            datetime_obj = datetime.strptime(self.cli_args["datearg"], "%Y-%m-%d %H:%M")
            _kwargs["date"] = datetime_obj.isoformat()
        else:
            datetime_obj = datetime.now()
        schedules = self.quads.get_current_schedules(**_kwargs)
        if schedules:
            for schedule in schedules:
                if schedule["end"] != datetime_obj:
                    self.logger.info(schedule["cloud"])
        else:
            self.logger.info(host.default_cloud.name)

    def action_cloudonly(self):
        _cloud = self.quads.get_cloud(self.cli_args["cloud"])
        if not _cloud:
            raise CliException("Cloud is not defined.")

        _kwargs = {"cloud": _cloud}
        if self.cli_args["datearg"]:
            _kwargs["date"] = datetime.strptime(
                self.cli_args["datearg"], "%Y-%m-%d %H:%M"
            ).isoformat()
        schedules = self.quads.get_current_schedules(**_kwargs)
        if schedules:
            _kwargs = {"retired": False}
            if self.cli_args["filter"]:
                filter_args = self._filter_kwargs(self.cli_args["filter"])
                _kwargs.update(filter_args)
            _hosts = self.quads.get_hosts()
            for schedule in sorted(schedules, key=lambda k: k["host"]["name"]):
                # TODO: check data properties
                if schedule["host"] in _hosts:
                    self.logger.info(schedule.host.name)
        else:
            if _kwargs.get("date") and self.cli_args["cloudonly"] == "cloud01":
                data = {
                    "start": _kwargs["date"],
                    "end": _kwargs["date"],
                }

                try:
                    available_hosts = self.quads.get_available(**data)
                except ConnectionError:
                    raise CliException(
                        "Could not connect to the quads-server, verify service is up and running."
                    )

                _kwargs = {}
                if self.cli_args["filter"]:
                    filter_args = self._filter_kwargs(self.cli_args["filter"])
                    _kwargs.update(filter_args)
                _hosts = []
                # TODO: check return from API
                _hosts = self.quads.get_hosts()
                for host in sorted(_hosts, key=lambda k: k["name"]):
                    _hosts.append(host.name)
                for host in sorted(available_hosts):
                    if host in _hosts:
                        self.logger.info(host)
            else:
                _kwargs = {"cloud": _cloud}
                if self.cli_args["filter"]:
                    filter_args = self._filter_kwargs(self.cli_args["filter"])
                    _kwargs.update(filter_args)
                # TODO: check return from API
                _hosts = self.quads.get_hosts()
                for host in sorted(_hosts, key=lambda k: k["name"]):
                    self.logger.info(host.name)

    def action_summary(self):
        _kwargs = {}
        if self.cli_args["datearg"]:
            _kwargs["date"] = datetime.strptime(
                self.cli_args["datearg"], "%Y-%m-%d %H:%M"
            ).isoformat()
        try:
            summary = self.quads.get_summary(**_kwargs)
        except ConnectionError:
            raise CliException(
                "Could not connect to the quads-server, verify service is up and running."
            )

        for cloud in summary:
            if self.cli_args["fullsummary"] or cloud["count"] > 0:
                if self.cli_args["detail"]:
                    self.logger.info(
                        "%s (%s): %s (%s) - %s"
                        % (
                            cloud["name"],
                            cloud["owner"],
                            cloud["count"],
                            cloud["description"],
                            cloud["ticket"],
                        )
                    )
                else:
                    self.logger.info(
                        "%s: %s (%s)"
                        % (cloud["name"], cloud["count"], cloud["description"])
                    )
