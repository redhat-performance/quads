from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, PickleType, DateTime, func, Table
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class TimestampMixin:
    @declared_attr.cascading
    def created_at(self):
        return Column(DateTime, default=func.now())


class Serialize:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))


class Role(Base, RoleMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))


class Vlan(Serialize, Base):
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


class Notification(Serialize, Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    fail = Column(Boolean, default=False)
    success = Column(Boolean, default=False)
    initial = Column(Boolean, default=False)
    pre_initial = Column(Boolean, default=False)
    pre = Column(Boolean, default=False)
    one_day = Column(Boolean, default=False)
    three_days = Column(Boolean, default=False)
    five_days = Column(Boolean, default=False)
    seven_days = Column(Boolean, default=False)

    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    assignment = relationship("Assignment", backref="notifications", foreign_keys=[assignment_id])

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


class Cloud(Serialize, Base):
    __tablename__ = "clouds"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_redefined = Column(Date, default=func.now())

    def __repr__(self):
        return "<Cloud(id='{}', name='{}', last_redefined={})>".format(
            self.id, self.name, self.last_redefined
        )


class Assignment(Serialize, TimestampMixin, Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=False)
    provisioned = Column(Boolean, default=False)
    validated = Column(Boolean, default=False)
    description = Column(String)
    owner = Column(String)
    ticket = Column(String)
    qinq = Column(Integer)
    wipe = Column(Boolean, default=False)
    ccuser = Column(MutableList.as_mutable(PickleType), default=[])

    # many-to-one parent
    cloud_id = Column(Integer, ForeignKey("clouds.id"))
    cloud = relationship("Cloud", foreign_keys=[cloud_id])

    # one-to-one parent
    notification = relationship(
        "Notification", backref="assignments", uselist=False
    )

    # many-to-one parent
    vlan_id = Column(Integer, ForeignKey("vlans.id"))
    vlan = relationship("Vlan", foreign_keys=[vlan_id])


class Disk(Serialize, Base):
    __tablename__ = "disks"
    id = Column(Integer, primary_key=True)
    disk_type = Column(String)
    size_gb = Column(Integer)
    count = Column(Integer)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Memory(Serialize, Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True)
    handle = Column(String)
    size_gb = Column(Integer)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Processor(Serialize, Base):
    __tablename__ = "processors"
    id = Column(Integer, primary_key=True)
    handle = Column(String)
    vendor = Column(String)
    product = Column(String)
    cores = Column(Integer)
    threads = Column(Integer)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Interface(Serialize, Base):
    __tablename__ = "interfaces"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bios_id = Column(String)
    mac_address = Column(String)
    switch_ip = Column(String)
    switch_port = Column(String)
    speed = Column(Integer)
    vendor = Column(String)
    pxe_boot = Column(Boolean, default=False)
    maintenance = Column(Boolean, default=False)

    host_id = Column(Integer, ForeignKey("hosts.id"))


class Host(Serialize, TimestampMixin, Base):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    host_type = Column(String)
    build = Column(Boolean, default=False)
    validated = Column(Boolean, default=False)
    switch_config_applied = Column(Boolean, default=False)
    broken = Column(Boolean, default=False)
    retired = Column(Boolean, default=False)
    last_build = Column(Date)

    # many-to-one
    cloud_id = Column(Integer, ForeignKey("clouds.id"))
    cloud = relationship("Cloud", foreign_keys=[cloud_id])

    # many-to-one
    default_cloud_id = Column(Integer, ForeignKey("clouds.id"))
    default_cloud = relationship("Cloud", foreign_keys=[default_cloud_id])

    # one-to-many parent
    interfaces = relationship("Interface")

    # one-to-many parent
    disks = relationship("Disk")

    # one-to-many parent
    memory = relationship("Memory")

    # one-to-many parent
    processors = relationship("Processor")


class Schedule(Serialize, TimestampMixin, Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    start = Column(Date)
    end = Column(Date)
    build_start = Column(Date)
    build_end = Column(Date)
    index = Column(Integer)

    # many-to-one parent
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    assignment = relationship("Assignment", foreign_keys=[assignment_id])

    # many-to-one parent
    host_id = Column(Integer, ForeignKey("hosts.id"))
    host = relationship("Host", foreign_keys=[host_id])
