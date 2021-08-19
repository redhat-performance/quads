import asyncio
import calendar
import struct
from asyncio import sleep
from json import JSONDecodeError

from bson.objectid import ObjectId
from datetime import timedelta
from mongoengine import ObjectIdField
from quads.config import SUPPORTED, OFFSETS, conf


def param_check(data, params, defaults={}):
    result = []
    # set defaults
    for k, v in defaults.items():
        data.setdefault(k, v)

    if data:
        # check for missing params
        for param in params:
            if param not in data:
                result.append("Missing required parameter: %s" % param)
            elif not data[param]:
                result.append("Could not parse %s parameter" % param)
            elif data[param] == 'None':
                data[param] = None
            if param == "_id":
                data["_id"] = ObjectIdField(data[param])

    return result, data


def is_supported(_host_name):
    for host_type in SUPPORTED:
        if host_type in _host_name:
            return True
    return False


def get_vlan(cloud_obj, index, last_nic=False):
    if cloud_obj.vlan and last_nic:
        return int(cloud_obj.vlan.vlan_id)
    else:
        vlan_first = int(conf.get("sw_vlan_first", 1100)) - 10
        cloud_offset = int(cloud_obj.name[5:]) * 10
        base_vlan = vlan_first + cloud_offset
        if cloud_obj.qinq == 1:
            index = 0
        vlan = base_vlan + list(OFFSETS.values())[index]
        return vlan


def date_span(start, end, delta=timedelta(days=1)):
    current = start
    while current < end:
        yield current
        current += delta


def month_delta_past(date, months):
    years = months // 12
    year = date.year - years
    month_delta = months % 12
    if not month_delta:
        return date.replace(year=year)
    if month_delta > date.month:
        year -= 1
        month = 12 - month_delta
        day = min(date.day, calendar.monthrange(year, month)[1])
        return date.replace(year=year, month=month, day=day)
    else:
        month = date.month - month_delta
        if month:
            day = min(date.day, calendar.monthrange(year, month)[1])
            return date.replace(year=year, month=month, day=day)
        return date.replace(year=year)


def last_day_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def first_day_month(date):
    return date - timedelta(days=date.day-1)


def date_to_object_id(date):
    """
    Create a dummy ObjectId instance with a specific datetime.

    This method is useful for doing range queries by oid creation date.

    .. _warning:
           It is not safe to insert a document containing an ObjectId
           generated using this method. This method deliberately
           eliminates the uniqueness guarantee that ObjectIds
           generally provide. ObjectIds generated with this method
           should be used exclusively in queries.
    """
    timestamp = calendar.timegm(date.timetuple())
    oid = struct.pack(
        ">I",
        int(timestamp)
    ) + b"\x00\x00\x00\x00\x00\x00\x00\x00"
    return ObjectId(oid)


async def execute_ipmi(host, arguments, semaphore):
    ipmi_cmd = [
        "/usr/bin/ipmitool",
        "-I",
        "lanplus",
        "-H",
        "mgmt-%s" % host,
        "-U",
        conf["ipmi_username"],
        "-P",
        conf["ipmi_password"],
    ]
    cmd = ipmi_cmd + arguments
    async with semaphore:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )
        await process.communicate()


async def ipmi_reset(host, semaphore):
    ipmi_off = [
        "chassis",
        "power",
        "off",
    ]
    await execute_ipmi(host, ipmi_off, semaphore)
    await sleep(conf["ipmi_reset_sleep"])
    ipmi_on = [
        "chassis",
        "power",
        "on",
    ]
    await execute_ipmi(host, ipmi_on, semaphore)


async def ipmi_pxe_persist(host, semaphore):
    ipmi_pxe_persistent = [
        "chassis",
        "bootdev",
        "pxe",
        "options=persistent",
    ]
    await execute_ipmi(
        host, arguments=ipmi_pxe_persistent, semaphore=semaphore
    )


def output_json_result(request, data, logger):
    try:
        if request.status_code == 204:
            logger.info("Removed: %s" % data)
        else:
            js = request.json()
            logger.debug("%s %s: %s" % (request.status_code, request.reason, data))
            for result in js["result"]:
                if type(result) == list:
                    for line in result:
                        logger.info(line)
                else:
                    logger.info(result)
    except JSONDecodeError:
        logger.error("Could not parse json reply.")
        logger.debug(request.text)
        exit(1)


def exception_handler(loop, context, logger):
    logger.error(f"Caught exception: {context['message']}")


def filter_kwargs(filter_args, logger):
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

                if keys[0].strip().lower() in ["disks", "interfaces"]:

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
                            logger.error("Model type not recognized.")
                            logger.warning(
                                f"Accepted model names are: {conf['models']}"
                            )
                            exit(1)
                    if type(value) == str:
                        value = value.upper()
                    query = {f"{'__'.join(keys)}{op_suffix}": value}
                    kwargs.update(query)
                break
        if not op_found:
            logger.error(
                "A filter was defined but not parsed correctly. Check filter operator."
            )
            logger.warning(f"Condition: {condition}")
            logger.warning(f"Accepted operators: {', '.join(ops.keys())}")
            exit(1)
    if not kwargs:
        logger.error(
            "A filter was defined but not parsed correctly. Check filter syntax."
        )
        exit(1)
    return kwargs
