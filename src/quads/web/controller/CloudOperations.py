from datetime import datetime
import re

from quads.quads_api import APIBadRequest, APIServerException


class CloudOperations:

    def __init__(self, quads_api, foreman, loop):
        self.__quads_api = quads_api
        self.__foreman = foreman
        self.__loop = loop

    def __get_cloud_summary(self) -> list:
        """
        This method returns the cloud summary
        """
        clouds_summary = []
        summary_response = self.__quads_api.get_summary(data={})
        if summary_response.status_code == 200:
            clouds_summary = summary_response.json()
        return clouds_summary

    def __get_all_hosts(self):
        """
        This method returns the all hosts
        """
        all_hosts = self.__loop.run_until_complete(self.__foreman.get_all_hosts())
        return all_hosts

    def get_managed_nodes(self):
        """
        This method returns the scheduled nodes
        """
        managed_hosts = []
        for cloud in self.__get_cloud_summary():
            if cloud["count"] > 0:
                _cloud_obj = self.__quads_api.get_cloud(cloud.get("name"))
                _hosts = sorted(
                    self.__quads_api.filter_hosts({"cloud": _cloud_obj.name, "retired": False, "broken": False}),
                    key=lambda x: x.name,
                )
                managed_hosts.append({
                    "name": cloud.get("name").strip(),
                    "owner": cloud.get("owner").strip(),
                    "count": cloud.get("count"),
                    "description": cloud.get("description").strip(),
                    "hosts": [self.__get_current_schedules(host.name) for host in _hosts],
                })
        return managed_hosts

    def get_daily_utilization(self) -> int:
        """
        This method returns the daily utilization
        """
        _host_count = len(self.__quads_api.filter_hosts({"broken": False, "retired": False}))
        _schedules = len(self.__quads_api.get_current_schedules())
        _daily_utilization = _schedules * 100 // _host_count
        return int(_daily_utilization)

    def get_cloud_summary_report(self) -> list:
        """
        This method returns the cloud summary
        """
        clouds_summary = []
        for cloud in self.__get_cloud_summary():
            if cloud.get("count") > 0:
                cloud_name = cloud.get("name")
                scheduled_hosts = len(self.__quads_api.get_current_schedules({"cloud": cloud_name}))
                moved_hosts = len(self.__quads_api.filter_hosts({"cloud": cloud_name}))
                try:
                    percent = (moved_hosts / scheduled_hosts) * 100
                except Exception as err:
                    percent = 0
                if cloud_name == 'cloud01':
                    percent = 100
                cloud['percent'] = percent
                clouds_summary.append(cloud)
        return clouds_summary

    def __get_current_schedules(self, host: str) -> dict:
        """
        This method returns the current schedules
        """
        short_host = host.split(".")[0]
        _schedule_obj = None
        _schedules = self.__quads_api.get_current_schedules({"host": host})
        if _schedules:
            _schedule_obj = _schedules[0]
        if not _schedule_obj:
            _date_start = "∞"
            _date_end = "∞"
            total_time = "∞"
            total_time_left = "∞"
        else:
            _date_now = datetime.now()
            _date_start = _schedule_obj.start
            _date_end = _schedule_obj.end
            total_sec_left = (_date_end - _date_now).total_seconds()
            total_days = (_date_end - _date_start).days
            total_days_left = total_sec_left // 86400
            total_hours_left = ((total_sec_left / 86400) - total_days_left) * 24
            total_time = "%0d day(s)" % total_days
            total_time_left = "%0d day(s)" % total_days_left
            if total_hours_left > 1:
                total_time_left = "%s, %0d hour(s)" % (total_time_left, total_hours_left)
            _date_start = _date_start.strftime("%Y-%m-%d")
            _date_end = _date_end.strftime("%Y-%m-%d")
        current_schedule = {
            "short_name": short_host,
            "name": host,
            "start_date": _date_start,
            "end_date": _date_end,
            "total_time": total_time,
            "total_time_left": total_time_left,
        }
        return current_schedule

    def get_domain_broken_hosts(self, domain: str):
        """
        This method returns the broken hosts
        """
        broken_hosts = self.__quads_api.filter_hosts({"broken": False})
        return [host for host in broken_hosts if domain in host.name]

    def get_unmanaged_hosts(self, exclude_hosts: str):
        """
        This method returns the unmanaged hosts
        """
        all_hosts = self.__get_all_hosts()
        blacklist = re.compile("|".join([re.escape(word) for word in exclude_hosts.split("|")]))
        mgmt_hosts = {}
        for host, properties in all_hosts.items():
            if not blacklist.search(host):
                if properties.get("sp_name", False):
                    properties["host_ip"] = all_hosts.get(host, {"ip": None})["ip"]
                    properties["host_mac"] = all_hosts.get(host, {"mac": None})["mac"]
                    properties["ip"] = properties.get("sp_ip")
                    properties["mac"] = properties.get("sp_mac")
                    mgmt_hosts[properties.get("sp_name")] = properties
        unmanaged_hosts = []
        for host, properties in mgmt_hosts.items():
            real_host = host[5:]
            try:
                host_obj = self.__quads_api.get_host(real_host)
            except (APIBadRequest, APIServerException):
                host_obj = None

            if not host_obj:
                short_host = real_host.split(".")[0]
                unmanaged_hosts.append({
                    "name": host,
                    "short_name": short_host,
                })
        return unmanaged_hosts

