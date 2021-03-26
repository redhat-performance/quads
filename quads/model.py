from datetime import datetime, timedelta
import ipaddress
import os

from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    queryset_manager,
    Q,
    StringField,
    BooleanField,
    ListField,
    ReferenceField,
    DateTimeField,
    SequenceField,
    IntField,
    LongField,
    EmbeddedDocumentField,
)
from quads.helpers import param_check


connect("quads", host=os.environ.get("MONGODB_IP", "127.0.0.1"))


class Vlan(Document):
    gateway = StringField()
    ip_free = IntField()
    ip_range = StringField()
    netmask = StringField()
    vlan_id = LongField()
    meta = {"indexes": [{"fields": ["$vlan_id"]}], "strict": False}

    @staticmethod
    def prep_data(data):
        _fields = [
            "gateway",
            "ip_range",
            "vlan_id",
        ]
        if "iprange" in data:
            data["ip_range"] = data.pop("iprange")
        if "vlanid" in data:
            data["vlan_id"] = data.pop("vlanid")
        ip_address = ipaddress.ip_network(data["ip_range"])
        data["netmask"] = str(ip_address.netmask)
        data["ip_free"] = ip_address.num_addresses - 2
        result, data = param_check(data, _fields)

        return result, data


class Notification(EmbeddedDocument):
    fail = BooleanField(default=False)
    success = BooleanField(default=False)
    initial = BooleanField(default=False)
    pre_initial = BooleanField(default=False)
    pre = BooleanField(default=False)
    one_day = BooleanField(default=False)
    three_days = BooleanField(default=False)
    five_days = BooleanField(default=False)
    seven_days = BooleanField(default=False)
    meta = {"strict": False}


class Cloud(Document):
    name = StringField(unique=True)
    assignment = ReferenceField('Assignment')
    last_redefined = DateTimeField(default=datetime.now() - timedelta(hours=3))

    meta = {"indexes": [{"fields": ["$name"]}], "strict": False}


class Assignment(Document):
    cloud = ReferenceField(Cloud, required=True)
    active = BooleanField(default=True)
    provisioned = BooleanField(default=False)
    validated = BooleanField(default=False)
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qinq = IntField()
    wipe = BooleanField()
    ccuser = ListField()
    notification = EmbeddedDocumentField(Notification)
    vlan = ReferenceField(Vlan)
    meta = {"strict": False}

    @staticmethod
    def prep_data(data, fields=None, mod=False):
        if not mod:
            data["validated"] = False
            data["last_redefined"] = datetime.now()
            data["notification"] = Notification()

        if "vlan" in data and data["vlan"]:
            vlan_id = data.pop("vlan")
            try:
                int(vlan_id)
            except ValueError:
                data["vlan"] = None
            else:
                vlan_obj = Vlan.objects(vlan_id=vlan_id).first()
                if not vlan_obj:
                    return ["No VLAN object defined with id: %s" % vlan_id], {}
                cloud_obj = Cloud.objects(vlan=vlan_obj).first()
                if cloud_obj:
                    return ["VLAN %s already in use." % vlan_id], {}
                data["vlan"] = vlan_obj
        if "ccuser" in data:
            data["ccuser"] = data["ccuser"].split()
        if "wipe" in data:
            if str(data["wipe"]).lower() == "false":
                data["wipe"] = False
            else:
                data["wipe"] = True

        if data.get("name"):
            cloud = Cloud.objects(name=data.get("name")).first()
            force = data.get("force", False) == "True"
            if not cloud and force:
                cloud = Cloud(name=data.get("name")).save()
            elif not cloud and not force:
                return ["Cloud %s not found. Try with --force to define a new cloud." % data.get("name")], {}
            data["cloud"] = cloud
            data.pop("name")

        if not fields:
            fields = ["description", "owner", "ticket"]

        if "qinq" in fields:
            fields.remove("qinq")
        if "wipe" in fields:
            fields.remove("wipe")

        for flag in ["provisioned", "validated", "last_redefined", "force"]:
            if flag in data:
                data.pop(flag)

        result, data = param_check(data, fields)

        return result, data


