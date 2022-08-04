from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, PickleType, DateTime, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, declarative_mixin, declarative_base

Base = declarative_base()


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, default=func.now())


class Vlan(Base):
    __tablename__ = "vlans"
    id = Column(Integer, primary_key=True)
    gateway = Column(String)
    ip_free = Column(Integer)
    ip_range = Column(String)
    netmask = Column(String)
    vlan_id = Column(Integer)

    def __repr__(self):
        return "<Vlan(vlan_id='{}', ip_free='{}', ip_range={}, netmask={}, gateway={})>".format(
            self.vlan_id, self.ip_free, self.ip_range, self.netmask, self.gateway
        )


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    fail = Column(Boolean)
    success = Column(Boolean)
    initial = Column(Boolean)
    pre_initial = Column(Boolean)
    pre = Column(Boolean)
    one_day = Column(Boolean)
    three_days = Column(Boolean)
    five_days = Column(Boolean)
    seven_days = Column(Boolean)

    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    assignment = relationship("Assignment", back_populates="notifications")

    def __repr__(self):
        return (
            "<Notification(id='{}', fail='{}', success={}, initial={}, pre_initial={}, "
            "pre={}, one_day={}, three_days={}, five_days={}, seven_days={}, assignment_id={})>".format(
                self.id,
                self.fail,
                self.success,
                self.initial,
                self.pre_initial,
                self.pre,
                self.one_day,
                self.three_days,
                self.five_days,
                self.seven_days,
                self.assignment_id,
            )
        )


class Cloud(Base):
    __tablename__ = "clouds"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_redefined = Column(Date)

    def __repr__(self):
        return "<Cloud(id='{}', name='{}', last_redefined={})>".format(
            self.id, self.name, self.last_redefined
        )


class Assignment(TimestampMixin, Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    provisioned = Column(Boolean)
    validated = Column(Boolean)
    description = Column(String)
    owner = Column(String)
    ticket = Column(String)
    qinq = Column(Integer)
    wipe = Column(Boolean)
    ccuser = Column(MutableList.as_mutable(PickleType), default=[])

    # many-to-one parent
    cloud_id = Column(Integer, ForeignKey("clouds.id"))
    cloud = relationship("Cloud")

    # one-to-one parent
    notification = relationship(
        "Notification", back_populates="assignments", uselist=False
    )

    # many-to-one parent
    vlan_id = Column(Integer, ForeignKey("vlans.id"))
    vlan = relationship("Vlan")


class Disk(Base):
    __tablename__ = "disks"
    id = Column(Integer, primary_key=True)
    disk_type = Column(String)
    size_gb = Column(Integer)
    count = Column(Integer)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True)
    handle = Column(String)
    size_gb = Column(Integer)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Processor(Base):
    __tablename__ = "processors"
    id = Column(Integer, primary_key=True)
    handle = Column(String)
    vendor = Column(String)
    product = Column(String)
    cores = Column(Integer)
    threads = Column(Integer)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Interface(Base):
    __tablename__ = "interfaces"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bios_id = Column(String)
    mac_address = Column(String)
    switch_ip = Column(String)
    switch_port = Column(String)
    speed = Column(Integer)
    vendor = Column(String)
    pxe_boot = Column(Boolean)
    maintenance = Column(Boolean)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Host(TimestampMixin, Base):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    host_type = Column(String)
    build = Column(Boolean)
    validated = Column(Boolean)
    switch_config_applied = Column(Boolean)
    broken = Column(Boolean)
    retired = Column(Boolean)
    last_build = Column(Date)

    # many-to-one
    cloud_id = Column(Integer, ForeignKey("clouds.id"))
    cloud = relationship("Cloud")

    # many-to-one
    default_cloud_id = Column(Integer, ForeignKey("clouds.id"))
    default_cloud = relationship("Cloud")

    # one-to-many parent
    interfaces = relationship("Interface")

    # one-to-many parent
    disks = relationship("Disk")

    # one-to-many parent
    memory = relationship("Memory")

    # one-to-many parent
    processors = relationship("Processor")


class Schedule(TimestampMixin, Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    start = Column(Date)
    end = Column(Date)
    build_start = Column(Date)
    build_end = Column(Date)
    index = Column(Integer)

    # many-to-one parent
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    assignment = relationship("Assignment")

    # many-to-one parent
    host_id = Column(Integer, ForeignKey("hosts.id"))
    host = relationship("Host")
