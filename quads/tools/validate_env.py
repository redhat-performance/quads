import os

from datetime import datetime
from quads.tools.quads_post_system_test import main as post_system_test
from quads.model import Cloud, Schedule
from jinja2 import Template

from tools.postman import Postman

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "../templates")
TOLERANCE = 14400


def notify_failure(_cloud):
    template_file = "validation_failed"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read)
    parameters = {
        "cloud": _cloud.name,
        "owner": _cloud.owner,
        "ticket": _cloud.ticket,
    }
    content = template.render(**parameters)

    subject = "Validation check failed for {cloud} / {owner} / {ticket}".format(**parameters)
    postman = Postman(subject, _cloud.owner, _cloud.cc_users, content)
    postman.send_email()


def notify_success(_cloud):
    template_file = "validation_succeded"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read)
    parameters = {
        "cloud": _cloud.name,
        "owner": _cloud.owner,
        "ticket": _cloud.ticket,
    }
    content = template.render(**parameters)

    subject = "Validation check succeeded for {cloud} / {owner} / {ticket}".format(**parameters)
    postman = Postman(subject, _cloud.owner, _cloud.cc_users, content)
    postman.send_email()


def env_allocation_time_exceeded(_cloud):
    now = datetime.now()
    schedule = Schedule.objects(cloud=_cloud, start__lt=now).first()
    if now - schedule.start > TOLERANCE:
        return True
    return False


def validate_env(_cloud):
    args = {"cloud": _cloud.name}
    try:
        post_system_test(**args)
    except SystemExit:
        if env_allocation_time_exceeded(_cloud):
            notify_failure(_cloud)

    # TODO: gather ansible-cmdb facts

    # TODO: quads post network tests

    # TODO: quads dell config report

    _cloud.update(valid=True, notified=True)
    return


if __name__ == "__main__":
    clouds = Cloud.objects(released=True, valid=False, notified=False)
    for cloud in clouds:
        validate_env(cloud)
