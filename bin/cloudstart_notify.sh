#!/bin/sh
cat > /tmp/testmessage <<EOF

To: wfoster@example.com,kambiz@example.com
Subject: QUADS Assignment Start for $1
From: QUADS <quads@example.com>

Greetings,

This is a notification that the following assignment is starting:

$1

http://wiki.example.com/assignments/#$1

Cheers, etc.

EOF

/usr/bin/sendmail -t < /tmp/testmessage 1>/dev/null 2>&1
