import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from quads.config import conf


class Postman(object):
    def __init__(self, subject, to, cc, content):
        self.subject = subject
        self.to = to
        self.cc = cc
        self.content = content

    def send_email(self):
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = Address("QUADS", "quads", conf["domain"])
        msg["To"] = Address(username=self.to, domain=conf["domain"])
        msg["Cc"] = ",".join(self.cc)
        msg.add_header("Reply-To", "dev-null@%s" % conf["domain"])
        msg.attach(self.content)
        with smtplib.SMTP('localhost') as s:
            s.send_message(msg)
