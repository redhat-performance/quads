import os
import smtplib

from datetime import datetime, timedelta
from email.message import EmailMessage
from email.headerregistry import Address
from helpers import quads_load_config
from jinja2 import Template
from pathlib import Path
from quads import Quads
from tools.common import environment_released
from tools.netcat import Netcat
from util import get_cloud_summary, get_tickets, get_cc


conf_file = os.path.join(os.path.dirname(__file__), "../../conf/quads.yml")
conf = quads_load_config(conf_file)

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "../templates")


def send_email(subject, to, cc, content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Address("QUADS", "quads", conf["domain"])
    msg["To"] = Address(username=to, domain=conf["domain"])
    msg["Cc"] = ",".join(cc)
    msg.add_header("Reply-To", "dev-null@%s" % conf["domain"])
    msg.attach(content)
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)


def create_initial_message(real_owner, cloud, cloud_info, ticket, cc, released):
    template_file = "initial_message"
    irc_bot_ip = conf["ircbot_ipaddr"]
    irc_bot_port = conf["ircbot_port"]
    irc_bot_channel = conf["ircbot_channel"]
    report_file = "%s-%s-pre-initial-%s" % (cloud, real_owner, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        if released:
            Path(report_file).touch()
            if conf["email_notify"]:
                with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                    template = Template(_file.read)
                content = template.render(
                    cloud_info=cloud_info,
                    wp_wiki=conf["wp_wiki"],
                    cloud=cloud,
                    quads_url=conf["quads_url"],
                    real_owner=real_owner,
                    ticket=ticket,
                    foreman_url=conf["foreman_url"],
                )
                send_email("New QUADS Assignment Allocated", real_owner, cc_users, content)
        if conf["irc_notify"]:
            with Netcat(irc_bot_ip, irc_bot_port) as nc:
                nc.write(
                    "%s QUADS: %s is now active, choo choo! - http://%s/assignments/#%s" % (
                        irc_bot_channel,
                        cloud_info,
                        conf["wp_wiki"],
                        cloud
                    )
                )

    return


def create_message(
        real_owner,
        day,
        cloud,
        cloud_info,
        ticket,
        cc,
        released,
        current_hosts,
        future_hosts
):
    template_file = "message"
    report_file = "%s-%s-%s-%s" % (cloud, real_owner, day, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        if released:
            host_list_expire = set(current_hosts) - set(future_hosts)
            if host_list_expire:
                Path(report_file).touch()
                if conf["email_notify"]:
                    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                        template = Template(_file.read)
                    content = template.render(
                        days_to_report=day,
                        cloud_info=cloud_info,
                        wp_wiki=conf["wp_wiki"],
                        cloud=cloud,
                        hosts=host_list_expire,
                    )
                    send_email("QUADS upcoming expiration notification", real_owner, cc_users, content)

    return


def create_future_initial_message(real_owner, cloud, cloud_info, ticket, cc):
    template_file = "future_initial_message"
    report_file = "%s-%s-pre-initial-%s" % (cloud, real_owner, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        Path(report_file).touch()
        if conf["email_notify"]:
            with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                template = Template(_file.read)
            content = template.render(
                cloud_info=cloud_info,
                wp_wiki=conf["wp_wiki"],
            )
            send_email("New QUADS Assignment Allocated", real_owner, cc_users, content)

    return


def create_future_message(
        real_owner,
        future_days,
        cloud,
        cloud_info,
        ticket,
        cc,
        released,
        current_hosts,
        future_hosts
):
    template_file = "future_message"
    report_file = "%s-%s-pre-%s" % (cloud, real_owner, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        if released:
            Path(report_file).touch()
            if conf["email_notify"]:
                host_list_expire = set(current_hosts) - set(future_hosts)
                with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                    template = Template(_file.read)
                content = template.render(
                    days_to_report=future_days,
                    cloud_info=cloud_info,
                    wp_wiki=conf["wp_wiki"],
                    cloud=cloud,
                    hosts=host_list_expire,
                )
                send_email("QUADS upcoming assignment notification", real_owner, cc_users, content)

    return


def main():
    days = [1, 3, 5, 7]
    future_days = 7

    default_config = conf["data_dir"] + "/schedule.yaml"
    default_state_dir = conf["data_dir"] + "/state"
    default_move_command = "/bin/echo"

    quads = Quads(
        default_config,
        default_state_dir,
        default_move_command,
        None, False, False, False
    )

    _cloud_summary = get_cloud_summary(quads, None, True)
    _clouds = [cloud.split()[0] for cloud in _cloud_summary]
    _clouds_full = get_cloud_summary(quads, None, False)

    for cloud in _clouds:
        owner = quads.get_owners(cloud)
        real_owner = owner
        if isinstance(owner, list):
            real_owner = owner[0][cloud]
        if real_owner == "nobody":
            continue
        cloud_info = next(ci for ci in _cloud_summary if cloud in ci)
        ticket = get_tickets(quads, cloud)
        cc = get_cc(quads, cloud)
        released = environment_released(quads, real_owner, cloud)
        print('=============== Initial Message')
        create_initial_message(
            real_owner,
            cloud,
            cloud_info,
            ticket,
            cc,
            released
        )
        alerted = False
        for day in days:
            if not alerted:
                now = datetime.now()
                today_date = "%4d-%.2d-%.2d 22:00" % (now.year, now.month, now.day)
                future = now + timedelta(days=day)
                future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
                current_hosts = [host for host in quads.query_cloud_hosts(today_date)[cloud]]
                future_hosts = [host for host in quads.query_cloud_hosts(future_date)[cloud]]
                diff = set(current_hosts) - set(future_hosts)
                if diff:
                    print('=============== Additional Message')
                    create_message(
                        real_owner,
                        day,
                        cloud,
                        cloud_info,
                        ticket,
                        cc,
                        released,
                        current_hosts,
                        future_hosts
                    )
                    alerted = True

    for cloud in _clouds_full:
        if cloud not in _clouds:
            owner = quads.get_owners(cloud)
            real_owner = owner
            if isinstance(owner, list):
                real_owner = owner[0][cloud]
            if real_owner == "nobody":
                continue
            cloud_info = next(ci for ci in _cloud_summary if cloud in ci)
            ticket = get_tickets(quads, cloud)
            cc = get_cc(quads, cloud)
            released = environment_released(quads, real_owner, cloud)
            print('=============== Future Initial Message')
            create_future_initial_message(real_owner, cloud, cloud_info, ticket, cc)
            now = datetime.now()
            today_date = "%4d-%.2d-%.2d 22:00" % (now.year, now.month, now.day)
            future = now + timedelta(days=future_days)
            future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
            current_hosts = [host for host in quads.query_cloud_hosts(today_date)[cloud]]
            future_hosts = [host for host in quads.query_cloud_hosts(future_date)[cloud]]
            diff = set(current_hosts) - set(future_hosts)
            if diff:
                print('=============== Additional Message')
                create_future_message(
                    real_owner,
                    future_days,
                    cloud,
                    cloud_info,
                    ticket,
                    cc,
                    released,
                    current_hosts,
                    future_hosts,
                )


if __name__ == "__main__":
    main()
