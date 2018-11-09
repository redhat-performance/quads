# PDU Management

In order to be able to turn off the connected systems, the scripts
in this directory are used to ensure power is off or on for the given
chassis in order to properly reset the out of band interfaces to
connected hardware.  This is to overcome occasional bugs or issues
with the out of band not properly responding to IPMI commands or
Dell hardware giving erroneous results over the "racadm" command.

In our environment we have two types of PDUs that are managed and
connected via telnet and/or ssh.  We have ServerTech as well as APC
pdus.

Ensure your quads host has access to the PDUs and can resolve the hosts
listed in the PDU-connections.txt file.  The format of this file is:

	<pdu short hostname>,<port>,<quads resource short hostname>

for example, if you have a host in your quads environment that can
be allocated to users, such as:

	a01-h03-r630.example.com

then you will want a line in PDU-connections.txt for each power supply
connection.  For example you might have:

      a01-pdu-01,3,a01-h03-r630
      a01-pdu-02,3,a01-h03-r630

This means that the host a01-h03-r630 is connected to two PDUs,
a01-pdu-01 and a01-pdu-02 on outlet 3 for each PDU.  Furthermore,
your quads host can lookup the IP address for those PDUs by their
short name.
