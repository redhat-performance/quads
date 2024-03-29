#!/usr/bin/python3

import logging
import smtplib

from email.message import EmailMessage
from quads.config import Config

logger = logging.getLogger(__name__)


class Postman(object):
    def __init__(self, subject, to, cc, content):
        self.subject = subject
        self.to = to
        self.cc = cc
        self.content = content

    def send_email(self):
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = "%s <%s>" % (
            Config["mail_display_name"],
            "@".join(["quads", Config["domain"]]),
        )
        msg["To"] = "@".join([self.to, Config["domain"]])
        msg["Cc"] = ",".join(self.cc)
        msg.add_header("Reply-To", "dev-null@%s" % Config["domain"])
        msg.add_header("User-Agent", Config["mail_user_agent"])
        msg.set_content(self.content)
        email_host = Config["email_host"]
        with smtplib.SMTP(email_host) as s:
            try:
                logger.debug(msg)
                s.send_message(msg)
            except smtplib.SMTPException as ex:
                logger.debug(ex)
                logger.error("Postman got bit by a dog, woof! woof!")
                return False
        return True