class Disk(EmbeddedDocument):
    disk_type = StringField()
    size_gb = LongField()
    count = IntField()
    meta = {"strict": False}

    @staticmethod
    def prep_data(data):
        _fields = ["disk_type", "size_gb", "count"]
        result, data = param_check(data, _fields)

        return result, data


class Interface(EmbeddedDocument):
    name = StringField()
    bios_id = StringField()
    mac_address = StringField()
    ip_address = StringField()
    switch_port = StringField()
    speed = LongField(default=-1)
    vendor = StringField(default="")
    pxe_boot = BooleanField(default=False)
    maintenance = BooleanField(default=False)
    meta = {"strict": False}

    @staticmethod
    def prep_data(data, fields=None):
        if not fields:
            fields = ["name", "mac_address", "ip_address", "switch_port"]

        if data.get("vendor"):
            data["vendor"] = data.get("vendor").upper()

        result, data = param_check(data, fields)

        return result, data


class Host(Document):
    name = StringField(unique=True)
    model = StringField()
    cloud = ReferenceField(Cloud)
    default_cloud = ReferenceField(Cloud)
    host_type = StringField()
    interfaces = ListField(EmbeddedDocumentField(Interface))
    build = BooleanField(default=False)
    validated = BooleanField(default=False)
    last_build = DateTimeField()
    disks = ListField(EmbeddedDocumentField(Disk))
    switch_config_applied = BooleanField(default=False)
    broken = BooleanField(default=False)
    retired = BooleanField(default=False)
    meta = {"indexes": [{"fields": ["$name"]}], "strict": False}

    @staticmethod
    def prep_data(data, fields=None):
        if "default_cloud" in data:
            _default_cloud_obj = Cloud.objects(name=data["default_cloud"]).first()
            if _default_cloud_obj:
                data["default_cloud"] = _default_cloud_obj
            else:
                return ["Cloud %s does not exist." % data["default_cloud"]], {}
        if not fields:
            fields = ["name", "host_type"]

        result, data = param_check(data, fields)

        return result, data


class Counters(Document):
    _id = StringField()
    seq = SequenceField()


class Schedule(Document):
    assignment = ReferenceField(Assignment, required=True)
    host = ReferenceField(Host, required=True)
    start = DateTimeField()
    end = DateTimeField()
    build_start = DateTimeField()
    build_end = DateTimeField()
    index = IntField()
    meta = {"strict": False}

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ["host"])

        return result, data

    @staticmethod
    def get_next_sequence(name):
        Counters.objects(_id=name).update_one(upsert=True, inc__seq=1)
        return Counters.objects(_id=name).first()["seq"]

    def insert_schedule(self, host, assignment, start, end):
        self.index = self.get_next_sequence(host)
        self.host = Host.objects(name=host).first()
        self.assignment = assignment
        self.start = start
        self.end = end
        return self.save()

    @queryset_manager
    def is_host_available(self, queryset, host, start, end, exclude=None):
        _host = Host.objects(name=host).first()
        if _host.broken or _host.retired:
            return False
        _query = Q(host=_host)
        if exclude:
            _query = _query & Q(index__ne=exclude)
        results = queryset.filter(_query)
        for result in results:
            if result["start"] <= start < result["end"]:
                return False
            if result["start"] < end <= result["end"]:
                return False
            if start < result["start"] and end > result["end"]:
                return False
        return True

    @queryset_manager
    def future_schedules(self, queryset, host=None, cloud=None):
        now = datetime.now()
        _query = Q(end__gte=now)
        if host:
            _query = _query & Q(host=host)
        if cloud:
            # TODO: check assignment group search
            assignment = Assignment.objects(cloud=cloud).first()
            _query = _query & Q(assignment=assignment)
        return queryset.filter(_query)

    @queryset_manager
    def current_schedule(self, queryset, date=None, host=None, cloud=None, assignment=None):
        if not date:
            date = datetime.now()
        _query = Q(start__lte=date) & Q(end__gte=date)
        if host:
            _query = _query & Q(host=host)
        if cloud:
            # TODO: check assignment group search
            assignment_obj = Assignment.objects(cloud=cloud).first()
            _query = _query & Q(assignment=assignment_obj)
        if assignment:
            _query = _query & Q(assignment=assignment)
        return queryset.no_cache().filter(_query)
