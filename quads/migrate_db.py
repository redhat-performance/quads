from quads.model import Host, Schedule, Vlan, Cloud, CloudHistory
from quads.server import models
from quads.server.models import db


def main():
    clouds = Cloud.objects()
    for cloud in clouds:
        _cloud = models.Cloud(name=cloud.name, last_redefined=cloud.last_redefined)
        db.session.add(_cloud)

    hosts = Host.objects()
    for host in hosts:
        _cloud = (
            db.session.query(models.Cloud)
            .filter(models.Cloud.name == host.cloud.name)
            .first()
        )
        _default_cloud = (
            db.session.query(models.Cloud)
            .filter(models.Cloud.name == host.default_cloud.name)
            .first()
        )
        _host = models.Host(
            name=host.name,
            model=host.model,
            cloud=_cloud,
            default_cloud=_default_cloud,
            host_type=host.host_type,
            build=host.build,
            validated=host.validated,
            switch_config_applied=host.switch_config_applied,
            broken=host.broken,
            retired=host.retired,
            last_build=host.last_build,
        )

        for interface in host.interfaces:
            _interface = models.Interface(
                name=interface.name,
                bios_id=interface.bios_id,
                mac_address=interface.mac_address,
                switch_ip=interface.switch_ip,
                switch_port=interface.switch_port,
                speed=interface.speed,
                vendor=interface.vendor,
                pxe_boot=interface.pxe_boot,
                maintenance=interface.maintenance,
            )
            db.session.add(_interface)
            _host.interfaces.append(_interface)

        for disk in host.disks:
            _disk = models.Disk(
                disk_type=disk.disk_type,
                size_gb=disk.size_gb,
                count=disk.count,
            )
            db.session.add(_disk)
            _host.disks.append(_disk)

        for memory in host.memory:
            _memory = models.Memory(
                handle=memory.handle,
                size_gb=memory.size_gb,
            )
            db.session.add(_memory)
            _host.memory.append(_memory)

        for processor in host.processors:
            _processor = models.Processor(
                handle=processor.handle,
                vendor=processor.vendor,
                product=processor.product,
                cores=processor.cores,
                threads=processor.threads,
            )
            db.session.add(_processor)
            _host.processors.append(_processor)

        db.session.add(_host)

    schedules = Schedule.objects()
    for schedule in schedules:
        _host = db.session.query(models.Host).filter(name=schedule.host.name).first()
        _schedule = models.Schedule(
            start=schedule.start,
            end=schedule.end,
            build_start=schedule.build_start,
            build_end=schedule.build_end,
            index=schedule.index,
            host=_host,
        )
        db.session.add(_schedule)

    vlans = Vlan.objects()
    for vlan in vlans:
        _vlan = models.Vlan(
            gateway=vlan.gateway,
            ip_free=vlan.ip_free,
            ip_range=vlan.ip_range,
            netmask=vlan.netmask,
            vlan_id=vlan.vlan_id,
        )
        db.session.add(_vlan)

    history = CloudHistory.objects()
    for cloud in history:
        notification = models.Notification(
            fail=cloud.notification.fail,
            success=cloud.notification.success,
            initial=cloud.notification.initial,
            pre_initial=cloud.notification.pre_initial,
            pre=cloud.notification.pre,
            one_day=cloud.notification.one_day,
            three_days=cloud.notification.three_days,
            five_days=cloud.notification.five_days,
            seven_days=cloud.notification.seven_days,
        )
        vlan = db.session.query(models.Vlan).filter(vlan_id=cloud.vlan.vlan_id).first()

        assignment = models.Assignment(
            active=False,
            provisioned=True,
            validated=True,
            description=cloud.description,
            owner=cloud.owner,
            ticket=cloud.ticket,
            qinq=cloud.qinq,
            wipe=cloud.wipe,
            cloud=cloud.cloud,
            notification=notification,
            vlan=vlan,
        )

        for user in cloud.ccuser:
            assignment.ccuser.append(user)

        db.session.add(assignment)
        db.session.add(notification)
